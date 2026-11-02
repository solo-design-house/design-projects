# Codex 작화 확인 테스트 (Codespace에서 처음 1회)

Codespace에서 `codex exec`로 이미지가 실제로 생성되는지 확인한다.
Claude(팀장)에게 **"Codex 테스트 돌려줘"**라고 하면 아래를 대신 실행하고 결과를 보고한다.

## 준비
```
scripts/new_comic.sh codex-test auto
cp codex_test/jobs/*.json work/codex-test/jobs/
scripts/validate_jobs.py work/codex-test
```

## 실행
```
scripts/run_artist.sh work/codex-test t1_gen_v1 t2_ref_v1 t3_edit_v1 t4_multi_v1
scripts/run_artist.sh work/codex-test t1_gen_v1     # T5: 이미 있으므로 실패해야 정상
```

## 확인 (Claude가 이미지를 열어 판정)
| # | 지시서 | 통과 기준 |
|---|---|---|
| T1 | `t1_gen_v1` | `panels/t1_gen_v1.png` 생성, 노란 우비·단발·안경, 글자 없음, 오른쪽 위가 비어 있음 |
| T2 | `t2_ref_v1` | T1과 같은 인물로 보임 (참조 이미지 반영) |
| T3 | `t3_edit_v1` | T2에서 표정만 바뀌고 나머지 동일 (편집) |
| T4 | `t4_multi_v1` | `bible/t4_multi_v1_c1.png`, `_c2.png` 2장, 캐릭터 시트 |
| T5 | `t1_gen_v1` 재실행 | `output 이미 있음`으로 실패, 기존 파일 보존 |

## 실패하면
- `logs/<id>.log`를 본다.
- 인증 오류(401, 로그인) → 터미널에서 `codex login` 후 다시 실행.
- 이미지 도구 없음(`FAILED: no image tool`) → Codex CLI 버전 확인(`codex --version`), 최신으로 업데이트(`npm i -g @openai/codex`) 후 재시도.
- 그래도 안 되면 대안: Claude가 OpenAI 이미지 API를 직접 호출하는 방식 (API 키 필요).

## 참고: 이전 검증 기록
`codex-smoke-test` 브랜치의 `02_comic_agent_team/codex_test/result/`.
1차(Codex 클라우드 안에서 `codex exec`)는 클라우드 인증 문제로 실패, 2차(Codex 세션 이미지 도구 직접 사용)는 T1–T5 모두 성공.
