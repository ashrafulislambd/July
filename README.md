# Bornona IBus

A fixed-layout Bangla input method for Linux, built on [IBus](https://github.com/ibus/ibus),
with a draggable, edge-snapping floating bar — the Bornona layout, in the
spirit of Avro Keyboard, native to Linux.

Full design rationale and architecture decisions live in [`SPEC.md`](./SPEC.md)
and [`tasks/plan.md`](./tasks/plan.md). The Bornona key→glyph mapping itself
is the source of truth in [`Bornona.txt`](./Bornona.txt).

## System dependencies (Debian/Ubuntu)

```
sudo apt install ibus ibus-gtk3 im-config \
    python3-gi gir1.2-ibus-1.0 gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1
```

## Setup

The venv **must** be created with `--system-site-packages` — PyGObject/GTK/
IBus bindings come from system packages and cannot be pip-installed into a
plain venv.

```
python3 -m venv --system-site-packages .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install -e .
```

## Commands

```
Run tests:              .venv/bin/pytest -q
Run tests w/ coverage:  .venv/bin/pytest --cov=bornona_ibus --cov-report=term-missing
Lint:                   .venv/bin/ruff check .
Format:                 .venv/bin/ruff format .
```

## Running it

**Quick local testing** (no system install, no sudo — registers the engine
live over D-Bus against a running `ibus-daemon`):

```
ibus-daemon -x --xim &            # if not already running
scripts/run-dev.sh                # starts the engine
.venv/bin/python3 -m bornona_ibus.floating_bar   # starts the bar
```

**Real, permanent install** (selectable like any other input source, works
in every app, survives logout/login):

```
im-config -n ibus                 # set ibus as your IM framework
scripts/install-dev.sh            # sudo-installs the component descriptor,
                                   # plus autostart entries for the bar and
                                   # a safety-net ibus-daemon launcher
```

Then **log out and log back in** so your session picks up
`GTK_IM_MODULE`/`QT_IM_MODULE`/`XMODIFIERS`. After that, the bar autostarts
and Bornona becomes available with no further steps.

### Why the bar self-selects the engine

Not every desktop runs IBus's own panel/tray switcher — confirmed missing
on plain XFCE, where there'd otherwise be no UI at all to pick "Bornona" as
the active input source. The floating bar calls
`IBus.Bus.set_global_engine_async("bornona")` on startup if it isn't
already active, making the bar itself the one control surface you need —
matching how Avro's floating bar works.

## Project structure

```
Bornona.txt                 Source-of-truth key→glyph mapping
SPEC.md                     Full spec: objective, architecture, boundaries
src/bornona_ibus/
    composer.py              Pure, unit-tested key-composition state machine
    layout_data.py            Bornona key→glyph tables, derived from Bornona.txt
    engine.py                 IBus.Engine wrapper
    main.py                   Entry point / IBus component registration
    ipc.py                    Shared bar<->engine state via IBus Config
    floating_bar/              Draggable/edge-snapping GTK bar, tray, settings
data/bornona.xml.in          IBus component descriptor template
data/autostart/               Autostart .desktop templates (bar, ibus-daemon safety net)
scripts/                     install-dev.sh, run-dev.sh, ensure-ibus-daemon.sh, dev test window
tests/test_composer.py       Composer unit tests (the core test suite)
tasks/                       plan.md, todo.md — implementation plan and task list
```

## Known limitations (v1)

- **Backspace** doesn't undo a previously committed multi-key composition
  glyph-by-glyph — only an as-yet-uncommitted pending key gets cleared;
  otherwise it's forwarded to the application for normal deletion.
- **Wayland**: the floating bar's drag/edge-snap relies on
  `Gtk.Window.move`, which Wayland's security model disallows for regular
  windows. Confirmed working on X11; Wayland is untested/unsupported for
  now.
- Only the fixed Bornona layout ships; the layout data structure is
  designed to be pluggable for a future phonetic mode, but that mode isn't
  built.

## License

MIT — see [`LICENSE`](./LICENSE).
