"""Tray icon for minimizing/restoring the floating bar.

Tries the Ayatana fork of AppIndicator3 first (what's packaged on this
machine — `gir1.2-ayatanaappindicator3-0.1`), then falls back to the
original AppIndicator3 typelib for portability across distros.
"""

from __future__ import annotations

import gi

try:
    gi.require_version("AyatanaAppIndicator3", "0.1")
    from gi.repository import AyatanaAppIndicator3 as AppIndicator3
except (ValueError, ImportError):
    gi.require_version("AppIndicator3", "0.1")
    from gi.repository import AppIndicator3  # type: ignore[no-redef]

APP_ID = "bornona-ibus"


class TrayIcon:
    """Wraps an AppIndicator that restores the floating bar when clicked."""

    def __init__(self, on_restore, on_quit=None):
        self._on_restore = on_restore
        self._on_quit = on_quit
        self._indicator = AppIndicator3.Indicator.new(
            APP_ID,
            "input-keyboard",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )
        self._indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
        self._indicator.set_title("Bornona")

        menu = self._build_menu()
        self._indicator.set_menu(menu)

    def _build_menu(self):
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk

        menu = Gtk.Menu()

        restore_item = Gtk.MenuItem(label="Show Bornona bar")
        restore_item.connect("activate", lambda _item: self._on_restore())
        menu.append(restore_item)

        menu.append(Gtk.SeparatorMenuItem())

        quit_item = Gtk.MenuItem(label="Quit Bornona")
        quit_item.connect("activate", lambda _item: self._on_quit and self._on_quit())
        menu.append(quit_item)

        menu.show_all()
        return menu

    def show(self) -> None:
        self._indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    def hide(self) -> None:
        self._indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
