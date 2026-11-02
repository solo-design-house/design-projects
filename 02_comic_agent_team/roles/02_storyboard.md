# 콘티 작가 (Claude)

## 입력
`script.md`, `bible/style.md`, `bible/` 이미지 목록, (재작업 시) 검수 리포트 또는 팀장 지시

## 순서
1. 장면별로 카메라 흐름을 정한다. 장면 첫 컷은 넓은 샷으로 장소를 보여주고, 이후 컷은 가까워진다.
2. 대화 장면에서는 인물의 좌우 위치를 장면 내내 고정한다(180도 규칙).
3. 컷마다 `storyboard.json` 항목을 쓴다.
   - `shot`: 샷 크기, 앵글
   - `characters`: 위치, 표정, 포즈
   - `background`: 배경 기준 파일
   - `dialogue`: 대사와 말풍선 위치
   - `empty_area`: 말풍선 자리로 비워 둘 영역
   - `mode`: 장면 첫 컷이면 `generate`, 같은 장면의 연속 컷이면 `edit_prev`
   - `references`: 참조 이미지 목록. `generate`이면 그림체 기준 + 캐릭터 시트 + 배경 기준, `edit_prev`이면 직전 컷 + 캐릭터 시트
   - `prompt`: 완성된 이미지 프롬프트
4. `prompt`는 다음 순서로 쓴다.
   1. `bible/style.md`의 그림체 문구
   2. 캐릭터 고정 문구
   3. 이 컷의 구도, 행동, 표정
   4. 배경
   5. 비울 영역
   6. "no text, no speech bubbles"
   - `edit_prev` 컷은 직전 컷에서 **바뀌는 점만** 쓴다.
5. 말풍선이 얼굴이나 핵심 행동 위에 오지 않는지, 읽는 순서(왼→오, 위→아래)와 대사 순서가 맞는지 확인한다.

## 산출물
`storyboard.json` (16개 항목)
