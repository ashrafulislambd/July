"""Minimal quick-settings popover for the floating bar.

v1 content is intentionally small (current mode + version) — structured as
its own function so real settings (layout selection, fonts, etc.) can be
added later without touching bar.py's layout code.
"""

from __future__ import annotations

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402

_VERSION = "0.2.0"


def build_settings_popover(relative_to: Gtk.Widget) -> Gtk.Popover:
    """Build the quick-settings popover attached to the bar's settings button.

    Args:
        relative_to: The widget the popover is anchored to (unused directly
            here — Gtk.MenuButton handles anchoring itself — kept for a
            future version that may need it for custom placement).

    Returns:
        A populated, not-yet-shown Gtk.Popover.
    """
    popover = Gtk.Popover()

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    box.set_border_width(10)
    popover.add(box)

    title = Gtk.Label(label="July (Bornona layout)")
    title.set_xalign(0)
    box.pack_start(title, False, False, 0)

    version_label = Gtk.Label(label=f"Version {_VERSION}")
    version_label.set_xalign(0)
    box.pack_start(version_label, False, False, 0)

    note = Gtk.Label(label="More settings coming soon.")
    note.set_xalign(0)
    note.get_style_context().add_class("dim-label")
    box.pack_start(note, False, False, 0)

    box.show_all()
    return popover
