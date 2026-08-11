"""Shared bar <-> engine coordination via IBus's own Config service.

Per SPEC.md's Architecture Decisions: both the floating bar and the engine
already talk to IBus over D-Bus, so we reuse `IBus.Bus.get_config()` as the
IPC channel for shared state instead of inventing a bespoke one. Currently
the only shared state is the Bangla-on/off mode flag.
"""

from __future__ import annotations

import sys

import gi

gi.require_version("IBus", "1.0")
from gi.repository import GLib, IBus  # noqa: E402

CONFIG_SECTION = "engine/bornona"
# Lowercase by convention, not just style: IBus's config backend
# (GSettings/dconf-based) lowercases key names in its "value-changed"
# signal even though get_value/set_value accept any case — using a
# lowercase key from the start avoids a signal-vs-storage case mismatch.
CONFIG_KEY_MODE = "mode"

ENGINE_NAME = "bornona"


def get_bus() -> IBus.Bus:
    """Connect to ibus-daemon and return the Bus proxy."""
    IBus.init()
    return IBus.Bus()


def get_config() -> IBus.Config:
    """Connect to ibus-daemon and return its Config service proxy."""
    return get_bus().get_config()


def ensure_bornona_engine_active(bus: IBus.Bus | None = None) -> None:
    """Make Bornona the active IBus engine, selecting it if it isn't.

    Not every desktop runs IBus's own panel/tray switcher (confirmed
    missing on this machine's XFCE session), so there may be no other way
    for the user to select Bornona as an input source at all. The floating
    bar calls this on startup so it works as the single control surface,
    the same way Avro's floating bar does — no separate system switcher
    required.
    """
    bus = bus or get_bus()
    try:
        current = bus.get_global_engine()
    except GLib.Error:
        # Some IBus setups raise here (rather than returning None) when no
        # global engine has ever been set on this machine — a fresh
        # install, most likely. Treat it the same as "nothing set yet".
        current = None
    if current is not None and current.get_name() == ENGINE_NAME:
        return
    try:
        bus.set_global_engine_async(ENGINE_NAME, -1, None, None, None)
    except GLib.Error as exc:
        # Never let engine auto-selection take the whole bar down with it —
        # worst case the user selects Bornona manually, same as before this
        # existed.
        print(f"july: could not set Bornona as active engine: {exc}", file=sys.stderr)


def read_bangla_mode(config: IBus.Config, default: bool = True) -> bool:
    """Read the current Bangla-mode flag from IBus config.

    Args:
        config: The IBus Config service proxy (see `get_config`).
        default: Value to use if nothing has been stored yet.

    Returns:
        True if Bangla composition should be active, False for passthrough.
    """
    variant = config.get_value(CONFIG_SECTION, CONFIG_KEY_MODE)
    if variant is None:
        return default
    return bool(variant.get_boolean())


def write_bangla_mode(config: IBus.Config, enabled: bool) -> None:
    """Persist the Bangla-mode flag to IBus config."""
    config.set_value(CONFIG_SECTION, CONFIG_KEY_MODE, GLib.Variant.new_boolean(enabled))
