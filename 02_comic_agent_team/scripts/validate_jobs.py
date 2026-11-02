#!/usr/bin/env python3
"""작화 지시서 검사: scripts/validate_jobs.py work/<작품명> [id ...]
id를 주지 않으면 jobs/*.json 전체를 검사한다. 문제가 있으면 종료 코드 1."""
import json, sys
from pathlib import Path

REQ = ["id", "kind", "artist", "mode", "prompt", "references", "aspect", "n", "output"]
ENUM = {"kind": {"style", "sheet", "bg", "panel"}, "artist": {"A", "B"},
        "mode": {"generate", "edit_prev"}, "aspect": {"square", "portrait", "landscape"}}

def check(work: Path, job_path: Path, planned: set) -> list:
    errs = []
    try:
        j = json.loads(job_path.read_text())
    except Exception as e:
        return [f"JSON 오류: {e}"]
    for k in REQ:
        if k not in j:
            errs.append(f"필수 필드 없음: {k}")
    if errs:
        return errs
    if j["id"] != job_path.stem:
        errs.append(f"id({j['id']})와 파일명({job_path.stem})이 다름")
    for k, allowed in ENUM.items():
        if j[k] not in allowed:
            errs.append(f"{k} 값 오류: {j[k]}")
    if not (isinstance(j["n"], int) and 1 <= j["n"] <= 4):
        errs.append("n은 1–4 정수")
    if j["kind"] == "panel" and j["n"] != 1:
        errs.append("panel은 n=1")
    out = j["output"]
    want_dir = "panels/" if j["kind"] == "panel" else "bible/"
    if not out.startswith(want_dir) or not out.endswith(".png"):
        errs.append(f"output은 {want_dir}*.png 이어야 함: {out}")
    elif (work / out).exists() or (work / out.replace(".png", "_c1.png")).exists():
        errs.append(f"output 이미 있음: {out}")
    def exists(p):  # 이미 있거나, 같은 실행 묶음에서 먼저 만들어질 파일
        return (work / p).exists() or p in planned
    for r in j["references"]:
        if not exists(r):
            errs.append(f"참조 파일 없음: {r}")
    if j["mode"] == "edit_prev":
        t = j.get("edit_target")
        if not t:
            errs.append("edit_prev인데 edit_target 없음")
        elif not exists(t):
            errs.append(f"edit_target 없음: {t}")
    if "text" in j["prompt"].lower() and "no text" not in j["prompt"].lower():
        errs.append("경고: prompt에 'text'가 들어 있음 (글자 그림 위험)")
    return errs

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    work = Path(sys.argv[1])
    ids = sys.argv[2:]
    paths = [work / "jobs" / f"{i}.json" for i in ids] if ids else sorted((work / "jobs").glob("*.json"))
    bad, planned = 0, set()
    for p in paths:
        if not p.exists():
            print(f"✗ {p.stem}: 지시서 파일 없음"); bad += 1; continue
        errs = check(work, p, planned)
        try:
            o = json.loads(p.read_text()).get("output", "")
            planned.update({o, o.replace(".png", "_c1.png"), o.replace(".png", "_c2.png")})
        except Exception:
            pass
        hard = [e for e in errs if not e.startswith("경고")]
        print(("✗ " if hard else "✓ ") + p.stem + ("" if not errs else ": " + "; ".join(errs)))
        bad += bool(hard)
    print(f"{len(paths) - bad}/{len(paths)} 통과")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
