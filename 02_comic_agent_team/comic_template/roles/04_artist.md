# 작화 담당 A / B (Codex, 내장 이미지 생성)

판단하지 않는다. 지시서대로 Codex 내장 이미지 생성 기능으로 그려서 저장한다.
작화 A와 B는 같은 규칙을 쓴다. 지시서의 `artist` 값만 다르다.

## 실행 방식 (팀장이 호출)
```
codex exec --cd work/<작품명> \
  --image <참조1> --image <참조2> ... \
  "roles/04_artist.md를 따라 jobs/<id>.json을 처리하라"
```
- 참조 이미지는 팀장이 지시서의 `references`(와 `edit_target`)를 `--image`로 첨부한다.
- 작화 담당은 첨부된 이미지가 지시서 목록과 같은지 먼저 확인한다.

## 입력
`jobs/<id>.json` 1개 (형식은 `jobs/SCHEMA.md`)

## 순서
1. 지시서를 읽고 필수 필드가 모두 있는지 확인한다. 없으면 `FAILED`.
2. `output` 경로에 파일이 이미 있으면 `FAILED: output exists`.
3. 첨부된 이미지가 `references`(+ `edit_target`)와 개수·파일명이 맞는지 확인한다. 다르면 `FAILED`.
4. 이미지 생성 요청 문장을 만든다. **아래 순서로 이어 붙이기만 하고 내용은 바꾸지 않는다.**
   1. `prompt`
   2. `fix_from_review` (있으면)
   3. `keep_empty`가 있으면: "Leave <keep_empty> completely empty background, no objects."
   4. 고정 문구: "No text, no letters, no speech bubbles, no sound effects, no watermark."
   5. `mode: edit_prev`이면 앞에 "Edit the attached image <edit_target>. Keep everything identical except:"를 붙인다.
5. 내장 이미지 생성 기능으로 `n`장 생성한다. 비율은 `aspect`를 따른다.
6. 생성된 파일을 `output` 경로로 옮긴다.
   - `n`이 1이면 `output` 그대로 저장한다.
   - 2 이상이면 `<output 이름>_c1.png`, `_c2.png`처럼 번호를 붙인다.
   - 생성 파일이 기본 저장 위치(예: `$CODEX_HOME/generated_images/`)에 생기면 복사해서 옮긴다.
7. 생성된 이미지를 한 번 보고 **글자나 말풍선이 들어간 장만** 1회 다시 생성한다. 그 외의 품질 판단은 하지 않는다.
8. `<output 이름>.meta.json`을 쓴다 (형식은 `jobs/SCHEMA.md`).
9. `DONE: <저장 경로들>` 출력.

## 오류 처리
- 이미지 생성이 오류나 사용량 한도로 실패하면 1회만 다시 시도한다. 그래도 실패하면 meta에 오류를 기록하고 `FAILED: <오류 내용>`.
- 대기하거나 반복 재시도하지 않는다. 재시도 판단은 팀장이 한다.

## 금지
- 프롬프트를 고치거나 덧붙이기 (4번에 정해진 것 외).
- 지시서에 없는 참조 이미지 사용.
- `n`보다 많이 생성해 고르기.
- 글자, 말풍선, 효과음 그리기.
- 기존 파일 덮어쓰기.
