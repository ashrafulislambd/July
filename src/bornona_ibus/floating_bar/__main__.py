"""Standalone launcher: `python -m bornona_ibus.floating_bar`.

Wires the bar's mode toggle to the IBus engine's live state via the shared
Config-based IPC (see SPEC.md's Architecture Decisions and
`bornona_ibus.ipc`). Requires ibus-daemon to be running; if the engine
isn't also running, toggling still writes the config value correctly, it
just won't affect anything until the engine is.
"""

from __future__ import annotations

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402

from bornona_ibus.floating_bar.bar import FloatingBar  # noqa: E402
from bornona_ibus.floating_bar.tray import TrayIcon  # noqa: E402
from bornona_ibus.ipc import get_config, read_bangla_mode, write_bangla_mode  # noqa: E402


def main() -> None:
    config = get_config()
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
