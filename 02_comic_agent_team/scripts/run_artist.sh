#!/usr/bin/env bash
# Codex 작화 담당 실행: scripts/run_artist.sh work/<작품명> <id> [<id> ...]
# 인자 순서대로 지시서 1건씩 codex exec 1회로 처리한다. (같은 장면은 한 번에 순서대로 넘길 것)
# 환경변수: ARTIST_TIMEOUT(초, 기본 900), CODEX_ARGS(추가 옵션)
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
work="$(cd "${1:?work/<작품명> 필요}" && pwd)"; shift
[ $# -gt 0 ] || { echo "지시서 id 필요"; exit 2; }
command -v codex >/dev/null || { echo "FAILED: codex 미설치 (npm i -g @openai/codex)"; exit 3; }
mkdir -p "$work/logs"
fail=0
for id in "$@"; do
  job="$work/jobs/$id.json"
  if ! python3 "$here/validate_jobs.py" "$work" "$id" >/dev/null; then
    echo "$id FAILED: 지시서 검사 불합격 → $(python3 "$here/validate_jobs.py" "$work" "$id" | head -1)"
    fail=1; continue
  fi
  out="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["output"])' "$job")"
  meta="${out%.png}.meta.json"
  log="$work/logs/$id.log"
  # 같은 지시서 재실행: 이전 실패 meta와 로그는 logs/로 옮겨 보관
  if [ -e "$work/$meta" ]; then
    ts=$(date +%Y%m%d-%H%M%S)
    mv "$work/$meta" "$work/logs/$id.failed-$ts.meta.json"
    [ -e "$log" ] && mv "$log" "$work/logs/$id.failed-$ts.log"
  fi
  start=$(date +%s)
  ( cd "$work" && timeout "${ARTIST_TIMEOUT:-900}" codex -a never exec --sandbox workspace-write ${CODEX_ARGS:-} \
      "roles/04_artist.md를 따라 jobs/$id.json 1건을 처리하라. 이 폴더의 AGENTS.md 규칙을 지켜라. 마지막 줄에 DONE 또는 FAILED를 출력하라." \
      </dev/null >"$log" 2>&1 )
  rc=$?
  secs=$(( $(date +%s) - start ))
  last="$(grep -E '^(DONE|FAILED)' "$log" | tail -n 1)"
  # codex가 시작 전에 실패하면 meta가 없으므로 호출자가 실패 meta를 남긴다
  if [ ! -e "$work/$meta" ]; then
    python3 - "$work/$meta" "$id" "$rc" "$log" <<'PY'
import json, sys, datetime
meta, id_, rc, log = sys.argv[1:]
tail = open(log, errors="replace").read()[-500:]
json.dump({"id": id_, "status": "failed", "files": [], "sizes": [], "final_prompt": "",
           "attached_images": [], "tool_calls": 0, "regenerated_for_text": False,
           "error": f"codex exec rc={rc}, meta 없음 (호출자 기록). log tail: {tail}",
           "finished_at": datetime.datetime.now().isoformat(timespec="seconds"), "written_by": "run_artist.sh"},
          open(meta, "w"), ensure_ascii=False, indent=2)
PY
  fi
  status="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("status"))' "$work/$meta")"
  [ "$status" = done ] && [ $rc -eq 0 ] || fail=1
  echo "$id rc=$rc ${secs}s status=$status ${last:-"(DONE/FAILED 출력 없음)"}"
done
exit $fail
