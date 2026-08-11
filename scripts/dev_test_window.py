#!/usr/bin/env python3
"""Throwaway GTK window for manually testing the July (Bornona) IBus engine.

Not part of the shipped product — a Phase 2 verification aid only. Launch
with GTK_IM_MODULE=ibus so this window (and only this window) routes
keystrokes through IBus, then type into the text view and compare against
Bornona.txt.
"""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402


def main():
    win = Gtk.Window(title="July dev test window (Bornona layout)")
    win.set_default_size(500, 200)
    win.connect("destroy", Gtk.main_quit)

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    box.set_border_width(12)
    win.add(box)

    label = Gtk.Label(label="Type here — this routes through IBus (bornona engine):")
    label.set_xalign(0)
    box.pack_start(label, False, False, 0)

    textview = Gtk.TextView()
    textview.set_wrap_mode(Gtk.WrapMode.WORD)
    scroller = Gtk.ScrolledWindow()
    scroller.add(textview)
    box.pack_start(scroller, True, True, 0)

    win.show_all()
    textview.grab_focus()
    Gtk.main()


if __name__ == "__main__":
    main()
