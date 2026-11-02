#!/usr/bin/env bash
# Codespace 생성 시 1회 실행 (devcontainer postCreateCommand). 수동 재실행도 가능.
set -uo pipefail
cd "$(dirname "$0")/.."

echo "== CLI 설치: Claude Code, Codex =="
npm install -g @anthropic-ai/claude-code @openai/codex || echo "경고: npm 설치 실패"

echo "== 파이썬 라이브러리 =="
pip install --quiet pillow || echo "경고: pillow 설치 실패"

echo "== 한글 글꼴 (세트 B) =="
sudo apt-get update -qq && sudo apt-get install -y -qq fonts-nanum fonts-nanum-extra >/dev/null || echo "경고: 나눔 글꼴 apt 설치 실패"
mkdir -p fonts/LICENSES
get() { curl -fsSL --retry 3 -o "$2" "$1" || echo "경고: 받기 실패 $1"; }
GF=https://raw.githubusercontent.com/google/fonts/main/ofl
get "$GF/jua/Jua-Regular.ttf"                 fonts/Jua-Regular.ttf
get "$GF/jua/OFL.txt"                         fonts/LICENSES/Jua-OFL.txt
get "$GF/gaegu/Gaegu-Regular.ttf"             fonts/Gaegu-Regular.ttf
get "$GF/gaegu/OFL.txt"                       fonts/LICENSES/Gaegu-OFL.txt
get "$GF/blackhansans/BlackHanSans-Regular.ttf" fonts/BlackHanSans-Regular.ttf
get "$GF/blackhansans/OFL.txt"                fonts/LICENSES/BlackHanSans-OFL.txt
# 나눔스퀘어라운드: apt(fonts-nanum-extra)에 있으면 복사, 없으면 letter.py가 나눔고딕 Bold로 대체
f="$(fc-list : file | grep -i 'NanumSquareRoundB\|NanumSquareRoundOTFB' | head -1 | cut -d: -f1)"
if [ -n "$f" ]; then cp "$f" fonts/; else echo "안내: 나눔스퀘어라운드 없음 → 나눔고딕 Bold로 대체. 원하면 네이버 한글한글 아름답게에서 받아 fonts/에 NanumSquareRoundB.ttf로 넣을 것"; fi

echo "== 확인 =="
for c in claude codex python3; do printf '%-8s ' "$c"; command -v $c >/dev/null && echo ok || echo "없음"; done
ls fonts
echo
echo "다음: 터미널에서  cd 02_comic_agent_team && claude  → 로그인"
echo "      별도 터미널에서 codex login  (ChatGPT 계정 또는 API 키)"
