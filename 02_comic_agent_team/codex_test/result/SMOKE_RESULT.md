# Codex 작화 담당 스모크 테스트 결과

- 실행일: 2026-11-02 (UTC)
- 환경: ChatGPT 관리형 클라우드 작업. 사용자 로컬 Codex CLI가 아니다.
- 저장소: solo-design-house/design-projects
- 시작 브랜치: ccr-558cff93-e0w82y
- 시작 커밋: `552a8959800305f8a16ca42d95532f18a601cc2c`
- 결과 브랜치: codex-smoke-test (위 커밋에서 생성)
- CLI: `codex-cli 0.163.0`, `/opt/codex/bin/codex`
- 로그인: `codex login status` → `Logged in using ChatGPT`. 요금제 종류는 확인하지 못했다. API 키 로그인은 사용하지 않았다.
- 결론: T1 최종 실패로 즉시 중단. T2–T6는 실행하지 않았다. 이 세션의 이미지 도구나 다른 생성 방식으로 대체하지 않았다.

## 테스트별 결과

| 테스트 | 결과 | 마지막 출력 | 시간 | 생성 파일 | meta 확인 |
|---|---|---|---|---|---|
| T1 최초 | 실패 (CLI 초기화) | `Error: failed to initialize in-process app-server client: Read-only file system (os error 30)` | 0.035초 | 없음 | 에이전트 미시작으로 없음 |
| T1 옵션 조정 후 | 실패 (서버 인증) | `ERROR: Your access token could not be refreshed because you have since logged out or signed in to another account. Please sign in again.` | 1.367초 | 이미지 없음 | 호출자가 `panels/t1_gen_v1.meta.json` 기록 |
| T2 참조 | 미실행 | 없음 | 해당 없음 | 없음 | 해당 없음 |
| T3 edit_prev | 미실행 | 없음 | 해당 없음 | 없음 | 해당 없음 |
| T4 가로·2장 | 미실행 | 없음 | 해당 없음 | 없음 | 해당 없음 |
| T5 덮어쓰기 | 미실행 | 없음 | 해당 없음 | 없음 | 해당 없음 |
| T6 사용량 | 미실행 | 없음 | 해당 없음 | 없음 | 해당 없음 |

두 T1 프로세스 모두 종료 코드 1이다. 모델이 실행되지 않아 에이전트의 `DONE/FAILED` 마지막 줄은 나오지 않았다. 이를 `FAILED` 출력이 있었다고 간주하지 않았다.

실패 meta는 작화 담당이 아니라 이 테스트를 수행한 호출자가 작성했다. SCHEMA의 기존 필드를 모두 포함하며 JSON 파싱과 타입을 확인했다. `attempts: 0`, `files: []`, `final_prompt: ""`는 실제 이미지 요청과 생성물이 없음을 뜻한다. CLI 실행은 2회이며 이미지 요청 재시도는 아니다.

## 실행 경로와 옵션

작업 폴더: `/workspace/design-projects/02_comic_agent_team/work/_codex_test`

준비는 지시대로 `comic_template/`을 `work/_codex_test/`로 복사하고, `codex_test/jobs/*.json`을 그 안의 `jobs/`로 복사했다. 원본 지시서는 수정하지 않았다.

1. 원문 T1 명령을 실행했다. 기본 `CODEX_HOME=/home/agent/.codex`가 읽기 전용이어서 CLI 초기화에 실패했다.
2. 작업 폴더 안에 쓰기 가능한 `.codex-runtime/`을 만들고, 기존 `auth.json`, 빈 `config.toml`, `plugins/`, `skills/`를 심볼릭 링크로 연결했다. 인증 파일 내용은 읽거나 출력하지 않았다. 새 로그인이나 API 키 대체는 하지 않았다.
3. `CODEX_HOME`을 이 경로로 지정하고 `-a never`, `exec --ephemeral --sandbox workspace-write -c sandbox_workspace_write.network_access=true`로 T1을 다시 실행했다. 상위 실행에도 네트워크 권한을 부여했다. 프롬프트에는 작업 폴더 안에서만 생성하고 도구가 없으면 실패를 기록하라는 제약만 추가했다.
4. 초기 app-server 오류는 피했지만 서버에서 HTTP 401 `Could not parse your authentication token` 및 토큰 갱신 실패가 발생했다. 도구 연결 로그에는 HTTP 451 `no_biscuit_no_service`도 있었다. 공유 skills 디렉터리 쓰기 경고도 남았다. 이미지 도구에 도달하지 않았으므로 이미지 도구 지원 여부 자체는 판정할 수 없다.
5. 샌드박스 전체 해제는 하지 않았다. 인증 실패를 권한 옵션으로 해결할 수 있다고 판단하지 않았다.

위 옵션 조합은 초기화 오류 다음 단계에 도달한 재현 조건이다. 모든 옵션이 필수라는 뜻도, 인증·이미지 생성 성공을 확인했다는 뜻도 아니다. 이 클라우드 세션의 도구·인증이 별도 `codex exec` 프로세스에 그대로 전달된다고 가정할 수 없다.

## 이미지·품질·사용량

- 실제 기본 이미지 저장 위치: 미확인. `$CODEX_HOME/generated_images/`는 검증된 경로가 아니다.
- 생성 이미지: 0장. 작업 폴더 밖에서도 생성하지 않았다.
- 글자·말풍선, `keep_empty`, 참조 일치, edit_prev 보존성, 비율·n·후보 파일명: 전부 판정 불가.
- 남은 이미지 한도·요금제별 한도: 조회하지 못했다.
- 1화 40–60장 가능 여부: 확인 불가. 이번 결과는 이미지 사용량 제한에 걸렸다는 증거가 아니다.

## 문서와 실제 차이 / 수정

- `comic_template/roles/04_artist.md`: CLI 초기화·인증 실패는 작화 에이전트 시작 전에 일어나므로 `FAILED`나 meta가 자동으로 생성되지 않는다. 로그인 상태 출력만으로 인증 성공을 보장할 수 없다. 호출자 실패 처리와 환경 사전 확인을 추가했다. 기본 이미지 저장 경로의 추정을 제거하고 실제 도구 반환 경로를 사용하도록 적었다. 실행 예에 작업 폴더·비대화형 옵션·첨부 경로를 명시했으며 생성 성공 미검증을 표시했다.
- `comic_template/jobs/SCHEMA.md`: 기존 결과 필드의 실패 시 의미(`status`, `attempts: 0`, 빈 `files`·`final_prompt`)와 에이전트 시작 전 호출자 기록을 명시했다. 지시서 필드 이름 변경이나 필드 추가는 없다.
- `comic_template/AGENTS.md`: 수정하지 않았다. 작화 에이전트가 실행되지 않았으므로 그 규칙의 실제 수행 차이를 판정할 수 없다.
- README, 원본 roles, codex_test/jobs와 그 밖의 문서는 수정하지 않았다.

## 납품

이 보고서와 `panels/t1_gen_v1.meta.json`을 `02_comic_agent_team/codex_test/result/`로 복사했다. 생성 이미지와 bible 결과가 없으므로 이미지 파일을 만들거나 대체하지 않았다. 빈 `bible/`은 Git이 추적하지 않는다. 런타임·인증 링크·원시 로그·작업용 복사본은 커밋하지 않는다.

## 확정 실행 명령

**이미지 생성 성공이 확인된 확정 명령은 없다.** 아래는 T1 두 번째 실패를 재현하는 명령이며, 배포용으로 검증된 명령이 아니다. 현재 클라우드에서는 별도 CLI의 서버 인증 및 도구 연결을 먼저 해결해야 한다. 로컬 CLI에서의 성공 여부는 별도 검증이 필요하다.

```bash
cd /workspace/design-projects/02_comic_agent_team/work/_codex_test
CODEX_HOME="$PWD/.codex-runtime" codex -a never exec \
  --ephemeral --sandbox workspace-write \
  -c sandbox_workspace_write.network_access=true -- \
  'roles/04_artist.md를 따라 jobs/t1_gen.json을 처리하라. 이미지 생성은 현재 work/_codex_test/ 내부에서만 수행하라. 이미지 생성 도구가 없으면 그 사실을 meta.json에 기록하고 FAILED로 종료하라.'
```

`.codex-runtime`은 위 준비 과정에서 만든 런타임이다. 인증 파일을 Git에 넣거나 토큰을 명령 문자열에 적지 않는다. 인증이 정상인 별도 실행 환경에서는 그 환경이 제공하는 쓰기 가능한 CLI 런타임을 사용해야 한다.

첨부 형식은 `codex exec --help`에서 `--image <FILE>...`를 확인했다. 아래는 T1 성공 후 사용할 T2 첨부 **형식 예시이며, 이번에는 실행하지 않았다.** 상대 경로 혼동을 피하려고 절대 경로를 쓰고 프롬프트 앞에 `--`를 둔다. 여러 참조는 `--image "$PWD/참조1.png" --image "$PWD/참조2.png"`처럼 전달한다. `edit_prev`에서는 `edit_target`도 첨부한다.

```bash
cd /workspace/design-projects/02_comic_agent_team/work/_codex_test
CODEX_HOME="$PWD/.codex-runtime" codex -a never exec \
  --ephemeral --sandbox workspace-write \
  -c sandbox_workspace_write.network_access=true \
  --image "$PWD/panels/t1_gen_v1.png" -- \
  'roles/04_artist.md를 따라 jobs/t2_ref.json을 처리하라'
```
