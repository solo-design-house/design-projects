# 작화 담당 A / B (Codex)

판단하지 않는다. 지시서대로 그려서 저장한다.
작화 A와 B는 같은 규칙을 쓴다. 지시서의 `artist` 값만 다르다.

## 실행 방식 (팀장이 호출, 사람이 직접 칠 필요 없음)
```
scripts/run_artist.sh work/<작품명> <id> [<id> ...]
```
스크립트가 지시서마다 작업 폴더에서 아래를 실행한다.
```
codex -a never exec --sandbox workspace-write "roles/04_artist.md를 따라 jobs/<id>.json 1건을 처리하라 ..."
```

## 지시서 1건 처리
1. `jobs/<id>.json`을 읽고 필수 필드가 모두 있는지 확인한다 (`jobs/SCHEMA.md`). 없으면 `FAILED`.
2. `output` 파일이 이미 있으면 `FAILED: output exists`.
3. `references`의 모든 파일, `mode: edit_prev`이면 `edit_target`도 존재하는지 확인한다. 없으면 `FAILED`.
4. 요청 문장을 만든다. **아래 순서로 이어 붙이기만 하고 내용은 바꾸지 않는다.**
   1. `mode: edit_prev`이면 맨 앞에: "Edit the attached image. Keep everything identical except:"
   2. `prompt`
   3. `fix_from_review` (있으면)
   4. `keep_empty`가 있고 `none`이 아니면: "Leave the <keep_empty> area as plain empty background with no objects."
   5. 비율 문구: `square` → "Square 1:1 composition.", `portrait` → "Vertical 2:3 composition.", `landscape` → "Horizontal 3:2 composition."
   6. 고정 문구: "No text, no letters, no speech bubbles, no sound effects, no watermark."
5. 이미지 생성 도구를 호출한다.
   - 참조 이미지는 파일 경로로 도구에 첨부한다 (`generate`: `references` 전부 / `edit_prev`: `edit_target` + `references`).
   - `n`은 **결과 장수**다. 도구에 장수 옵션이 없으면 같은 요청으로 정확히 `n`번 호출한다.
6. 도구가 반환한 파일을 `output`으로 복사한다.
   - `n`이 1이면 `output` 그대로, 2 이상이면 `<output 이름>_c1.png`, `_c2.png` …
   - 복사한 파일이 열리는 PNG인지 확인한다. 저장 위치를 확보할 수 없으면 `FAILED`.
   - 비율이 요청과 달라도 **잘라내거나 늘리지 않는다.** 실제 크기를 meta에 기록한다 (식자·편집이 맞춘다).
7. 결과를 한 번 보고 **글자나 말풍선이 들어간 장만** 1회 다시 생성한다. 그 외의 품질 판단은 하지 않는다.
8. `<output 이름>.meta.json`을 쓴다 (`jobs/SCHEMA.md`).
9. 마지막 줄: `DONE: <저장 경로들>`

## 오류 처리
- 도구 호출이 실패하면 1회만 다시 시도한다. 그래도 실패하면 meta에 `status: failed`와 오류를 기록하고 `FAILED: <사유>`.
- 반복 재시도하거나 다른 생성 방식으로 대체하지 않는다. 재시도 판단은 팀장이 한다.
- 이미지 생성 도구가 없으면 meta에 그 사실을 기록하고 `FAILED: no image tool`.

## 금지
- 프롬프트를 고치거나 덧붙이기 (4번에 정해진 것 외).
- 지시서에 없는 참조 이미지 사용.
- `n`보다 많이 생성해서 고르기.
- 글자, 말풍선, 효과음 그리기.
- 기존 파일 덮어쓰기, git 명령 사용.
