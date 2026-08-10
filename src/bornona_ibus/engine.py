"""IBus engine wrapper around the Bornona composer.

Bridges raw IBus key events to `composer.step()` and commits the resulting
text. Contains no layout knowledge itself — all mapping rules live in
`layout_data.py` / `composer.py`, which stay unit-testable without a running
IBus session.

Known v1 limitation (documented, not accidental): Backspace does not undo a
previously *committed* multi-key composition (e.g. an independent vowel
formed from ``h``+vowel) glyph-by-glyph — it only clears an as-yet-uncommitted
pending key, otherwise it is forwarded to the application for normal
single-character deletion.
"""

from __future__ import annotations

import gi

gi.require_version("IBus", "1.0")
from gi.repository import GObject, IBus  # noqa: E402

from bornona_ibus.composer import step  # noqa: E402
from bornona_ibus.layout_data import SINGLE_KEY  # noqa: E402

# Printable ASCII range that Bornona keys live in (space through tilde).
_PRINTABLE_MIN = 0x20
_PRINTABLE_MAX = 0x7E

# Modifiers that, when held, mean "not a layout keystroke" (e.g. Ctrl+C).
_BYPASS_MODIFIERS = (
    IBus.ModifierType.CONTROL_MASK
    | IBus.ModifierType.MOD1_MASK  # Alt
    | IBus.ModifierType.SUPER_MASK
)

# Bare modifier keysyms fire their own key-press events (e.g. pressing Shift
# before a shifted letter delivers a Shift_L press first). These carry no
# character and must be ignored outright — NOT treated as "some other key"
# that would flush pending state, or Shift+<vowel> sequences like h+E/h+R/h+O
# break (the Shift_L press flushes `h` before the real letter arrives).
_MODIFIER_KEYVALS = frozenset(
    {
        IBus.KEY_Shift_L,
        IBus.KEY_Shift_R,
        IBus.KEY_Control_L,
        IBus.KEY_Control_R,
        IBus.KEY_Alt_L,
        IBus.KEY_Alt_R,
        IBus.KEY_Super_L,
        IBus.KEY_Super_R,
        IBus.KEY_Meta_L,
        IBus.KEY_Meta_R,
        IBus.KEY_Caps_Lock,
        IBus.KEY_Shift_Lock,
        IBus.KEY_ISO_Level3_Shift,
    }
)


class BornonaEngine(IBus.Engine):
    """IBus engine implementing the Bornona fixed Bangla layout."""

    __gtype_name__ = "BornonaEngine"

    def __init__(self):
        super().__init__()
        self._pending: str | None = None

    def _flush_pending(self) -> None:
        """Commit any buffered pending key as its own glyph and clear it."""
        if self._pending is not None:
            glyph = SINGLE_KEY.get(self._pending, self._pending)
            self.commit_text(IBus.Text.new_from_string(glyph))
            self._pending = None

    def do_process_key_event(self, keyval: int, keycode: int, state: int) -> bool:
        # Ignore key-release events; only act on key-press.
        if state & IBus.ModifierType.RELEASE_MASK:
            return False

        # Bare modifier presses (Shift, Ctrl, ...) carry no character and
        # must not disturb pending composition state.
        if keyval in _MODIFIER_KEYVALS:
            return False

        # Let bypass-modified combinations (Ctrl/Alt/Super) through untouched,
        # after flushing any pending composition state first.
        if state & _BYPASS_MODIFIERS:
            self._flush_pending()
            return False

        # Backspace: clear an uncommitted pending key without deleting
        # anything; otherwise let the application handle deletion normally.
        if keyval == IBus.KEY_BackSpace:
            if self._pending is not None:
                self._pending = None
                return True
            return False

        # Only printable ASCII keys are part of the Bornona layout; for
        # IBus/X11 keysyms in this range, keyval equals the character's
        # Unicode code point.
        if _PRINTABLE_MIN <= keyval <= _PRINTABLE_MAX:
            key = chr(keyval)
            text, self._pending = step(self._pending, key)
            if text:
                self.commit_text(IBus.Text.new_from_string(text))
            return True

        # Any other key (Enter, Tab, arrows, function keys, ...): flush
        # pending state first, then let the application handle the key.
        self._flush_pending()
        return False

    def do_reset(self) -> None:
        self._pending = None

    def do_focus_out(self) -> None:
        self._pending = None


GObject.type_register(BornonaEngine)
