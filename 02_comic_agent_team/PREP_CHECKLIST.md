# 에이전트 제작 전 준비 체크리스트

## 준비 완료 (저장소에 있음)
- [x] 조직 구성과 Claude/Codex 배치 — `README.md` 1–8절
- [x] 사전 작화 전략 (그림체 선택 → 시트·배경 기준 → 컷마다 참조 생성) — 9절
- [x] Claude 직원 7명 업무 절차 — `roles/`
- [x] Codex 작화 담당 규칙·절차·지시서 형식 — `comic_template/AGENTS.md`, `comic_template/roles/04_artist.md`, `comic_template/jobs/SCHEMA.md`
- [x] Claude 쪽 파일 형식 (진행표, 콘티, 검수 리포트) — `SCHEMAS.md`
- [x] 작품 폴더 틀 — `comic_template/` (`brief.md`, `production.json`, 빈 폴더들)
- [x] Codex 확인 테스트와 테스트용 지시서 — `codex_smoke_test.md`, `codex_test/jobs/`
- [x] Codex에 전달할 프롬프트 — `CODEX_PROMPT.md`
- [x] 작업 폴더 `work/`는 git 제외 — `.gitignore`

## 사용자가 할 일
- [ ] 로컬에 Codex CLI 설치·로그인 (요금제 또는 API 키)
- [ ] 이 브랜치를 로컬로 받기 (원격에 올리려면 push 필요)
- [ ] `CODEX_PROMPT.md`를 Codex에 전달 → `work/_codex_test/SMOKE_RESULT.md` 받기
- [ ] 로컬에 Claude Code 설치 (팀장이 `codex exec`를 호출하려면 같은 컴퓨터에 있어야 함)

## 에이전트 제작 시작 전에 정할 것
- [ ] Codex 테스트 결과: 내장 이미지 생성으로 진행 가능한가 (불가 시 B안: API 스크립트)
- [ ] 첫 작품의 요청서 (`comic_template/brief.md` 항목)
- [ ] 형식: 4×4 한 페이지 / 세로 스크롤
- [ ] 식자용 한글 글꼴 (무료 상업용)

## 다음 단계 (에이전트 제작)
1. `SMOKE_RESULT.md`의 확정 실행 명령 반영
2. Claude 직원 7명을 `.claude/agents/*.md`로 생성 (`roles/` 내용 기반)
3. 팀장용 실행 스크립트 (단계 진행, `codex exec` 호출, 진행표 갱신)
4. 식자·편집용 말풍선 합성 스크립트
5. 짧은 4컷으로 전체 흐름 시험 → 16컷
