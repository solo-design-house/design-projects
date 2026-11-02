# Codex 작화 담당 확인 테스트

`codex_test/jobs/`의 지시서 4개를 실제 절차(`roles/04_artist.md`)대로 처리해 보고, 결과를 `work/_codex_test/SMOKE_RESULT.md`에 기록한다.

## 준비
```
mkdir -p work && cp -r comic_template work/_codex_test
cp codex_test/jobs/*.json work/_codex_test/jobs/
cd work/_codex_test
```

## 테스트 (순서대로, 앞 테스트 결과를 뒤에서 참조함)

| # | 확인할 것 | 명령 |
|---|---|---|
| T1 | `codex exec`에서 이미지가 생성·저장되는가, 기본 저장 위치는 어디인가 | `codex exec "roles/04_artist.md를 따라 jobs/t1_gen.json을 처리하라"` |
| T2 | `--image` 참조가 반영되는가 (같은 인물로 보이는가) | `codex exec --image panels/t1_gen_v1.png "roles/04_artist.md를 따라 jobs/t2_ref.json을 처리하라"` |
| T3 | 직전 컷 수정(`edit_prev`)이 표정만 바꾸고 나머지를 유지하는가 | `codex exec --image panels/t2_ref_v1.png "roles/04_artist.md를 따라 jobs/t3_edit.json을 처리하라"` |
| T4 | 가로 비율, 2장 생성(`n: 2`), `_c1/_c2` 파일명 | `codex exec --image panels/t1_gen_v1.png "roles/04_artist.md를 따라 jobs/t4_multi.json을 처리하라"` |
| T5 | 덮어쓰기 금지 | T1 명령을 다시 실행 → `FAILED: output exists`가 나와야 함 |
| T6 | 사용량 | 테스트 후 남은 한도. 1화 ≈ 40–60장이 가능한지 |

## SMOKE_RESULT.md에 기록할 것
- Codex CLI 버전 (`codex --version`), 로그인 방식(ChatGPT 요금제 / API 키)
- 테스트별: 성공 여부, 마지막 줄 출력(`DONE/FAILED`), 걸린 시간, 생성 파일 경로, `meta.json`이 형식대로인지
- 생성 이미지의 실제 기본 저장 위치
- 글자·말풍선이 섞여 나왔는지, `keep_empty` 영역이 비었는지
- 실행에 필요했던 옵션 (샌드박스, 승인 모드, 네트워크 등)
- `roles/04_artist.md`와 실제 동작이 다른 부분
