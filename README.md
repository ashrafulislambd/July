<div align="center">

# 🇧🇩 July

### Type Bangla on Linux the way it should feel — fast, native, and always one click away.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-FCC624?logo=linux&logoColor=black)](#-install)
[![Built on IBus](https://img.shields.io/badge/built%20on-IBus-6E4C1E)](https://github.com/ibus/ibus)

</div>

---

Windows Bangla typists have had Avro Keyboard for years — a floating bar,
a familiar layout, type-and-forget-about-it simplicity. **Linux never had
its own version of that feeling. July is it.**

July is a native Linux input method: a real IBus engine under the hood, a
small floating control bar on top, and the **Bornona** keyboard layout
doing the typing. Install it, log in, and Bangla just works — in your
browser, your terminal, your editor, everywhere.

## ✨ Why you'll like it

- 🪶 **It just works, everywhere.** Any IBus-aware app — browser, terminal,
  editor, chat client — gets correct Bangla the moment you type. No
  per-app configuration.
- 🎯 **A bar that stays out of your way.** Drag it anywhere, it snaps to
  the nearest edge as you let go. Minimize it to the tray when you don't
  need it.
- 🔤 **One click to switch languages.** বাংলা ⇄ EN, live, mid-sentence,
  no restart.
- 📖 **Never forget a key.** Tap **"?"** on the bar for the full Bornona
  key guide, right there, in বাংলা or English.
- 🧠 **No setup gymnastics.** The bar makes itself the active input
  method automatically — even on desktops with no built-in IBus switcher.
- ⚡ **Built for real typing speed.** Every key composes instantly; no
  lag waiting on the next keystroke to "confirm" what you just typed.

## 📦 Install

The easiest path — download the `.deb`, install it, done:

```bash
sudo apt install ./july-ibus_<version>_all.deb
```

`apt` pulls in everything else it needs automatically. Log out, log back
in, and the floating bar is already there, ready to type.

> [!TIP]
> Building the `.deb` yourself, running from source, or contributing?
> See [`DEVELOPMENT.md`](./DEVELOPMENT.md) for the full technical setup.

## ⌨️ The Bornona Layout

July types with **Bornona**, a fixed Bangla keyboard layout covering
every vowel, consonant, conjunct, and phala you need — vowels and kars,
all five consonant বর্গ groups, র-ফলা, রেফ, and more, including
shortcut keys for the sequences you'll type most.

Don't want to memorize it? You don't have to — open the bar's built-in
guide any time, in either language.

## 🛣️ What's Next

July's layout engine is built to grow: today it ships Bornona, and the
architecture leaves room for additional layouts (like a phonetic mode)
down the line without a rewrite.

## 📜 License

MIT — see [`LICENSE`](./LICENSE).
