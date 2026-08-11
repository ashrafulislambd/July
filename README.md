# July

A Bangla input method for Linux, built on [IBus](https://github.com/ibus/ibus),
with a draggable, edge-snapping floating bar in the spirit of Avro Keyboard.
July ships the fixed-layout **Bornona** keyboard mapping — July is the
project/product name, Bornona is the layout it types with (and a design
that leaves room for other layouts later).

Full design rationale and architecture decisions live in [`SPEC.md`](./SPEC.md)
and [`tasks/plan.md`](./tasks/plan.md). The Bornona key→glyph mapping itself
is the source of truth in [`Bornona.txt`](./Bornona.txt), and is also
browsable live from the floating bar's "?" user guide button (বাংলা/English
toggle).

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
Run tests w/ coverage:  .venv/bin/pytest --cov=july --cov-report=term-missing
Lint:                   .venv/bin/ruff check .
Format:                 .venv/bin/ruff format .
```

## Running it

**Quick local testing** (no system install, no sudo — registers the engine
live over D-Bus against a running `ibus-daemon`):

```
ibus-daemon -x --xim &            # if not already running
scripts/run-dev.sh                # starts the engine
.venv/bin/python3 -m july.floating_bar   # starts the bar
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
and the Bornona engine becomes available with no further steps.

For an actual one-click end-user install, build the `.deb` — see
[Packaging](#packaging) below.

### Why the bar self-selects the engine

Not every desktop runs IBus's own panel/tray switcher — confirmed missing
on plain XFCE, where there'd otherwise be no UI at all to pick Bornona as
the active input source. The floating bar calls
`IBus.Bus.set_global_engine_async("bornona")` on startup if it isn't
already active, making the bar itself the one control surface you need —
matching how Avro's floating bar works.

## Packaging

A `.deb` gives end users a real one-click install (double-click → Software
Center/gdebi → Install; `apt` pulls in all dependencies automatically).

```
sudo apt install debhelper dh-python python3-all pybuild-plugin-pyproject
dpkg-buildpackage -us -uc -b
```

Produces `../july-ibus_<version>_all.deb` one directory up from the repo
root. Installs to system Python (`/usr/lib/python3/dist-packages/july/`, no
bundled venv), registers the IBus component, and installs autostart entries
system-wide to `/etc/xdg/autostart/` (covers every user on the machine, not
just the one who installed it). See `debian/` for the packaging source.

## Project structure

```
Bornona.txt                 Source-of-truth key→glyph mapping
SPEC.md                     Full spec: objective, architecture, boundaries
src/july/
    composer.py              Pure, unit-tested key-composition state machine
    layout_data.py            Bornona key→glyph tables, derived from Bornona.txt
    engine.py                 IBus.Engine wrapper (BornonaEngine)
    main.py                   Entry point / IBus component registration
    ipc.py                    Shared bar<->engine state via IBus Config
    floating_bar/              Draggable/edge-snapping GTK bar, tray, settings, guide
data/july.xml.in             IBus component descriptor template
data/autostart/               Autostart .desktop templates (bar, ibus-daemon safety net)
scripts/                     install-dev.sh, run-dev.sh, ensure-ibus-daemon.sh, dev test window
debian/                      .deb packaging (see Packaging above)
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
- No AppIndicator3/AyatanaAppIndicator3 typelib on the system (e.g. plain
  Ubuntu GNOME) means minimize-to-tray is unavailable — the bar detects
  this and disables it rather than failing to start.

## License

MIT — see [`LICENSE`](./LICENSE).
