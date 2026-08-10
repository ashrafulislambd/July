#!/usr/bin/env bash
# Installs the Bornona IBus component descriptor so it's selectable as a
# normal input source from your desktop's input method settings.
#
# NOTE: on this machine's IBus build (Ubuntu-packaged 1.5.29), ibus-daemon
# only scans /usr/share/ibus/component for components — it does NOT scan a
# per-user directory (confirmed by inspecting its registry observed-paths;
# other distros/builds may differ). That means a real install here requires
# root to place the file under /usr/share, which this script does with sudo
# after confirming with you. For quick local testing without touching system
# directories at all, use `scripts/run-dev.sh` instead (registers the engine
# live over D-Bus, no XML install needed).
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$REPO_DIR/.venv/bin/python3"
MAIN="$REPO_DIR/src/bornona_ibus/main.py"
SYSTEM_DEST_DIR="/usr/share/ibus/component"

if [[ ! -x "$PYTHON" ]]; then
    echo "error: $PYTHON not found — create the venv first (see SPEC.md Commands)" >&2
    exit 1
fi

TMP_XML="$(mktemp)"
trap 'rm -f "$TMP_XML"' EXIT
sed "s|@EXEC@|$PYTHON $MAIN --ibus|" "$REPO_DIR/data/bornona.xml.in" > "$TMP_XML"

echo "This will copy the component descriptor to $SYSTEM_DEST_DIR/bornona.xml"
echo "using sudo, then restart ibus-daemon. Continue? [y/N]"
read -r REPLY
if [[ "$REPLY" != "y" && "$REPLY" != "Y" ]]; then
    echo "Aborted. Use scripts/run-dev.sh for testing without a system install."
    exit 0
fi

sudo install -m 644 "$TMP_XML" "$SYSTEM_DEST_DIR/bornona.xml"
echo "Installed to $SYSTEM_DEST_DIR/bornona.xml"

echo "Restarting ibus-daemon..."
ibus-daemon -drx || true

echo "Done. Use ibus-setup (or your desktop's Input Method settings) to add 'Bornona'."
