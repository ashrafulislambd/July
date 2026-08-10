"""Standalone launcher: `python -m bornona_ibus.floating_bar`.

Runs the floating bar with its tray minimize/restore wired up, independent
of the IBus engine (see SPEC.md's Architecture Decisions for why the bar
and engine are separate processes, coordinated only via IBus's Config API —
that wiring is Task 10, not needed for the bar to be usable standalone).
"""

from __future__ import annotations

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402

from bornona_ibus.floating_bar.bar import FloatingBar  # noqa: E402
from bornona_ibus.floating_bar.tray import TrayIcon  # noqa: E402


def main() -> None:
    def restore() -> None:
        bar.show_all()
        bar.present()
        tray.hide()

    def minimize() -> None:
        tray.show()

    def quit_app() -> None:
        Gtk.main_quit()

    tray = TrayIcon(on_restore=restore, on_quit=quit_app)
    bar = FloatingBar(on_minimize=minimize, on_quit=quit_app)
    bar.connect("destroy", lambda _w: quit_app())
    bar.show_all()
    bar.move_to_default_position()

    Gtk.main()


if __name__ == "__main__":
    main()
