#!/usr/bin/env bash
# 새 작품 작업 폴더 만들기: scripts/new_comic.sh <작품명> [auto|confirm]
set -euo pipefail
cd "$(dirname "$0")/.."
name="${1:?작품명 필요 (영문 소문자·숫자·하이픈)}"
mode="${2:-auto}"
[[ "$name" =~ ^[a-z0-9][a-z0-9-]*$ ]] || { echo "FAILED: 작품명은 영문 소문자·숫자·하이픈만"; exit 1; }
[[ "$mode" == auto || "$mode" == confirm ]] || { echo "FAILED: 모드는 auto 또는 confirm"; exit 1; }
dest="work/$name"
[ -e "$dest" ] && { echo "FAILED: $dest 이미 있음"; exit 1; }
mkdir -p work
cp -r comic_template "$dest"
find "$dest" -name .gitkeep -delete
mkdir -p "$dest/logs"
python3 - "$dest/production.json" "$name" "$mode" <<'PY'
import json, sys, datetime
p, name, mode = sys.argv[1:]
d = json.load(open(p))
d["title"] = name
d["mode"] = mode
d["log"].append({"at": datetime.datetime.now().isoformat(timespec="seconds"), "who": "director", "event": f"created ({mode})"})
json.dump(d, open(p, "w"), ensure_ascii=False, indent=2)
PY
echo "DONE: $dest"
