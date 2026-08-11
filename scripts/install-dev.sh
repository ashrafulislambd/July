#!/usr/bin/env bash
# Installs the July IBus component descriptor (Bornona layout) so it's
# selectable as a normal input source, plus autostart entries for the
# floating bar and a safety-net ibus-daemon launcher.
#
# NOTE: on this machine's IBus build (Ubuntu-packaged 1.5.29), ibus-daemon
# only scans /usr/share/ibus/component for components — it does NOT scan a
# per-user directory (confirmed by inspecting its registry observed-paths;
# other distros/builds may differ). That means a real install here requires
# root to place the file under /usr/share, which this script does with sudo
# after confirming with you. For quick local testing without touching system
# directories at all, use `scripts/run-dev.sh` instead (registers the engine
# live over D-Bus, no XML install needed).
#
# Also run `im-config -n ibus` yourself (not done here — it changes your
# session-wide input method framework, which is your call) and log out and
# back in afterwards so GTK_IM_MODULE/QT_IM_MODULE/XMODIFIERS get exported.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$REPO_DIR/.venv/bin/python3"
MAIN="$REPO_DIR/src/july/main.py"
SYSTEM_DEST_DIR="/usr/share/ibus/component"
AUTOSTART_DIR="$HOME/.config/autostart"

if [[ ! -x "$PYTHON" ]]; then
    echo "error: $PYTHON not found — create the venv first (see README.md Setup)" >&2
    exit 1
fi

TMP_XML="$(mktemp)"
trap 'rm -f "$TMP_XML"' EXIT
sed "s|@EXEC@|$PYTHON $MAIN --ibus|" "$REPO_DIR/data/july.xml.in" > "$TMP_XML"

echo "This will:"
echo "  1. sudo-copy the component descriptor to $SYSTEM_DEST_DIR/july.xml"
echo "  2. restart ibus-daemon"
echo "  3. install autostart entries to $AUTOSTART_DIR"
echo "Continue? [y/N]"
read -r REPLY
if [[ "$REPLY" != "y" && "$REPLY" != "Y" ]]; then
    echo "Aborted. Use scripts/run-dev.sh for testing without a system install."
    exit 0
fi

sudo install -m 644 "$TMP_XML" "$SYSTEM_DEST_DIR/july.xml"
echo "Installed to $SYSTEM_DEST_DIR/july.xml"

echo "Restarting ibus-daemon..."
ibus-daemon -drx || true

mkdir -p "$AUTOSTART_DIR"
sed "s|@VENV_PYTHON@|$PYTHON|" \
    "$REPO_DIR/data/autostart/july-floating-bar.desktop.in" \
    > "$AUTOSTART_DIR/july-floating-bar.desktop"
sed "s|@ENSURE_SCRIPT@|$REPO_DIR/scripts/ensure-ibus-daemon.sh|" \
    "$REPO_DIR/data/autostart/july-ibus-daemon.desktop.in" \
    > "$AUTOSTART_DIR/july-ibus-daemon.desktop"
echo "Installed autostart entries to $AUTOSTART_DIR"

echo
echo "Done. Remaining manual steps:"
echo "  1. Run: im-config -n ibus   (sets ibus as your input method framework)"
echo "  2. Log out and log back in (needed for GTK_IM_MODULE etc. to apply)"
echo "  3. The floating bar will autostart and select Bornona automatically."
