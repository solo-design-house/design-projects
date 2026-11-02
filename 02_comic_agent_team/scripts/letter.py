#!/usr/bin/env python3
"""식자·조판: scripts/letter.py work/<작품명> [--split] [--fonts DIR]

storyboard.json + 합격 컷(production.json의 passed_file)으로
lettered/pNN.png 와 final/comic.png(세로 스크롤)를 만든다.
--split 이면 final/parts/part_NN.png 로 높이 약 1600px씩 컷 사이에서 나눈다.
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 800
GAP_SAME = 60
GAP_SCENE = 240
SPLIT_H = 1600
RATIO = {"landscape": 3 / 2, "portrait": 2 / 3, "square": 1.0}
FONT_FILES = {  # 세트 B, 없으면 뒤 후보로
    "normal": ["NanumSquareRoundB.ttf", "NanumSquareRoundOTFB.otf", "NanumGothicBold.ttf"],
    "shout": ["Jua-Regular.ttf", "NanumSquareRoundEB.ttf", "NanumGothicExtraBold.ttf"],
    "thought": ["Gaegu-Regular.ttf", "NanumPen.ttf", "NanumGothic.ttf"],
    "sfx": ["BlackHanSans-Regular.ttf", "NanumGothicExtraBold.ttf"],
}
SYSTEM_FALLBACK = ["/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
                   "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"]
SIZE = {"normal": 26, "shout": 34, "thought": 26, "sfx": 56}
SPEAKER_X = {"left": 0.2, "center": 0.5, "right": 0.8}
warnings = []


def load_font(kind, font_dir):
    for name in FONT_FILES[kind]:
        for p in [font_dir / name, *font_dir.rglob(name)] if font_dir.exists() else []:
            if p.exists():
                return ImageFont.truetype(str(p), SIZE[kind])
    for p in SYSTEM_FALLBACK:
        if Path(p).exists():
            warnings.append(f"{kind}: 세트 B 글꼴 없음 → {Path(p).name} 사용")
            return ImageFont.truetype(p, SIZE[kind])
    sys.exit("FAILED: 한글 글꼴이 없음. scripts/setup_codespace.sh 실행 필요")


def crop_to(img, aspect):
    r = RATIO.get(aspect, RATIO["landscape"])
    w, h = img.size
    if w / h > r:
        nw = round(h * r)
        img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    elif w / h < r:
        nh = round(w / r)
        img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return img.resize((WIDTH, round(WIDTH / r)), Image.LANCZOS)


def wrap(text, font, max_w, draw):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if draw.textlength(cur + ch, font=font) > max_w and cur:
            cut = cur.rfind(" ")
            if cut > 0:
                lines.append(cur[:cut]); cur = cur[cut + 1:] + ch
            else:
                lines.append(cur); cur = ch
        else:
            cur += ch
    lines.append(cur)
    return [l for l in lines if l.strip()]


def bubble_size(text, font, max_w, draw):
    lines = wrap(text, font, max_w, draw)
    lh = font.size + 8
    tw = max(draw.textlength(l, font=font) for l in lines)
    return lines, lh, int(tw) + 72, lh * len(lines) + 40


def draw_bubble(draw, box, kind, tail_to, lines, lh, font, tail_max=45):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if kind == "shout":
        pts, n = [], 22
        rx, ry = (x1 - x0) / 2 + 10, (y1 - y0) / 2 + 10
        for i in range(n * 2):
            a = math.pi * i / n
            k = 1.0 if i % 2 == 0 else 0.82
            pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
        draw.polygon(pts, fill="white", outline="black", width=3)
    elif kind == "thought":
        draw.rounded_rectangle(box, radius=28, fill="white", outline="black", width=2)
    else:
        draw.ellipse(box, fill="white", outline="black", width=3)
    if tail_to and kind == "thought":
        tx, ty = tail_to
        for i, r in enumerate((10, 7, 4)):
            px = cx + (tx - cx) * (0.45 + 0.2 * i)
            py = y1 + (ty - y1) * (0.3 + 0.25 * i) if ty > y1 else y0 + (ty - y0) * (0.3 + 0.25 * i)
            draw.ellipse((px - r, py - r, px + r, py + r), fill="white", outline="black", width=2)
    elif tail_to:
        # 꼬리: 말풍선 가장자리에서 화자 쪽으로 짧게 (얼굴을 가로지르지 않게)
        tx, ty = tail_to
        dx, dy = tx - cx, ty - cy
        dist = math.hypot(dx, dy) or 1
        ux, uy = dx / dist, dy / dist
        rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
        edge = 1 / math.sqrt((ux / rx) ** 2 + (uy / ry) ** 2)  # 타원 경계까지 거리
        length = max(12, min(tail_max, dist - edge))
        px, py = -uy * 13, ux * 13
        bx, by = cx + ux * (edge - 10), cy + uy * (edge - 10)
        tip = (cx + ux * (edge + length), cy + uy * (edge + length))
        draw.polygon([(bx + px, by + py), (bx - px, by - py), tip], fill="white", outline="black", width=3)
        # 이음새: 말풍선 테두리와 꼬리 안쪽 선을 지운다
        ix, iy = cx + ux * (edge - 14), cy + uy * (edge - 14)
        jx, jy = cx + ux * (edge + 4), cy + uy * (edge + 4)
        draw.polygon([(ix + px * 0.75, iy + py * 0.75), (ix - px * 0.75, iy - py * 0.75),
                      (jx - px * 0.55, jy - py * 0.55), (jx + px * 0.55, jy + py * 0.55)], fill="white")
    ty = cy - lh * len(lines) / 2 + 2
    for l in lines:
        w = draw.textlength(l, font=font)
        draw.text((cx - w / 2, ty), l, font=font, fill="black")
        ty += lh


def region(pos, W, H, bw, bh, m=16):
    v, _, h = (pos or "top-left").partition("-")
    if not h:
        v, h = ("top", v) if v in ("left", "right", "center") else (v, "center")
    x = {"left": m, "center": (W - bw) / 2, "right": W - bw - m}.get(h, m)
    y = {"top": m, "middle": (H - bh) / 2, "center": (H - bh) / 2, "bottom": H - bh - m}.get(v, m)
    return x, y


def speaker_point(panel, speaker, W, top, H):
    pos = "center"
    for c in panel.get("characters", []):
        if c.get("id") == speaker:
            pos = c.get("pos", "center")
    return W * SPEAKER_X.get(pos, 0.5), top + H * 0.35


def render_panel(panel, img_path, fonts):
    art = crop_to(Image.open(img_path).convert("RGB"), panel.get("aspect", "landscape"))
    W, H = art.size
    tmp = ImageDraw.Draw(art)
    above, below, inside = [], [], []
    for d in panel.get("dialogue", []):
        pos = d.get("position", "top-left")
        (above if pos == "gutter-above" else below if pos == "gutter-below" else inside).append(d)

    def gutter_block(items):
        if not items:
            return 0, []
        laid, x, h = [], 24, 0
        for d in items:
            f = fonts[d.get("bubble", "normal")]
            lines, lh, bw, bh = bubble_size(d["text"], f, W * 0.55, tmp)
            laid.append((d, f, lines, lh, bw, bh)); h = max(h, bh)
        return h + 40, laid

    ha, la = gutter_block(above)
    hb, lb = gutter_block(below)
    canvas = Image.new("RGB", (W, ha + H + hb), "white")
    canvas.paste(art, (0, ha))
    draw = ImageDraw.Draw(canvas)

    def place_row(laid, y_top, toward_y):
        n = len(laid)
        for i, (d, f, lines, lh, bw, bh) in enumerate(laid):
            slot = W / n
            sx, sy = speaker_point(panel, d.get("speaker"), W, ha, H)
            x = min(max(sx - bw / 2, slot * i + 12), slot * (i + 1) - bw - 12) if n > 1 else min(max(sx - bw / 2, 12), W - bw - 12)
            box = (x, y_top + 20, x + bw, y_top + 20 + bh)
            draw_bubble(draw, box, d.get("bubble", "normal"), (sx, toward_y), lines, lh, f, tail_max=70)

    place_row(la, 0, ha + 40)
    place_row(lb, ha + H, ha + H - 40)
    for d in inside:
        f = fonts[d.get("bubble", "normal")]
        lines, lh, bw, bh = bubble_size(d["text"], f, W * 0.42, draw)
        x, y = region(d.get("position"), W, H, bw, bh)
        sx, sy = speaker_point(panel, d.get("speaker"), W, ha, H)
        draw_bubble(draw, (x, ha + y, x + bw, ha + y + bh), d.get("bubble", "normal"), (sx, sy), lines, lh, f)
    for s in panel.get("sfx", []):
        f = fonts["sfx"]
        tw = draw.textlength(s["text"], font=f)
        x, y = region(s.get("position", "middle-right"), W, H, tw, f.size)
        draw.text((x, ha + y), s["text"], font=f, fill="black", stroke_width=4, stroke_fill="white")
    return canvas


def passed_file(work, prod, pid):
    p = prod.get("panels", {}).get(pid, {})
    if p.get("passed_file"):
        return work / p["passed_file"]
    cands = sorted((work / "panels").glob(f"{pid}_v*.png"),
                   key=lambda q: int(re.search(r"_v(\d+)", q.name).group(1)))
    if cands:
        warnings.append(f"{pid}: passed_file 없음 → 최신 {cands[-1].name} 사용")
        return cands[-1]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("work")
    ap.add_argument("--split", action="store_true")
    ap.add_argument("--fonts", default=str(Path(__file__).resolve().parent.parent / "fonts"))
    a = ap.parse_args()
    work = Path(a.work)
    board = json.loads((work / "storyboard.json").read_text())
    prod = json.loads((work / "production.json").read_text())
    fonts = {k: load_font(k, Path(a.fonts)) for k in FONT_FILES}
    (work / "lettered").mkdir(exist_ok=True)
    tiles, scenes = [], []
    for panel in sorted(board, key=lambda p: p["panel"]):
        pid = f"p{panel['panel']:02d}"
        src = passed_file(work, prod, pid)
        if not src or not src.exists():
            sys.exit(f"FAILED: {pid} 이미지 없음")
        tile = render_panel(panel, src, fonts)
        tile.save(work / "lettered" / f"{pid}.png")
        tiles.append(tile); scenes.append(panel.get("scene"))
    gaps = [0] + [GAP_SCENE if scenes[i] != scenes[i - 1] else GAP_SAME for i in range(1, len(tiles))]
    total = sum(t.height for t in tiles) + sum(gaps) + 2 * GAP_SAME
    page = Image.new("RGB", (WIDTH, total), "white")
    y, cuts = GAP_SAME, []
    for t, g in zip(tiles, gaps):
        if g:
            cuts.append(y + g // 2)  # 컷 사이 여백 한가운데
        y += g
        page.paste(t, (0, y)); y += t.height
    (work / "final").mkdir(exist_ok=True)
    page.save(work / "final" / "comic.png")
    out = [f"final/comic.png ({WIDTH}x{total})"]
    if a.split:
        (work / "final" / "parts").mkdir(exist_ok=True)
        start, n = 0, 0
        bounds = cuts + [total]
        while start < total:
            ok = [c for c in bounds if c - start <= SPLIT_H and c > start]
            end = ok[-1] if ok else next(c for c in bounds if c > start)  # 긴 컷 1개는 통째로
            n += 1
            page.crop((0, start, WIDTH, end)).save(work / "final" / "parts" / f"part_{n:02d}.png")
            start = end
        out.append(f"final/parts/ {n}장")
    for w in warnings:
        print("경고:", w)
    print("DONE:", ", ".join(out))


if __name__ == "__main__":
    main()
