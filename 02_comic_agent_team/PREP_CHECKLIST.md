# 에이전트 제작 전 준비 체크리스트

## 준비 완료 (저장소에 있음)
- [x] 조직 구성과 Claude/Codex 배치 — `README.md` 1–8절
- [x] 사전 작화 전략 (그림체 선택 → 시트·배경 기준 → 컷마다 참조 생성) — 9절
- [x] Claude 직원 7명 업무 절차 — `roles/`
- [x] Codex 작화 담당 규칙·절차·지시서 형식 — `comic_template/AGENTS.md`, `comic_template/roles/04_artist.md`, `comic_template/jobs/SCHEMA.md`
- [x] Claude 쪽 파일 형식 (진행표, 콘티, 검수 리포트) — `SCHEMAS.md`
- [x] 작품 폴더 틀 — `comic_template/` (`brief.md`, `production.json`, 빈 폴더들)
- [x] Codex 이미지 생성 검증 — 세션 이미지 도구로 생성·참조·편집·후보 여러 장·덮어쓰기 방지 모두 성공 (`codex-smoke-test` 브랜치)
- [x] 운영 방식 확정 — 작품 브랜치 + 사용자 전달 (README 13절)
- [x] Codex에 전달할 메시지 — `CODEX_PROMPT.md` (작품 시작 안내 + 처리 요청)
- [x] 테스트 폴더만 git 제외, 작품 폴더는 작품 브랜치에 커밋 — `.gitignore`

## 사용자가 할 일
- [x] Codex 클라우드 세션 준비 (GitHub 연결)
- [ ] 작품마다 Claude ↔ Codex 메시지 전달 (1화 약 6–8번 + 반려분)

## 에이전트 제작 시작 전에 정할 것
- [ ] 첫 작품의 요청서 (`comic_template/brief.md` 항목)
- [ ] 형식: 4×4 한 페이지 / 세로 스크롤 (이미지 도구 기본 출력이 가로 3:2라는 점 고려)
- [ ] 식자용 한글 글꼴 (무료 상업용)

## 다음 단계 (에이전트 제작)
1. Claude 직원 6명을 하위 에이전트 정의(`.claude/agents/*.md`)로 생성, 팀장 절차는 세션 지침으로 (`roles/` 내용 기반)
2. 팀장용 보조 스크립트 (작품 브랜치 생성, 지시서 묶음 작성·검증, 진행표 갱신, 전달 메시지 출력)
3. 식자·편집용 말풍선 합성 스크립트 (비율 자르기 포함)
4. 짧은 4컷으로 전체 흐름 시험 → 16컷
