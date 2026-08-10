#!/usr/bin/env python3
"""Entry point for the Bornona IBus engine.

Run with ``--ibus`` when spawned by ibus-daemon (the normal case, driven by
the ``<exec>`` line in the installed component XML — see
``data/bornona.xml.in`` and ``scripts/install-dev.sh``). Run with no
arguments for a quick standalone sanity check that registers the engine
directly against a running ibus-daemon, without needing the component XML
installed.
"""

from __future__ import annotations

import argparse
import sys

import gi

gi.require_version("IBus", "1.0")
from gi.repository import IBus  # noqa: E402

from bornona_ibus.engine import BornonaEngine  # noqa: E402

COMPONENT_NAME = "org.freedesktop.IBus.Bornona"
ENGINE_NAME = "bornona"


def main() -> None:
    parser = argparse.ArgumentParser(description="Bornona IBus engine")
    parser.add_argument(
        "--ibus",
        action="store_true",
        help="Run connected to ibus-daemon (spawned via the component XML's <exec>)",
    )
    args = parser.parse_args()

    IBus.init()
    bus = IBus.Bus()
    if not bus.is_connected():
        print("Could not connect to ibus-daemon; is it running?", file=sys.stderr)
        sys.exit(1)

    factory = IBus.Factory.new(bus.get_connection())
    factory.add_engine(ENGINE_NAME, BornonaEngine)

    if args.ibus:
        # ibus-daemon already knows about this component from the installed
        # XML; just claim the well-known bus name so it can find us.
        bus.request_name(COMPONENT_NAME, 0)
    else:
        # Standalone dev mode: register the component ourselves and switch
        # to it immediately, without needing the XML installed first.
        component = IBus.Component.new(
            COMPONENT_NAME,
            "Bornona Bangla input method (dev mode)",
            "0.1.0",
            "MIT",
            "Bornona IBus project",
            "",
            "",
            "ibus-bornona",
        )
        engine_desc = IBus.EngineDesc.new(
            ENGINE_NAME,
            "Bornona (Bangla)",
            "Bornona fixed-layout Bangla input method",
            "bn",
            "MIT",
            "Bornona IBus project",
            "input-keyboard",
            "us",
        )
        component.add_engine(engine_desc)
        bus.register_component(component)
        bus.set_global_engine_async(ENGINE_NAME, -1, None, None, None)

    IBus.main()


if __name__ == "__main__":
    main()
