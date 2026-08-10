"""Standalone launcher: `python -m bornona_ibus.floating_bar`.

On startup, ensures Bornona is the active IBus engine (not every desktop
runs IBus's own panel/tray switcher — confirmed missing on XFCE here — so
the bar is the one guaranteed control surface, same as Avro's). Wires the
bar's mode toggle to the IBus engine's live state via the shared
Config-based IPC (see SPEC.md's Architecture Decisions and
`bornona_ibus.ipc`). Requires ibus-daemon to be running.
"""

from __future__ import annotations

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402

from bornona_ibus.floating_bar.bar import FloatingBar  # noqa: E402
from bornona_ibus.floating_bar.tray import TrayIcon  # noqa: E402
from bornona_ibus.ipc import (  # noqa: E402
    ensure_bornona_engine_active,
    get_bus,
    read_bangla_mode,
    write_bangla_mode,
)


def main() -> None:
    bus = get_bus()
    ensure_bornona_engine_active(bus)
    config = bus.get_config()
    initial_mode = read_bangla_mode(config)

    def restore() -> None:
        bar.show_all()
        bar.present()
        tray.hide()

    def minimize() -> None:
        tray.show()

    def quit_app() -> None:
        Gtk.main_quit()

    def mode_toggled(enabled: bool) -> None:
        write_bangla_mode(config, enabled)

    tray = TrayIcon(on_restore=restore, on_quit=quit_app)
    bar = FloatingBar(
        on_minimize=minimize,
        on_quit=quit_app,
        on_mode_toggle=mode_toggled,
        initial_bangla_mode=initial_mode,
    )
    bar.connect("destroy", lambda _w: quit_app())
    bar.show_all()
    bar.move_to_default_position()

    Gtk.main()


if __name__ == "__main__":
    main()
