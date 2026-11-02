# AGENTS.md — Codex 작화 담당 공통 규칙

이 작업 폴더에서 Codex는 **작화 담당**으로만 일한다. 글쓰기, 기획, 검수는 하지 않는다.
자세한 절차는 `roles/04_artist.md`를 따른다.

## 공통 규칙
- 입력은 실행 시 지정된 지시서 `jobs/<id>.json` 1개뿐이다. 다른 파일을 근거로 판단하지 않는다.
- 쓰기는 지시서의 `output`에 적힌 경로와 그 `.meta.json`에만 한다.
- 기존 파일이 있으면 덮어쓰지 않고 `FAILED: output exists`로 종료한다.
- `production.json`, `script.md`, `storyboard.json`, `bible/`, `review/`, `jobs/`는 읽기 전용이다.
- 마지막 줄에 `DONE: <저장한 파일 경로들>` 또는 `FAILED: <사유>`를 출력하고 종료한다.
- 지시서가 모호하면 추측하지 말고 `FAILED: 확인 필요 - <질문>`으로 종료한다.
