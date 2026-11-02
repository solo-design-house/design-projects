# jobs/SCHEMA.md — 작화 지시서와 결과 기록 형식

## 지시서 `jobs/<id>.json`

| 필드 | 필수 | 값 | 설명 |
|---|---|---|---|
| `id` | ✓ | `p05_v2`, `style_2`, `char_minji_v1`, `bg_cafe_v1` | 파일명과 같게 |
| `kind` | ✓ | `style` / `sheet` / `bg` / `panel` | 작업 종류 |
| `artist` | ✓ | `A` / `B` | 담당자 (기록용) |
| `mode` | ✓ | `generate` / `edit_prev` | |
| `prompt` | ✓ | 문자열 | 콘티 작가 또는 아트 디렉터가 쓴 최종 프롬프트 |
| `references` | ✓ | 경로 배열 (빈 배열 가능) | 참조 이미지. 팀장이 `--image`로 첨부 |
| `edit_target` | `edit_prev`이면 ✓ | 경로 | 수정할 직전 컷 |
| `aspect` | ✓ | `square` / `portrait` / `landscape` | |
| `n` | ✓ | 1–4 | 생성 장수. 컷은 1, 그림체 테스트·시트·배경 후보는 2–4 |
| `output` | ✓ | 경로 | 예: `panels/p05_v2.png` |
| `keep_empty` | | 문자열 | 말풍선 자리. 예: `top-right 30%` |
| `fix_from_review` | | 문자열 | 검수에서 온 영어 수정 문구 |

### 예시
```json
{
  "id": "p05_v2", "kind": "panel", "artist": "A", "mode": "generate",
  "prompt": "...",
  "references": ["bible/style_anchor.png", "bible/char_minji.png", "bible/bg_cafe.png"],
  "aspect": "square", "n": 1,
  "output": "panels/p05_v2.png",
  "keep_empty": "top-right 30%",
  "fix_from_review": "Exactly five fingers on left hand. Red hair tie."
}
```

## 결과 기록 `<output 이름>.meta.json`

```json
{
  "id": "p05_v2",
  "artist": "A",
  "status": "done",
  "files": ["panels/p05_v2.png"],
  "final_prompt": "<실제로 보낸 요청 문장 전문>",
  "attached_images": ["bible/style_anchor.png", "..."],
  "regenerated_for_text": false,
  "attempts": 1,
  "error": null,
  "finished_at": "2026-11-02T14:03:00+09:00"
}
```
