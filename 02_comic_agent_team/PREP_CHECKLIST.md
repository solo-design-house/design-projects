# 준비 현황 체크리스트

## 완료 (저장소에 있음)
- [x] 조직 구성, Claude/Codex 배치, 사전 작화 전략 — `README.md` 1–9절
- [x] Claude 직원 절차 — `roles/` (팀장 `00_director.md` 포함)
- [x] Codex 작화 규칙·절차·지시서 형식 — `comic_template/AGENTS.md`, `comic_template/roles/04_artist.md`, `comic_template/jobs/SCHEMA.md`
- [x] Claude 쪽 파일 형식 — `SCHEMAS.md`
- [x] 작품 폴더 틀 — `comic_template/`
- [x] 형식·글꼴 확정 — 세로 스크롤, 글꼴 세트 B (README 14절)
- [x] Codespace 설정 — 루트 `.devcontainer/devcontainer.json`, `scripts/setup_codespace.sh`
- [x] Claude Code 팀장 지침과 시작 명령 — `CLAUDE.md`, `.claude/commands/comic.md` (`/comic`)
- [x] 하위 에이전트 6개 — `.claude/agents/comic-*.md`
- [x] 스크립트 — `new_comic.sh`, `validate_jobs.py`, `run_artist.sh`, `letter.py` (가짜 codex와 테스트 이미지로 동작 확인)
- [x] 모드 2종 — `auto` / `confirm`

## Codespace에서 확인할 것 (처음 1회)
- [ ] `codex login` 후 `codex_smoke_test.md` 테스트 통과 (`codex exec`에서 이미지 생성이 되는지는 아직 미검증)
- [ ] 나눔스퀘어라운드 설치 여부 (없으면 나눔고딕 Bold로 대체됨)
- [ ] 권한 확인 창이 너무 자주 뜨면 허용 규칙 추가 (README 13절 아래 "권한")

## 다음
1. Codespace에서 Codex 테스트
2. 짧은 주제로 `/comic confirm` 1회 시험 → 단계별 결과 확인
3. 문제 없으면 `/comic auto`로 운영
