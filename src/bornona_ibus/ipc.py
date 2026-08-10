"""Shared bar <-> engine coordination via IBus's own Config service.

Per SPEC.md's Architecture Decisions: both the floating bar and the engine
already talk to IBus over D-Bus, so we reuse `IBus.Bus.get_config()` as the
IPC channel for shared state instead of inventing a bespoke one. Currently
the only shared state is the Bangla-on/off mode flag.
"""

from __future__ import annotations

import gi

gi.require_version("IBus", "1.0")
from gi.repository import GLib, IBus  # noqa: E402

CONFIG_SECTION = "engine/bornona"
# Lowercase by convention, not just style: IBus's config backend
# (GSettings/dconf-based) lowercases key names in its "value-changed"
# signal even though get_value/set_value accept any case — using a
# lowercase key from the start avoids a signal-vs-storage case mismatch.
CONFIG_KEY_MODE = "mode"


def get_config() -> IBus.Config:
    """Connect to ibus-daemon and return its Config service proxy."""
    IBus.init()
    bus = IBus.Bus()
    return bus.get_config()


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
