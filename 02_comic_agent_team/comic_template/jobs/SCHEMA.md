# jobs/SCHEMA.md — 작화 지시서와 결과 기록 형식

## 지시서 `jobs/<id>.json`

| 필드 | 필수 | 값 | 설명 |
|---|---|---|---|
| `id` | ✓ | `p05_v2`, `style_2`, `char_minji_v1`, `bg_cafe_v1` | 파일명과 같게. 처리 순서는 파일명 순이므로 `edit_prev`는 직전 컷보다 뒤 이름이어야 한다 |
| `kind` | ✓ | `style` / `sheet` / `bg` / `panel` | `panel`은 `panels/`, 나머지는 `bible/`에 저장 |
| `artist` | ✓ | `A` / `B` | 담당자 (기록용) |
| `mode` | ✓ | `generate` / `edit_prev` | |
| `prompt` | ✓ | 문자열 (영어) | 콘티 작가 또는 아트 디렉터가 쓴 최종 프롬프트 |
| `references` | ✓ | 경로 배열 (빈 배열 가능) | 참조 이미지 |
| `edit_target` | `edit_prev`이면 ✓ | 경로 | 수정할 직전 컷 |
| `aspect` | ✓ | `square` / `portrait` / `landscape` | 도구에 비율 옵션이 없어 요청 문장으로만 전달된다. 실제 비율은 다를 수 있다 |
| `n` | ✓ | 1–4 | **결과 장수.** 도구를 n번 호출한다. 컷은 1, 그림체·시트·배경 후보는 2–4 |
| `output` | ✓ | 경로 | 예: `panels/p05_v2.png`, `bible/char_minji_v1.png` |
| `keep_empty` | | 문자열 | 말풍선 자리. 예: `top-right 30%` |
| `fix_from_review` | | 문자열 (영어) | 검수에서 온 수정 문구 |

### 예시
```json
{
  "id": "p05_v2", "kind": "panel", "artist": "A", "mode": "generate",
  "prompt": "...",
  "references": ["bible/style_anchor.png", "bible/char_minji.png", "bible/bg_cafe.png"],
  "aspect": "landscape", "n": 1,
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
  "sizes": ["1536x1024"],
  "final_prompt": "<실제로 보낸 요청 문장 전문>",
  "attached_images": ["bible/style_anchor.png", "..."],
  "tool_calls": 1,
  "regenerated_for_text": false,
  "error": null,
  "finished_at": "2026-11-02T14:03:00+09:00"
}
```
- `status`: `done` / `failed`. 실패 시 `error`에 원인을 쓴다.
- `tool_calls`: 실제 이미지 도구 호출 횟수 (`n`회 + 글자 재생성 + 오류 재시도). 요청을 보내지 못했으면 0.
- `final_prompt`: 요청을 보내지 못했으면 빈 문자열, 생성 파일이 없으면 `files`는 빈 배열.
- `sizes`: 실제 저장된 이미지 크기. 비율 불일치는 식자·편집이 처리한다.
