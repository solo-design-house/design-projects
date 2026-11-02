# AGENTS.md — Codex 작화 담당 공통 규칙

이 작업 폴더(`work/<작품명>/`)에서 Codex는 **작화 담당**으로만 일한다. 글쓰기, 기획, 검수는 하지 않는다.
자세한 절차는 `roles/04_artist.md`를 따른다.

## 운영 방식
- Claude(팀장)가 지시서를 작품 브랜치(`comic/<작품명>`)에 push하고, 사용자가 "처리해" 메시지를 전달한다.
- Codex는 그 브랜치에서 **출력 파일이 아직 없는 지시서**를 모두 처리하고, 결과만 커밋해 같은 브랜치에 push한다.
- 이미지는 이 세션의 이미지 생성 도구(`image_gen.imagegen`)로 직접 만든다. `codex exec`로 다른 Codex를 띄우지 않는다.

## 공통 규칙
- 입력은 `jobs/*.json` 지시서와 지시서에 적힌 참조 이미지뿐이다. 다른 파일을 근거로 판단하지 않는다.
- 쓰기는 지시서의 `output` 경로(후보가 여러 장이면 `_c1`, `_c2` …)와 그 `.meta.json`에만 한다.
  - `kind`가 `panel`이면 `panels/`, `style`·`sheet`·`bg`이면 `bible/`에 쓴다. 이 두 폴더 외에는 쓰지 않는다.
- 기존 파일이 있으면 덮어쓰지 않는다. 그 지시서는 건너뛰고 보고에 `skipped: output exists`로 적는다.
- `production.json`, `brief.md`, `script.md`, `storyboard.json`, `review/`, `jobs/`, `roles/`는 읽기 전용이다.
- git: 작업 전 `git pull`, 커밋은 결과 파일만, push는 작품 브랜치에만. 다른 브랜치·`main`에 push하지 않는다.
- 지시서가 모호하면 추측하지 말고 그 지시서를 실패로 기록하고 질문을 보고에 적는다.
