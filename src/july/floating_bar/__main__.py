"""Standalone launcher: `python -m july.floating_bar`.

On startup, ensures the Bornona engine is the active IBus engine (not every desktop
runs IBus's own panel/tray switcher — confirmed missing on XFCE here — so
the bar is the one guaranteed control surface, same as Avro's). Wires the
bar's mode toggle to the IBus engine's live state via the shared
Config-based IPC (see `july.ipc`). Requires ibus-daemon to be running.

The bar window is always constructed and shown first; IBus config/engine
setup happens afterward and is defensive throughout (see `ipc.py`) — a
failure there should degrade functionality, never prevent the window from
appearing. This app is autostarted with no visible terminal, so an
uncaught exception here previously meant total, silent failure: on at
least one real machine (Ubuntu GNOME) the process crashed before showing
any window, with no clue why beyond an opaque OS-level crash notification.
"""

from __future__ import annotations

import sys

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk  # noqa: E402

from july.floating_bar.bar import FloatingBar  # noqa: E402
from july.floating_bar.tray import TrayIcon  # noqa: E402
from july.ipc import (  # noqa: E402
    ensure_bornona_engine_active,
    get_bus,
    read_bangla_mode,
    write_bangla_mode,
)


def main() -> None:
    def restore() -> None:
        bar.show_all()
        bar.present()
        tray.hide()

    def minimize() -> None:
        # Only actually hide if the tray can restore it again — otherwise
        # minimize would trap the user with no way to bring the bar back
        # (see tray.py: not every desktop has a working AppIndicator host).
        if tray.is_available:
            bar.hide()
            tray.show()

    def quit_app() -> None:
        Gtk.main_quit()

    def mode_toggled(enabled: bool) -> None:
        if _config is not None:
            write_bangla_mode(_config, enabled)

    tray = TrayIcon(on_restore=restore, on_quit=quit_app)
    bar = FloatingBar(
        on_minimize=minimize,
        on_quit=quit_app,
        on_mode_toggle=mode_toggled,
        initial_bangla_mode=True,
    )
    bar.connect("destroy", lambda _w: quit_app())
    bar.show_all()
    bar.move_to_default_position()

    # IBus setup runs after the window is already up, so any failure here
    # only degrades functionality (manual engine selection, mode always
    # starting as Bangla-on) rather than hiding the whole app.
    _config = None
    try:
        bus = get_bus()
        ensure_bornona_engine_active(bus)
        _config = bus.get_config()
        bar.set_bangla_mode(read_bangla_mode(_config))
    except GLib.Error as exc:
        print(f"july: IBus setup failed, continuing without it: {exc}", file=sys.stderr)

    Gtk.main()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Autostarted with no visible terminal: an uncaught exception here
        # otherwise vanishes silently (or, on distros with apport enabled,
        # surfaces only as an opaque "System problem detected" popup with
        # no clue which app or why). Print a real traceback to stderr,
        # which systemd/journalctl or ~/.xsession-errors will capture.
        import traceback

        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
