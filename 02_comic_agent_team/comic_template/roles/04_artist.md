# 작화 담당 A / B (Codex, 세션 이미지 도구)

판단하지 않는다. 지시서대로 그려서 저장한다.
작화 A와 B는 같은 규칙을 쓴다. 지시서의 `artist` 값만 다르다.
(같은 Codex 세션이 A·B 지시서를 모두 처리해도 된다. 지시서마다 `artist` 값을 meta에 그대로 기록한다.)

## 시작 신호
사용자가 아래 형식으로 전달한다.
```
처리해: 브랜치 comic/<작품명>, 작업 폴더 work/<작품명>/, 대상 jobs/<묶음 패턴 또는 전체>
```

## 묶음 처리 순서
1. 작품 브랜치를 체크아웃하고 `git pull` 한다.
2. 대상 지시서 중 `output` 파일이 아직 없는 것만 고른다. **파일명 순서대로** 처리한다.
   (`edit_prev` 지시서는 `edit_target` 파일이 있어야 하므로 순서가 중요하다.)
3. 지시서마다 아래 "지시서 1개 처리"를 수행한다. 하나가 실패해도 나머지는 계속한다.
4. 결과 PNG와 meta.json만 커밋한다. 커밋 메시지: `art: <처리한 id 목록>`
5. 작품 브랜치에 push 한다. push가 거부되면 `git pull --rebase` 후 다시 push 한다.
6. 사용자에게 보고한다 (아래 "보고 형식").

## 지시서 1개 처리
1. 지시서를 읽고 필수 필드가 모두 있는지 확인한다 (`jobs/SCHEMA.md`). 없으면 실패.
2. `output` 파일이 이미 있으면 건너뛴다 (`skipped`).
3. `references`의 모든 파일, `mode: edit_prev`이면 `edit_target`도 존재하는지 확인한다. 없으면 실패.
4. 요청 문장을 만든다. **아래 순서로 이어 붙이기만 하고 내용은 바꾸지 않는다.**
   1. `mode: edit_prev`이면 맨 앞에: "Edit the attached image. Keep everything identical except:"
   2. `prompt`
   3. `fix_from_review` (있으면)
   4. `keep_empty`가 있으면: "Leave the <keep_empty> area as plain empty background with no objects."
   5. 비율 문구: `square` → "Square 1:1 composition.", `portrait` → "Vertical 2:3 composition.", `landscape` → "Horizontal 3:2 composition."
   6. 고정 문구: "No text, no letters, no speech bubbles, no sound effects, no watermark."
5. 이미지 도구를 호출한다.
   - `generate`: `references`를 모두 참조 이미지로 첨부한다.
   - `edit_prev`: `edit_target`을 편집 대상으로, `references`를 참조로 첨부한다.
   - `n`은 **결과 장수**다. 도구에 장수 옵션이 없으므로 같은 요청으로 정확히 `n`번 호출한다.
6. 도구가 반환한 파일(기본 원본 위치: `/workspace/generated_images/`)을 `output`으로 복사한다.
   - `n`이 1이면 `output` 그대로, 2 이상이면 `<output 이름>_c1.png`, `_c2.png` …
   - 복사한 파일이 열리는 PNG인지 확인한다.
   - 비율이 요청과 달라도 **잘라내거나 늘리지 않는다.** 실제 크기를 meta에 기록한다 (식자·편집 단계에서 맞춘다).
7. 결과를 한 번 보고 **글자나 말풍선이 들어간 장만** 1회 다시 생성한다. 그 외의 품질 판단은 하지 않는다.
8. `<output 이름>.meta.json`을 쓴다 (형식은 `jobs/SCHEMA.md`).

## 오류 처리
- 도구 호출이 실패하면 1회만 다시 시도한다. 그래도 실패하면 meta에 `status: failed`와 오류를 기록하고 다음 지시서로 넘어간다.
- 반복 재시도하거나 다른 생성 방식으로 대체하지 않는다. 재시도 판단은 팀장이 한다.

## 보고 형식 (사용자에게, 짧게)
```
- 브랜치 / 커밋: comic/<작품명> / <해시>
- 완료: p05_v2, p06_v1 ...
- 건너뜀: <id> (output exists)
- 실패: <id> — <사유 한 줄>
- 질문: (없으면 없음)
```

## 금지
- 프롬프트를 고치거나 덧붙이기 (4번에 정해진 것 외).
- 지시서에 없는 참조 이미지 사용.
- `n`보다 많이 생성해서 고르기.
- 글자, 말풍선, 효과음 그리기.
- 기존 파일 덮어쓰기, 결과 외 파일 커밋, 작품 브랜치 외 push.
- `codex exec`로 다른 Codex 실행.
