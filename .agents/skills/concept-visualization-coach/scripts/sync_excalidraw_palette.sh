#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_SCRIPT="${SCRIPT_DIR}/sync_excalidraw_palette.js"
CONFIG_PATH="${SCRIPT_DIR}/../references/palette-sync-state.json"
VAULT_NAME="${OBSIDIAN_VAULT:-content}"
MODE="check"
TIMEOUT=600
JSON_OUTPUT=false

usage() {
  cat <<'EOF'
Sync the semantic CSS palette into palette-managed Obsidian Excalidraw drawings.

Usage:
  sync_excalidraw_palette.sh [--check | --apply] [options]

Modes:
  --check          Dry-run and audit only (default). Exits 2 when changes are pending.
  --apply          Apply changed CSS values through the Excalidraw plugin and update sync state.

Options:
  --vault=NAME     Obsidian vault name (default: content or $OBSIDIAN_VAULT).
  --config=PATH    Alternate sync-state JSON, useful for testing.
  --timeout=SEC    Wait timeout for Obsidian (default: 600).
  --json           Print the full JSON report.
  -h, --help       Show this help.

Authoritative palette:
  content/Knowledge/Assets/Styles/concept-visualization-palette.css
EOF
}

for arg in "$@"; do
  case "$arg" in
    --check) MODE="check" ;;
    --apply) MODE="apply" ;;
    --vault=*) VAULT_NAME="${arg#*=}" ;;
    --config=*) CONFIG_PATH="${arg#*=}" ;;
    --timeout=*) TIMEOUT="${arg#*=}" ;;
    --json) JSON_OUTPUT=true ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $arg" >&2; usage >&2; exit 64 ;;
  esac
done

command -v obsidian >/dev/null 2>&1 || { echo "obsidian CLI is not installed or not on PATH" >&2; exit 127; }
[[ -f "$CORE_SCRIPT" ]] || { echo "Missing core script: $CORE_SCRIPT" >&2; exit 66; }
[[ -f "$CONFIG_PATH" ]] || { echo "Missing sync state: $CONFIG_PATH" >&2; exit 66; }
CONFIG_PATH="$(cd "$(dirname "$CONFIG_PATH")" && pwd)/$(basename "$CONFIG_PATH")"
[[ "$TIMEOUT" =~ ^[0-9]+$ ]] || { echo "--timeout must be an integer" >&2; exit 64; }

STAMP="$(date +%s)-$$-$RANDOM"
REPORT_PATH="/tmp/excalidraw-palette-sync-${STAMP}.json"
ERROR_PATH="/tmp/excalidraw-palette-sync-${STAMP}.error"
LAUNCH_LOG="/tmp/excalidraw-palette-sync-${STAMP}.launch.log"
rm -f "$REPORT_PATH" "$ERROR_PATH" "$LAUNCH_LOG"

LAUNCHER="$(python3 - "$CORE_SCRIPT" "$CONFIG_PATH" "$REPORT_PATH" "$ERROR_PATH" "$MODE" <<'PY'
import json,sys
core,config,report,error,mode=sys.argv[1:]
options={"configPath":config,"reportPath":report,"apply":mode=="apply"}
print("(async()=>{try{globalThis.PALETTE_SYNC_OPTIONS="+json.dumps(options,ensure_ascii=False)+";await eval(require('fs').readFileSync("+json.dumps(core)+",'utf8'));}catch(e){require('fs').writeFileSync("+json.dumps(error)+",String(e&&e.stack||e));}finally{delete globalThis.PALETTE_SYNC_OPTIONS;}})()")
PY
)"

if ! obsidian "vault=${VAULT_NAME}" eval "code=${LAUNCHER}" >"$LAUNCH_LOG" 2>&1; then
  echo "Failed to dispatch palette sync to Obsidian:" >&2
  cat "$LAUNCH_LOG" >&2
  exit 1
fi

DEADLINE=$((SECONDS + TIMEOUT))
while [[ ! -f "$REPORT_PATH" && ! -f "$ERROR_PATH" && $SECONDS -lt $DEADLINE ]]; do
  sleep 0.5
done

if [[ -f "$ERROR_PATH" ]]; then
  echo "Palette sync failed:" >&2
  cat "$ERROR_PATH" >&2
  exit 1
fi
if [[ ! -f "$REPORT_PATH" ]]; then
  echo "Palette sync timed out after ${TIMEOUT}s. Is Obsidian open with vault '${VAULT_NAME}'?" >&2
  [[ -s "$LAUNCH_LOG" ]] && cat "$LAUNCH_LOG" >&2
  exit 124
fi

if [[ "$JSON_OUTPUT" == true ]]; then
  cat "$REPORT_PATH"
else
  python3 - "$REPORT_PATH" <<'PY'
import json,sys
r=json.load(open(sys.argv[1]))
print(f"mode: {r['mode']}")
print(f"managed files: {r['managedFiles']}")
print(f"palette roles changed: {len(r['roleChanges'])}")
for x in r['roleChanges']:
    print(f"  {x['role']}: {x['from']} -> {x['to']}")
print(f"files needing write: {r['filesNeedingWrite']}")
print(f"element color fields: {r['plannedElementFields']}")
print(f"SVG image instances: {r['plannedImageInstances']}")
print(f"scene backgrounds: {r['plannedBackgrounds']}")
print(f"applied: {r['applied']}")
print(f"sync state updated: {r['stateUpdated']}")
print(f"report: {sys.argv[1]}")
PY
fi

PENDING="$(python3 - "$REPORT_PATH" <<'PY'
import json,sys
r=json.load(open(sys.argv[1]))
print(1 if r['changesPending'] else 0)
PY
)"
if [[ "$MODE" == "check" && "$PENDING" == 1 ]]; then exit 2; fi
