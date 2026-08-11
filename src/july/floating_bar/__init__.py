"""July floating bar — a draggable, edge-snapping GTK toolbar.

Mirrors Avro Keyboard's floating bar: drag it anywhere, it snaps to the
nearest screen edge on release, and it offers a mode toggle, quick settings,
and minimize-to-tray.
"""

from july.floating_bar.bar import FloatingBar

__all__ = ["FloatingBar"]
