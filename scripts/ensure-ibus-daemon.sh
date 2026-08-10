#!/usr/bin/env bash
# Safety-net for autostart: only starts ibus-daemon if one isn't already
# running. im-config's session wiring normally starts it; this covers
# session managers that don't route through that pipeline.
pgrep -x ibus-daemon >/dev/null || ibus-daemon -drx --xim
