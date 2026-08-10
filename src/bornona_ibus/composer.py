"""Incremental composer for the Bornona fixed layout.

This module is deliberately free of any IBus/GTK dependency so it can be
unit-tested in isolation (see tests/test_composer.py) and reused by any
front end. IBus delivers one keystroke at a time, so the core primitive is
`step()`: given the currently pending key (if any) and the newly typed key,
it returns the text to commit right now and the new pending state.

The only ambiguity in the Bornona layout is a single key of lookahead: `h`
and `r` each may begin a two-key sequence (independent vowels, র-ফলা, রেফ)
depending on what follows. Everything else resolves in one key.
"""

from __future__ import annotations

from bornona_ibus.layout_data import PENDING_KEYS, SINGLE_KEY, TWO_KEY_SEQUENCES


def step(pending: str | None, key: str) -> tuple[str, str | None]:
    """Process one incoming key given the current pending state.

    Args:
        pending: The previously buffered pending key (``"h"``, ``"r"``, or
            ``None`` if nothing is pending).
        key: The raw key symbol just typed.

    Returns:
        A ``(text_to_commit_now, new_pending_state)`` tuple.
    """
    if pending is not None:
        resolved = TWO_KEY_SEQUENCES.get((pending, key))
        if resolved is not None:
            return resolved, None
        # The new key doesn't resolve the pending one: flush the pending
        # key as its own glyph, then process the new key fresh.
        flushed = SINGLE_KEY.get(pending, pending)
        commit, new_pending = step(None, key)
        return flushed + commit, new_pending

    if key in PENDING_KEYS:
        return "", key

    return SINGLE_KEY.get(key, key), None


def compose(raw_keys: list[str]) -> str:
    """Compose a full raw key sequence into Bangla Unicode text.

    Drives `step()` over the whole sequence and flushes any trailing
    pending key at the end. Intended for tests and other batch use; a live
    IBus engine should call `step()` directly, one key at a time.

    Args:
        raw_keys: Ordered list of raw key symbols typed so far.

    Returns:
        The composed Bangla Unicode string for this key sequence.
    """
    pending: str | None = None
    parts: list[str] = []
    for key in raw_keys:
        text, pending = step(pending, key)
        parts.append(text)
    if pending is not None:
        parts.append(SINGLE_KEY.get(pending, pending))
    return "".join(parts)
