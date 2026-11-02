# 파일 형식 정의 (Claude 직원용)

작화 지시서와 결과 기록 형식은 `comic_template/jobs/SCHEMA.md`에 있다 (Codex도 읽음).

## production.json — 팀장만 쓴다
초기 파일: `comic_template/production.json`

| 필드 | 값 |
|---|---|
| `mode` | `auto` / `confirm` |
| `stage` | 현재 단계 `S0`–`S6` |
| `stages.<단계>.status` | `todo` / `in_progress` / `review` / `done` |
| `scenes[]` | `{"id": "s1", "place": "bg_cafe", "panels": ["p01","p02"], "artist": "A"}` |
| `panels.<pNN>.status` | `todo` → `job_written` → `generated` → `reviewing` → `passed` / `passed_with_issues` → `lettered` (불합격 시 `job_written`으로) |
| `panels.<pNN>.version` | 마지막으로 낸 지시서 버전 |
| `panels.<pNN>.fails` | 연속성 검수 불합격 횟수. 2가 되면 팀장 판단 |
| `panels.<pNN>.passed_file` | 잠긴 최종 파일 경로 |
| `artist_runs[]` | 작화 실행 기록 `{"ids": ["p05_v1","p06_v1"], "at": "...", "result": "2 done / 0 failed"}` |
| `log[]` | `{"at": "...", "who": "...", "event": "..."}` |

## storyboard.json — 콘티 작가
배열, 항목 16개.

| 필드 | 필수 | 설명 |
|---|---|---|
| `panel` | ✓ | 1–16 |
| `scene` | ✓ | `scenes[].id`와 같은 값 |
| `act` | ✓ | 기 / 승 / 전 / 결 |
| `shot` | ✓ | 샷 크기, 앵글 |
| `characters` | ✓ | `[{"id", "pos": "left/center/right", "expression", "pose"}]` |
| `background` | ✓ | `bible/bg_*.png` 파일명 |
| `dialogue` | ✓ | `[{"speaker", "text", "bubble": "normal/shout/thought", "position"}]` (없으면 빈 배열). `position`은 컷 안 위치(`top-left` 등) 또는 `gutter-above` / `gutter-below` |
| `sfx` | | `[{"text", "position"}]` |
| `empty_area` | ✓ | 컷 안 말풍선 자리. 예: `top-right 30%`. 여백만 쓰면 `none` |
| `mode` | ✓ | `generate` / `edit_prev` |
| `references` | ✓ | 참조 이미지 경로 배열 |
| `aspect` | ✓ | 세로 스크롤 기본 `landscape`, 강조 컷만 `portrait` |
| `prompt` | ✓ | 최종 이미지 프롬프트 (영어) |

## review/*.json — 검수자
```json
{
  "target": "panels/p05_v2.png",
  "stage": "G4",
  "reviewer": "continuity",
  "verdict": "pass | fail",
  "issues": [
    {"check": 1, "severity": "major | minor", "panel": 5, "detail": "머리끈이 파란색", "fix": "Red hair tie."}
  ]
}
```
- 파일명: `review/continuity_<대상 id>.json`, `review/story_<G1|G3|G5>.json`
- 연속성 검수의 `fix`는 작화 지시서 `fix_from_review`에 그대로 넣을 수 있는 영어 문구로 쓴다.
