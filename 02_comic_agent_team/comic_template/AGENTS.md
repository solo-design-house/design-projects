# AGENTS.md — Codex 작화 담당 공통 규칙

이 작업 폴더(`work/<작품명>/`)에서 Codex는 **작화 담당**으로만 일한다. 글쓰기, 기획, 검수는 하지 않는다.
자세한 절차는 `roles/04_artist.md`를 따른다.

## 운영 방식
- 팀장(Claude Code)이 `scripts/run_artist.sh`로 `codex exec`를 실행한다. **실행 1회 = 지시서 1건.**
- 이미지는 Codex의 이미지 생성 도구로 만든다. 다른 Codex를 띄우거나 다른 생성 방식으로 대체하지 않는다.

## 공통 규칙
- 입력은 실행 명령에서 지정한 지시서 `jobs/<id>.json` 1건과 그 안에 적힌 참조 이미지뿐이다.
- 쓰기는 지시서의 `output` 경로(후보가 여러 장이면 `_c1`, `_c2` …)와 그 `.meta.json`에만 한다.
  - `kind`가 `panel`이면 `panels/`, `style`·`sheet`·`bg`이면 `bible/`. 이 두 폴더 외에는 쓰지 않는다.
- 기존 파일이 있으면 덮어쓰지 않고 `FAILED: output exists`로 끝낸다.
- `production.json`, `brief.md`, `script.md`, `storyboard.json`, `review/`, `jobs/`, `roles/`는 읽기 전용이다.
- git 명령(commit, push 등)을 쓰지 않는다.
- 마지막 줄에 `DONE: <저장한 파일 경로들>` 또는 `FAILED: <사유>`를 출력한다.
