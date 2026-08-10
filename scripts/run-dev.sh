#!/usr/bin/env bash
# Runs the Bornona engine in standalone dev mode: registers itself directly
# against a running ibus-daemon over D-Bus and switches to it immediately.
# No component XML installation needed — this is the fast path for local
# development and manual testing (see SPEC.md Testing Strategy).
#
# Requires ibus-daemon to already be running (e.g. `ibus-daemon -x --xim &`).
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "$REPO_DIR/.venv/bin/python3" "$REPO_DIR/src/bornona_ibus/main.py"
