"""Tray icon for minimizing/restoring the floating bar.

Tries the Ayatana fork of AppIndicator3 first (what's packaged on
Mint/some distros as `gir1.2-ayatanaappindicator3-0.1`), then falls back
to the original AppIndicator3 typelib. Neither ships by default on plain
Ubuntu GNOME, so this must degrade gracefully rather than crash — an
earlier version let an uncaught ImportError here take down the entire
floating bar process before any window could appear (confirmed: engine
worked fine, only the bar failed, on a GNOME machine neither typelib was
installed on).
"""

from __future__ import annotations

import importlib
import sys

import gi

AppIndicator3 = None
for _module_name in ("AyatanaAppIndicator3", "AppIndicator3"):
    try:
        gi.require_version(_module_name, "0.1")
        AppIndicator3 = importlib.import_module(f"gi.repository.{_module_name}")
        break
    except (ValueError, ImportError):
        continue

TRAY_AVAILABLE = AppIndicator3 is not None

APP_ID = "july-ibus"


class TrayIcon:
    """Wraps an AppIndicator that restores the floating bar when clicked.

    If neither AppIndicator3 typelib is available, this becomes an inert
    no-op object instead of raising — `is_available` tells callers whether
    minimize-to-tray actually works, so they can avoid the trap of hiding
    the bar with no way to bring it back.
    """

    def __init__(self, on_restore, on_quit=None):
        self.is_available = TRAY_AVAILABLE
        self._indicator = None
        if not self.is_available:
            print(
                "july: no AppIndicator3/AyatanaAppIndicator3 typelib found; "
                "tray icon disabled, minimize-to-tray unavailable.",
                file=sys.stderr,
            )
            return

        self._on_restore = on_restore
        self._on_quit = on_quit
        try:
            self._indicator = AppIndicator3.Indicator.new(
                APP_ID,
                "input-keyboard",
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
            )
            self._indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
            self._indicator.set_title("July")
            self._indicator.set_menu(self._build_menu())
        except Exception as exc:  # noqa: BLE001 - degrade, don't crash the bar
            print(f"july: tray icon setup failed ({exc}); disabling.", file=sys.stderr)
            self.is_available = False
            self._indicator = None

    def _build_menu(self):
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk

        menu = Gtk.Menu()

        restore_item = Gtk.MenuItem(label="Show July bar")
        restore_item.connect("activate", lambda _item: self._on_restore())
        menu.append(restore_item)

        menu.append(Gtk.SeparatorMenuItem())

        quit_item = Gtk.MenuItem(label="Quit July")
        quit_item.connect("activate", lambda _item: self._on_quit and self._on_quit())
        menu.append(quit_item)

        menu.show_all()
        return menu

    def show(self) -> None:
        if self._indicator is not None:
            self._indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    def hide(self) -> None:
        if self._indicator is not None:
            self._indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
