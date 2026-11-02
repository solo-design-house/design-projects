# Codex 작화 담당 스모크 테스트 결과

## 2차 시도 — 세션 이미지 도구 직접 사용

- 실행일: 2026-11-02 UTC. 환경: ChatGPT 클라우드.
- 저장소/브랜치: `solo-design-house/design-projects` / `codex-smoke-test`.
- 방식: 사용자 전달 지시서 → 이 대화의 이미지 도구 직접 호출 → PNG·meta 저장 → GitHub push. `codex exec`는 이번 시도에서 실행하지 않았다.
- `comic_template/`을 복사해 `work/_codex_test/`를 새로 준비하고 원본 테스트 지시서 4개를 복사했다. 이전 작업용 런타임과 실패 meta는 제거했다. 이전 보고서는 아래 「1차 시도」에 보존했다.
- 이번에는 문서 파일과 원본 지시서를 수정하지 않았다. 변경 대상은 `codex_test/result/`뿐이다.

### 도구와 지원 옵션

도구 이름은 `image_gen.imagegen`이며 이 런타임의 호출 이름은 `image_gen__imagegen`이다.

| 항목 | 지원/실제 사용 |
|---|---|
| 생성 요청 | `prompt` 문자열 |
| 참조 파일 첨부 | `referenced_image_paths` 로컬 절대 경로 배열. T2·T4에 실제 첨부했다. |
| 기존 이미지 편집 | 동일 옵션에 편집 원본을 첨부하고 prompt로 변경 사항 요청. T3에서 실제 사용했다. 마스크·픽셀 잠금 전용 옵션은 없다. |
| 최근 대화 이미지 | `num_last_images_to_include` (최대 5). 이번에는 사용하지 않았다. 참조 경로 옵션과 동시 사용 불가. |
| 투명 배경 | `transparent_background`. 모든 호출에서 false. |
| 비율/픽셀 크기 | 전용 옵션 없음. 일반적으로 prompt로 요청할 수 있지만, 이번에는 04_artist.md 4단계의 조립 규칙만 지켜 추가 문장을 넣지 않았다. 지시서 `aspect`를 별도 인자로 전달할 수 없었고 T1–T3의 square는 충족하지 못했다. |
| 한 호출에 여러 장 | `n` 전용 옵션 없음. 한 호출의 반환 이미지 1장. T4의 `n: 2`는 같은 prompt와 같은 T1 참조로 순차 2회 호출했다. 한 번에 2장 생성한 것으로 보고하지 않는다. |
| 출력 경로 | 전용 옵션 없음. 도구가 원본을 `/workspace/generated_images/`에 자동 저장하고 data URL과 실제 경로 안내를 반환했다. 그 경로에서 작업 폴더로 바이트 그대로 복사했다. |

### 테스트 판정

아래의 성공은 각 스모크 테스트의 기능 항목을 뜻한다. 지시서의 모든 요구를 충족했다는 뜻은 아니다. **T1–T3는 정사각형 요구 미충족으로 지시서 전체 준수 판정은 실패**다. 모든 PNG를 함께 납품하므로 그림 품질과 연속성 최종 판정은 팀장이 한다.

| 테스트 | 기능 결과 | 소요 시간(이미지 도구 호출) | 마지막 출력 / 확인 |
|---|---|---|---|
| T1 | 성공: 새 이미지 생성·PNG 저장. square 미충족. | 28.522초 | `DONE: panels/t1_gen_v1.png` |
| T2 | 성공: 실제 T1 PNG 첨부로 버스 안 장면 생성. square 미충족. | 34.470초 | `DONE: panels/t2_ref_v1.png` |
| T3 | 성공: 실제 T2 PNG 첨부·놀란 표정으로 편집. square 미충족. | 28.944초 | `DONE: panels/t3_edit_v1.png` |
| T4 | 성공: landscape 2장, `_c1/_c2` 저장. 순차 2회 호출. | 136.857초(합계) | `DONE: bible/t4_multi_v1_c1.png bible/t4_multi_v1_c2.png` |
| T5 | 성공: 기존 output을 확인하고 생성 전에 거부. | 0.001초 미만(파일 검사) | `FAILED: output exists`. PNG와 meta 모두 SHA-256 불변. 이미지 도구 추가 호출 0회. |

실제 이미지 도구 호출은 총 5회, 결과는 5장이다. 도구 오류·사용량 제한 오류는 없었다. 글자·말풍선으로 인한 재생성도 없었다. 프롬프트를 고쳐 품질을 개선하거나 후보를 더 생성해 고르지 않았다. 참조와 편집 대상은 지시서에 적힌 파일만 사용했다.

### 요청 문장·참조·절차

- `prompt` → `fix_from_review`(해당 없음) → `Leave <keep_empty> completely empty background, no objects.`(있을 때) → 고정 금지 문구 순서로 연결했다.
- T3는 그 앞에 `Edit the attached image panels/t2_ref_v1.png. Keep everything identical except:`를 붙였다.
- 실제 보낸 요청 문장 전문은 각 meta의 `final_prompt`에 있다. aspect나 저장 경로를 위한 추가 문구는 넣지 않았다.
- T1: 신규 생성이므로 참조 옵션을 생략했다. 최근 대화 이미지를 참조로 지정하지 않았다.
- T2: `referenced_image_paths`에 작업 폴더의 `panels/t1_gen_v1.png` 1개를 첨부했다. 첨부 전에 `view_image`로 파일을 열어 확인했다.
- T3: 작업 폴더의 `panels/t2_ref_v1.png` 1개를 첨부했다. 첨부 전에 `view_image`로 확인했다.
- T4: 두 호출 모두 작업 폴더의 `panels/t1_gen_v1.png` 1개만 첨부했다. 첫 번째 후보나 T2·T3는 첨부하지 않았다.
- meta의 `attached_images`에는 작업 폴더 기준 경로를 기록했다. 실제 도구에는 같은 파일의 절대 경로를 전달했다.
- meta는 기존 SCHEMA 필드만 사용한다. `attempts`는 T1–T3 각각 1, T4는 총 이미지 생성 요청 횟수인 2다. 모든 meta는 JSON 파싱과 필수 필드를 확인했다.

### 글자·말풍선·여백 관찰

| 테스트 | 글자/말풍선 | keep_empty 관찰 |
|---|---|---|
| T1 | 육안상 없음. 재생성 없음. | 오른쪽 위에 넓은 회색 하늘 여백이 있다. `top-right 30%`의 정확한 좌표·면적 정의가 없어 전 영역 무객체 충족을 정량 보증하지 않는다. |
| T2 | 육안상 없음. 재생성 없음. | 왼쪽 위에 넓은 밝은 여백이 있다. 그 아래·오른쪽에는 창틀과 머리카락이 있어 정확한 사각형 정의가 필요하다. 엄격한 25% 영역 충족은 미확정이다. |
| T3 | 육안상 없음. 재생성 없음. | 지시서에 keep_empty 없음. 눈·입 표정이 변경됐고 배경·자세·의상은 육안상 유지됐다. 비표정 영역의 픽셀 완전 동일성은 보장하지 않는다. |
| T4 c1/c2 | 두 장 모두 육안상 글자·말풍선 없음. 재생성 없음. | keep_empty 없음. 흰 배경 캐릭터 시트. |

### 실제 저장 위치와 파일 검증

최종 작업 폴더: `/workspace/design-projects/02_comic_agent_team/work/_codex_test/`

도구의 실제 기본 저장 위치는 아래와 같다. 생성 파일을 찾기 위해 추정 경로를 스캔하지 않았고, 도구가 반환한 경로를 사용했다. **현재 도구는 임시 원본을 작업 폴더 밖에 자동 저장하므로, 모든 생성 단계의 저장 위치를 work 안으로 한정한다는 종전 규칙은 이 인터페이스로 충족할 수 없다.** 원본을 숨기거나 work에서 처음 만들어진 것처럼 보고하지 않는다. 도구 원본은 남겨 두고, 작업·납품 파일은 아래 work/result 안에 복사했다.

| 호출 | 실제 도구 원본 경로 | 소요 시간 |
|---|---|---|
| t1 | `/workspace/generated_images/exec-e4aaa69f-2244-4699-ba09-b82eb7a23100.png` | 28.522초 |
| t2 | `/workspace/generated_images/exec-12ae6082-b246-43d7-aa3c-7b7690ba7e1a.png` | 34.470초 |
| t3 | `/workspace/generated_images/exec-b252d0dd-5c3a-4e69-a486-61d4caa1a492.png` | 28.944초 |
| t4c1 | `/workspace/generated_images/exec-5d664dda-96f1-44d6-894e-26b45a6abf25.png` | 78.438초 |
| t4c2 | `/workspace/generated_images/exec-36fc85d5-138f-4b43-b814-fc3b50daa54a.png` | 58.419초 |

다음 파일은 확장자뿐 아니라 Pillow `Image.verify()`와 이미지 포맷 확인으로 실제 PNG임을 검증했다. 리사이즈·크롭·후처리는 하지 않았다. 도구 원본, work 파일, result 파일의 SHA-256이 같다.

| 테스트 | 작업 폴더 안 상대 경로 | 포맷 | 크기 | 바이트 | SHA-256 |
|---|---|---|---|---|---|
| T1 | `panels/t1_gen_v1.png` | PNG | 1536×1024 | 2,342,108 | `21466c0bd5cf6cdae55237d57533827260908a565d2a11feb9610f5fd9d152e6` |
| T2 | `panels/t2_ref_v1.png` | PNG | 1536×1024 | 2,198,912 | `d8f7b6f57988b226040bdddc46362a553c4f46586f591a4661f6aa326149e2c1` |
| T3 | `panels/t3_edit_v1.png` | PNG | 1536×1024 | 2,157,396 | `87c2af28e3b3a9ad54ad9487d5ecda327559c26e09550fa7bdf8a5f34c14101c` |
| T4 | `bible/t4_multi_v1_c1.png` | PNG | 1536×1024 | 2,129,732 | `dc2206d29b51c12297df631d7963442a53625480003e784eae62ec0a257048a3` |
| T4 | `bible/t4_multi_v1_c2.png` | PNG | 1536×1024 | 2,086,555 | `3b7293ed9bf26c9e8feda5a2180e62c9b3805ce01c1526c8767a43ef9e0fb287` |

meta 파일:

- `panels/t1_gen_v1.meta.json`
- `panels/t2_ref_v1.meta.json`
- `panels/t3_edit_v1.meta.json`
- `bible/t4_multi_v1.meta.json` (후보 2개를 한 meta의 files 배열에 기록)

T5는 기존 meta도 덮어쓰지 않았다. T5 별도 실행 증거는 이 보고서와 `tool_outputs/test_results.json`에 있다. 실제 도구 반환 경로와 소요 시간은 `tool_outputs/calls.json`에 있다. 이 파일들에는 인증 정보나 이미지 base64를 넣지 않았다.

### 사용량

이번 실행으로 5장의 생성·저장을 확인했다. 남은 이미지 한도나 40–60장 연속 처리 가능 여부를 조회하는 옵션은 이 도구 인터페이스에 없어서 확인하지 못했다. 이번 5장 성공만으로 1화 물량 가능을 보장하지 않는다.

### 문서 수정 제안

이번에는 아래 제안만 기록하며 문서는 수정하지 않는다.

1. 실행 방식을 `codex exec`에서 사용자 중계 + GitHub 지시서 + 세션 이미지 도구 호출로 바꾼다. 현재 세션의 이미지 도구가 별도 CLI 인증 실패와 무관하게 동작함을 확인했다.
2. 참조 첨부를 `--image` 대신 실제 도구의 `referenced_image_paths`로 표현한다. GitHub에서 가져온 참조를 로컬 PNG로 저장한 뒤 첨부한다. `edit_prev`는 edit_target을 첨부하고 지정 편집 문구를 사용한다.
3. `aspect`를 도구에 전달할 전용 옵션이 없는 경우를 정의한다. 현재 4단계는 aspect를 요청 문장에 넣지 않아 square가 누락됐다. 다음 개정에서 aspect 문구를 추가하도록 허용하거나 이를 지원하는 인터페이스를 선택해야 한다. 이번에는 문장을 임의로 추가하거나 이미지를 잘라 맞추지 않았다.
4. `n`은 한 번의 요청 장수가 아니라 총 결과 장수로 해석하고, n 옵션 없는 도구에서는 정확히 n회 호출하도록 한다. T4의 2회 호출과 오류 재시도를 구별해 기록한다.
5. 파일 이동 단계는 도구 반환 경로에서 work/output으로 복사하고 실제 PNG를 검증하도록 쓴다. 도구의 자동 원본 저장 `/workspace/generated_images/`를 명시한다. 생성 자체도 work 밖에서 금지하려면 출력 경로를 지정할 수 있는 도구가 필요하다.
6. `bible/` 읽기 전용 규칙에 kind=sheet/bg/style의 명시적 output 예외가 필요하다. 이번 T4는 사용자가 bible 출력 작업을 직접 승인했으므로 그 경로에 저장했다.
7. `keep_empty`의 퍼센트를 정규화 사각형 좌표로 정의하면 엄격한 검수가 가능하다. 현재 자연어만으로는 무객체 범위를 일치시켜 판단하기 어렵다.
8. T5처럼 생성 전 거부한 경우 기존 성공 meta도 보존하고 별도 실행 로그에 FAILED를 기록한다.

### 납품 및 실행 방식

이미지 5장, meta 4개, 이 보고서와 경로/시간·T5 실행 증거 JSON을 `02_comic_agent_team/codex_test/result/`에 복사했다. 이번 커밋의 변경은 result 폴더로만 제한한다. `codex exec` 실행 명령을 새 확정 방식으로 제시하지 않는다. 사용자가 jobs 지시서를 전달하면 이 세션이 읽고, 파일 참조를 도구에 첨부해 생성·편집하고 PNG와 meta를 GitHub에 올리는 절차를 실제로 수행했다.

## 1차 시도

아래는 보존한 이전 보고서 원문이다. 당시 CLI 인증 실패 기록이며, 이번 직접 도구 테스트 결과와 구분한다. 이전 보고서의 수정·납품·명령 설명은 당시 실행에만 해당한다.

<details>
<summary>1차 시도 원문 펼치기</summary>

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

</details>
