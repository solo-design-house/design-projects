# Codex에게 전달할 프롬프트

아래 블록을 그대로 Codex(대화형 세션, 저장소 루트에서 실행)에 붙여 넣는다.

```
너는 16컷 만화 제작팀의 "작화 담당 A/B" 에이전트를 완성하고 검증하는 일을 맡았다.
작화 담당은 Codex 내장 이미지 생성 기능으로 지시서대로 그림만 그리는 역할이고,
기획·검수·지휘는 Claude 에이전트들이 한다. 너는 그림 판단을 하지 않는다.

## 먼저 읽을 파일 (02_comic_agent_team/ 기준)
1. README.md 8절, 11절 — 전체 구조에서 작화 담당의 위치와 Codex가 읽는 파일
2. comic_template/AGENTS.md — 작화 담당 공통 규칙
3. comic_template/roles/04_artist.md — 작화 절차
4. comic_template/jobs/SCHEMA.md — 지시서·결과 기록 형식
5. codex_smoke_test.md — 이번에 할 테스트

## 할 일
1. codex_smoke_test.md의 "준비"대로 work/_codex_test/ 를 만든다.
2. T1–T6을 순서대로 실행한다. 각 테스트는 반드시 터미널에서
   `codex exec ...` 명령으로 실행한다 (팀장이 실제로 이 방식으로 호출하기 때문).
   네가 이 세션 안에서 직접 그리지 말 것.
   - `codex exec`가 이미지 생성을 못 하거나 샌드박스·권한 때문에 막히면,
     필요한 옵션을 찾아 다시 시도하고, 무엇이 필요했는지 기록한다.
   - 그래도 안 되면 그 테스트는 실패로 기록하고 다음으로 넘어간다.
3. 결과를 work/_codex_test/SMOKE_RESULT.md 에 codex_smoke_test.md가 정한 항목대로 쓴다.
4. 실제 동작과 문서가 다른 부분만 고친다. 고쳐도 되는 파일은 아래 3개뿐이다.
   - comic_template/roles/04_artist.md (특히 "실행 방식"과 6번 "파일 옮기기")
   - comic_template/AGENTS.md
   - comic_template/jobs/SCHEMA.md
   지시서 필드 이름은 바꾸지 말 것 (Claude 쪽이 이 이름으로 지시서를 쓴다).
   필드를 추가해야 하면 SCHEMA.md에 추가하고 이유를 SMOKE_RESULT.md에 쓴다.
5. 팀장(Claude)이 그대로 쓸 수 있는 최종 실행 명령 형식을
   SMOKE_RESULT.md 맨 아래 "확정 실행 명령" 절에 적는다.
   (작업 폴더, --image 첨부 방법, 필요한 옵션 포함)

## 하지 말 것
- 위 3개 외의 파일 수정 (README.md, roles/ 폴더, codex_test/ 포함)
- git commit / push
- work/_codex_test/ 밖에 이미지 생성

## 끝나면 보고
- 테스트별 성공/실패 한 줄씩
- 고친 파일과 고친 이유
- "확정 실행 명령"
- 사용량 한도로 1화(40–60장) 제작이 가능한지 판단
```
