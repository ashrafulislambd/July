"""The draggable, edge-snapping floating bar window.

Known limitation (X11 only): dragging/snapping relies on the window
manager honoring client-requested absolute window positions
(`Gtk.Window.move`). Wayland's security model disallows this for regular
top-level windows, so drag/snap will not work under a Wayland session —
a known, deliberate limitation (see README.md), not silently broken.
"""

from __future__ import annotations

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, Gtk  # noqa: E402

from july.floating_bar.guide import build_guide_window  # noqa: E402

# Snapping is a magnet effect, not unconditional: the bar only jumps to an
# edge when dropped within this many pixels of it. Drop it further from any
# edge (e.g. mid-screen) and it just stays where you left it.
_SNAP_THRESHOLD = 40

_CSS = b"""
window.july-bar {
    background-color: rgba(46, 52, 64, 0.96);
    border-radius: 10px;
}
.july-bar-handle {
    color: alpha(#ffffff, 0.35);
    font-size: 10px;
}
.july-bar-btn {
    background: transparent;
    border: none;
    border-radius: 6px;
    color: #eceff4;
    padding: 4px 8px;
    min-width: 0;
    font-size: 14px;
}
.july-bar-btn:hover {
    background-color: alpha(#ffffff, 0.14);
}
"""


class FloatingBar(Gtk.Window):
    """A small always-on-top bar: mode toggle, user guide, minimize-to-tray."""

    def __init__(
        self, on_minimize=None, on_quit=None, on_mode_toggle=None, initial_bangla_mode=True
    ):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self._on_minimize = on_minimize
        self._on_quit = on_quit
        self._on_mode_toggle = on_mode_toggle
        self._dragging = False
        self._drag_offset = (0, 0)
        self._bangla_mode = initial_bangla_mode
        self._guide_window = None

        self.set_decorated(False)
        self.set_resizable(False)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_title("July")
        self.get_style_context().add_class("july-bar")

        self._apply_css()
        self._enable_transparency()
        self._build_ui()
        self._build_context_menu()
        self._wire_drag_events()

    def _apply_css(self) -> None:
        provider = Gtk.CssProvider()
        provider.load_from_data(_CSS)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def _enable_transparency(self) -> None:
        # Needed so the CSS border-radius actually shows rounded corners
        # instead of a rounded rect painted on an opaque rectangle. Do NOT
        # set app-paintable here: that disables GTK's normal CSS background
        # painting entirely (it means "I'll draw the background myself"),
        # which left this window with a black backdrop and visible
        # bleed-through of whatever was on screen underneath it.
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual is not None and screen.is_composited():
            self.set_visual(visual)

    def _build_ui(self) -> None:
        outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        outer.set_border_width(5)
        self.add(outer)

        handle = Gtk.Label(label="⋮⋮")
        handle.get_style_context().add_class("july-bar-handle")
        handle.set_margin_start(2)
        handle.set_margin_end(4)
        outer.pack_start(handle, False, False, 0)

        self._mode_button = self._make_button(
            "বা" if self._bangla_mode else "EN", "Toggle Bangla/English"
        )
        self._mode_button.connect("clicked", self._handle_mode_button_clicked)
        outer.pack_start(self._mode_button, False, False, 0)

        guide_button = self._make_button("?", "User guide (বাংলা / English)")
        guide_button.connect("clicked", self._on_guide_clicked)
        outer.pack_start(guide_button, False, False, 0)

        minimize_button = self._make_button("—", "Minimize to tray")
        minimize_button.connect("clicked", self._on_minimize_clicked)
        outer.pack_start(minimize_button, False, False, 0)

    def _make_button(self, label: str, tooltip: str) -> Gtk.Button:
        button = Gtk.Button(label=label)
        button.set_tooltip_text(tooltip)
        button.set_relief(Gtk.ReliefStyle.NONE)
        button.get_style_context().add_class("july-bar-btn")
        return button

    def _build_context_menu(self) -> None:
        menu = Gtk.Menu()
        quit_item = Gtk.MenuItem(label="Quit July")
        quit_item.connect("activate", lambda _item: self._quit())
        menu.append(quit_item)
        menu.show_all()
        self._context_menu = menu

    def _handle_mode_button_clicked(self, _button: Gtk.Button) -> None:
        self._bangla_mode = not self._bangla_mode
        self._mode_button.set_label("বা" if self._bangla_mode else "EN")
        if self._on_mode_toggle is not None:
            self._on_mode_toggle(self._bangla_mode)

    def set_bangla_mode(self, enabled: bool) -> None:
        """Update the displayed mode without triggering `on_mode_toggle`.

        Used to reflect the real persisted state once it's known (IBus
        setup happens after the window is already shown — see
        `floating_bar/__main__.py`), without re-writing it right back to
        config as if the user had clicked the button.
        """
        self._bangla_mode = enabled
        self._mode_button.set_label("বা" if self._bangla_mode else "EN")

    def _on_guide_clicked(self, _button: Gtk.Button) -> None:
        if self._guide_window is None:
            self._guide_window = build_guide_window(bangla_initial=self._bangla_mode)
            self._guide_window.connect("delete-event", self._on_guide_window_closed)
        self._guide_window.show_all()
        self._guide_window.present()

    def _on_guide_window_closed(self, window: Gtk.Window, _event) -> bool:
        window.destroy()
        self._guide_window = None
        return True

    def _on_minimize_clicked(self, _button: Gtk.Button) -> None:
        # Hiding is the caller's call, not ours: if there's no working tray
        # to restore from, hiding here would trap the user with no way to
        # bring the bar back.
        if self._on_minimize is not None:
            self._on_minimize()

    def _quit(self) -> None:
        if self._on_quit is not None:
            self._on_quit()

    # -- Dragging + edge snapping -------------------------------------

    def _wire_drag_events(self) -> None:
        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK
            | Gdk.EventMask.BUTTON_RELEASE_MASK
            | Gdk.EventMask.POINTER_MOTION_MASK
        )
        self.connect("button-press-event", self._on_button_press)
        self.connect("motion-notify-event", self._on_motion_notify)
        self.connect("button-release-event", self._on_button_release)

    def _on_button_press(self, _widget, event) -> bool:
        if event.button == 3:
            self._context_menu.popup_at_pointer(event)
            return True
        if event.button != 1:
            return False
        win_x, win_y = self.get_position()
        self._dragging = True
        self._drag_offset = (event.x_root - win_x, event.y_root - win_y)
        return False

    def _on_motion_notify(self, _widget, event) -> bool:
        if not self._dragging:
            return False
        offset_x, offset_y = self._drag_offset
        raw_x = int(event.x_root - offset_x)
        raw_y = int(event.y_root - offset_y)
        # Snap live, while the button is still held — a magnet effect, not
        # just a settle-on-release. Matches Avro's floating bar feel: you
        # can feel it catch on an edge as you drag past it.
        snapped_x, snapped_y = self._compute_snapped_position(raw_x, raw_y)
        self.move(snapped_x, snapped_y)
        return False

    def _on_button_release(self, _widget, event) -> bool:
        if event.button != 1 or not self._dragging:
            return False
        self._dragging = False
        # Final settle — normally a no-op since motion already kept it
        # snapped, but covers the case of a release with no motion events.
        win_x, win_y = self.get_position()
        new_x, new_y = self._compute_snapped_position(win_x, win_y)
        self.move(new_x, new_y)
        return False

    def _compute_snapped_position(self, raw_x: int, raw_y: int) -> tuple[int, int]:
        """Given a candidate top-left position, apply edge magnetism.

        Clamps the bar to stay fully on-screen, and snaps whichever axis is
        within `_SNAP_THRESHOLD` pixels of its nearest monitor edge flush
        against that edge.
        """
        geometry = self._monitor_geometry()
        if geometry is None:
            return raw_x, raw_y
        mon_x, mon_y, mon_w, mon_h = geometry
        win_w, win_h = self.get_size()

        dist_left = raw_x - mon_x
        dist_right = (mon_x + mon_w) - (raw_x + win_w)
        dist_top = raw_y - mon_y
        dist_bottom = (mon_y + mon_h) - (raw_y + win_h)

        new_x = min(max(raw_x, mon_x), mon_x + mon_w - win_w)
        new_y = min(max(raw_y, mon_y), mon_y + mon_h - win_h)

        nearest = min(dist_left, dist_right, dist_top, dist_bottom)
        if nearest <= _SNAP_THRESHOLD:
            if nearest == dist_left:
                new_x = mon_x
            elif nearest == dist_right:
                new_x = mon_x + mon_w - win_w
            elif nearest == dist_top:
                new_y = mon_y
            else:
                new_y = mon_y + mon_h - win_h

        return new_x, new_y

    def move_to_default_position(self) -> None:
        """Place the bar pre-snapped to the top edge, right-of-center.

        Top edge is fully flush (snapped); horizontally it sits at ~75% of
        the monitor width rather than jammed into the exact corner, which
        tends to overlap other windows' minimize/maximize/close buttons.

        Must be called after the window is realized/allocated (e.g. right
        after `show_all()`) so `get_size()` reflects the real bar size.
        """
        geometry = self._monitor_geometry()
        if geometry is None:
            return
        mon_x, mon_y, mon_w, _mon_h = geometry
        win_w, _win_h = self.get_size()
        target_x = mon_x + int(mon_w * 0.75) - win_w // 2
        target_x = min(max(target_x, mon_x), mon_x + mon_w - win_w)
        self.move(target_x, mon_y)

    def _monitor_geometry(self) -> tuple[int, int, int, int] | None:
        gdk_window = self.get_window()
        display = Gdk.Display.get_default()
        if display is None:
            return None
        if gdk_window is not None:
            monitor = display.get_monitor_at_window(gdk_window)
        else:
            monitor = display.get_primary_monitor() or display.get_monitor(0)
        if monitor is None:
            return None
        rect = monitor.get_geometry()
        return rect.x, rect.y, rect.width, rect.height
