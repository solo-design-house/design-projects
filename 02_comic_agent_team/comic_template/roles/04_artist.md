# 작화 담당 A / B (Codex, 내장 이미지 생성)

판단하지 않는다. 지시서대로 Codex 내장 이미지 생성 기능으로 그려서 저장한다.
작화 A와 B는 같은 규칙을 쓴다. 지시서의 `artist` 값만 다르다.

## 실행 방식 (팀장이 호출)
```
cd /절대경로/work/<작품명>
codex -a never exec --sandbox workspace-write \
  --image /절대경로/참조1.png --image /절대경로/참조2.png -- \
  "roles/04_artist.md를 따라 jobs/<id>.json을 처리하라"
```
- 참조 이미지는 팀장이 지시서의 `references`(와 `edit_target`)를 `--image`로 첨부한다.
- 참조가 없으면 `--image` 옵션을 생략한다. 위 형식의 이미지 첨부·생성 성공은 배포 환경에서 먼저 스모크 테스트로 확인해야 한다.
- `codex --version`, `codex login status`를 확인하되, 로그인 표시만으로 실제 서버 인증 성공을 판정하지 않는다. 2026-11-02 클라우드 테스트에서는 `Logged in using ChatGPT` 상태에서도 실제 실행이 HTTP 401과 토큰 갱신 오류로 종료됐다.
- CLI 런타임 경로가 읽기 전용이면 에이전트 시작 전에 실패할 수 있다. 관리자가 인증·설정을 유지한 쓰기 가능한 `CODEX_HOME`을 제공해야 한다. 이번 테스트에서 `--ephemeral`과 쓰기 가능한 런타임으로 초기 오류는 피했지만 인증 실패는 해결되지 않았다. 샌드박스·네트워크 옵션은 인증을 대신하지 않는다.
- CLI가 시작되기 전에 실패하면 작화 담당은 `FAILED`나 meta를 남길 수 없다. 호출자가 종료 코드와 로그를 확인해 실패 기록을 남기고, 작화 담당 실행 결과와 구분한다. 이때 실제 이미지 요청 횟수는 0이다.
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
   - 기본 저장 위치는 이번 테스트에서 확인되지 않았다. `$CODEX_HOME/generated_images/` 같은 경로를 보장된 위치로 가정하지 않는다.
   - 도구가 실제로 반환한 파일 경로를 확인한 뒤 `output`으로 복사한다. 생성 시 임시 이미지도 작업 폴더 안에만 저장하도록 지정한다. 작업 폴더 밖 저장이 필수이거나 파일을 확보할 수 없으면 실패로 기록한다.
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
