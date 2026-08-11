"""User guide window: the Bornona key mapping, in বাংলা or English.

Glyphs shown here are computed live through `composer.compose()` rather
than hardcoded, so the guide can never drift out of sync with what
actually happens when you type — if the mapping changes, this changes
with it automatically. Only the key-sequence labels, section titles, and
descriptions are hand-authored (bilingual, toggled together).
"""

from __future__ import annotations

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402

from bornona_ibus.composer import compose  # noqa: E402

# Each section: (title_en, title_bn, rule_en, rule_bn, entries)
# Each entry: (key_sequence, key_label, description_en, description_bn)
GUIDE_SECTIONS = [
    (
        "Independent Vowels",
        "স্বরবর্ণ (স্বাধীন রূপ)",
        "Press h, then the vowel key.",
        "হ চেপে তারপর স্বরের কী চাপুন।",
        [
            (["A"], "A", "a (as in 'about')", "অ-ধ্বনি"),
            (["h", "a"], "h + a", "aa (as in 'father')", "আ-ধ্বনি"),
            (["h", "i"], "h + i", "i (short)", "হ্রস্ব ই-ধ্বনি"),
            (["h", "I"], "h + I", "ii (long)", "দীর্ঘ ঈ-ধ্বনি"),
            (["h", "u"], "h + u", "u (short)", "হ্রস্ব উ-ধ্বনি"),
            (["h", "U"], "h + U", "uu (long)", "দীর্ঘ ঊ-ধ্বনি"),
            (["h", "R"], "h + R", "ri (vocalic r)", "ঋ-ধ্বনি"),
            (["h", "e"], "h + e", "e", "এ-ধ্বনি"),
            (["h", "E"], "h + E", "oi", "ঐ-ধ্বনি"),
            (["h", "o"], "h + o", "o", "ও-ধ্বনি"),
            (["h", "O"], "h + O", "ou", "ঔ-ধ্বনি"),
        ],
    ),
    (
        "Vowel Signs (Kars)",
        "স্বরবর্ণের কার",
        "Press right after a consonant.",
        "ব্যঞ্জনবর্ণের ঠিক পরে চাপুন।",
        [
            (["k", "a"], "a", "aa-kar", "আ-কার"),
            (["k", "i"], "i", "i-kar (short)", "হ্রস্ব ই-কার"),
            (["k", "I"], "I", "ii-kar (long)", "দীর্ঘ ঈ-কার"),
            (["k", "u"], "u", "u-kar (short)", "হ্রস্ব উ-কার"),
            (["k", "U"], "U", "uu-kar (long)", "দীর্ঘ ঊ-কার"),
            (["k", "R"], "R", "ri-kar", "ঋ-কার"),
            (["k", "e"], "e", "e-kar", "এ-কার"),
            (["k", "E"], "E", "oi-kar", "ঐ-কার"),
            (["k", "o"], "o", "o-kar", "ও-কার"),
            (["k", "O"], "O", "ou-kar", "ঔ-কার"),
        ],
    ),
    (
        "Consonants — ক-বর্গ",
        "ব্যঞ্জনবর্ণ — ক-বর্গ",
        "",
        "",
        [
            (["k"], "k", "ka", "ক"),
            (["K"], "K", "kha", "খ"),
            (["g"], "g", "ga", "গ"),
            (["G"], "G", "gha", "ঘ"),
            (["Q"], "Q", "nga", "ঙ"),
        ],
    ),
    (
        "Consonants — চ-বর্গ",
        "ব্যঞ্জনবর্ণ — চ-বর্গ",
        "",
        "",
        [
            (["c"], "c", "cha", "চ"),
            (["C"], "C", "chha", "ছ"),
            (["j"], "j", "ja", "জ"),
            (["J"], "J", "jha", "ঝ"),
            (["M"], "M", "nya", "ঞ"),
        ],
    ),
    (
        "Consonants — ট-বর্গ",
        "ব্যঞ্জনবর্ণ — ট-বর্গ",
        "",
        "",
        [
            (["T"], "T", "Ta", "ট"),
            (["W"], "W", "Tha", "ঠ"),
            (["D"], "D", "Da", "ড"),
            (["w"], "w", "Dha", "ঢ"),
            (["N"], "N", "Na", "ণ"),
        ],
    ),
    (
        "Consonants — ত-বর্গ",
        "ব্যঞ্জনবর্ণ — ত-বর্গ",
        "",
        "",
        [
            (["t"], "t", "ta", "ত"),
            (["Y"], "Y", "tha", "থ"),
            (["d"], "d", "da", "দ"),
            (["y"], "y", "dha", "ধ"),
            (["n"], "n", "na", "ন"),
        ],
    ),
    (
        "Consonants — প-বর্গ",
        "ব্যঞ্জনবর্ণ — প-বর্গ",
        "",
        "",
        [
            (["p"], "p", "pa", "প"),
            (["f"], "f", "fa", "ফ"),
            (["b"], "b", "ba", "ব"),
            (["v"], "v", "bha", "ভ"),
            (["m"], "m", "ma", "ম"),
        ],
    ),
    (
        "Consonants — Others",
        "ব্যঞ্জনবর্ণ — অন্যান্য",
        "",
        "",
        [
            (["z"], "z", "ya", "য"),
            (["r"], "r", "ra", "র"),
            (["l"], "l", "la", "ল"),
            (["S"], "S", "sha", "শ"),
            (["x"], "x", "sha (retroflex)", "ষ"),
            (["s"], "s", "sa", "স"),
            (["H"], "H", "ha", "হ"),
            (["Z"], "Z", "Ra", "ড়"),
            (["X"], "X", "Rha", "ঢ়"),
            (["B"], "B", "ya (antahstha)", "য়"),
        ],
    ),
    (
        "Special Characters & Phalas",
        "বিশেষ চিহ্ন ও ফলা",
        "",
        "",
        [
            (["h"], "h (alone)", "hasanta / virama (link letters)", "হসন্ত"),
            (["q"], "q", "anusvara", "অনুস্বার"),
            ([":"], ":", "bisarga", "বিসর্গ"),
            (["@"], "@ (Shift+2)", "chandrabindu", "চন্দ্রবিন্দু"),
            (["&"], "& (Shift+7)", "khanda ta", "খণ্ড ত"),
            (["$"], "$", "taka sign", "টাকা চিহ্ন"),
            (["V"], "V (Shift+v)", "zo-fola", "য-ফলা"),
            (["h", "r"], "h + r", "ro-fola", "র-ফলা"),
            (["P"], "P (Shift+p)", "ro-fola (shortcut)", "র-ফলা (শর্টকাট)"),
            (["r", "h"], "r + h", "reph", "রেফ"),
            (["F"], "F (Shift+f)", "reph (shortcut)", "রেফ (শর্টকাট)"),
            (["L"], "L (Shift+l)", "dari (full stop)", "দাড়ি"),
        ],
    ),
    (
        "Numerals",
        "সংখ্যা",
        "",
        "",
        [([d], d, "", "") for d in "0123456789"],
    ),
]


def _build_language_toggle(on_toggle) -> Gtk.Button:
    button = Gtk.Button(label="বাংলা / EN")
    button.connect("clicked", lambda _b: on_toggle())
    return button


def _entry_row(key_label: str, glyph: str, desc_en: str, desc_bn: str, bangla: bool) -> Gtk.Box:
    row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)

    key_lbl = Gtk.Label(label=key_label)
    key_lbl.set_width_chars(14)
    key_lbl.set_xalign(0)
    key_lbl.get_style_context().add_class("dim-label")
    row.pack_start(key_lbl, False, False, 0)

    glyph_lbl = Gtk.Label(label=glyph)
    glyph_lbl.set_width_chars(4)
    glyph_lbl.set_xalign(0)
    row.pack_start(glyph_lbl, False, False, 0)

    desc = desc_bn if bangla else desc_en
    if desc:
        desc_lbl = Gtk.Label(label=desc)
        desc_lbl.set_xalign(0)
        row.pack_start(desc_lbl, True, True, 0)

    return row


def build_guide_window(bangla_initial: bool = True) -> Gtk.Window:
    """Build the (not-yet-shown) user guide window."""
    win = Gtk.Window(title="Bornona — User Guide")
    win.set_default_size(480, 640)
    win.set_position(Gtk.WindowPosition.CENTER)

    state = {"bangla": bangla_initial}

    outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    outer.set_border_width(12)
    win.add(outer)

    header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    title_label = Gtk.Label()
    title_label.set_xalign(0)
    title_label.set_markup("<b>Bornona User Guide</b>")
    header.pack_start(title_label, True, True, 0)
    outer.pack_start(header, False, False, 0)

    scroller = Gtk.ScrolledWindow()
    scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
    content.set_border_width(4)
    scroller.add(content)
    outer.pack_start(scroller, True, True, 0)

    def render() -> None:
        bangla = state["bangla"]
        for child in content.get_children():
            content.remove(child)

        for title_en, title_bn, rule_en, rule_bn, entries in GUIDE_SECTIONS:
            frame = Gtk.Frame()
            frame.set_label(title_bn if bangla else title_en)
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            box.set_border_width(8)
            frame.add(box)

            rule = rule_bn if bangla else rule_en
            if rule:
                rule_lbl = Gtk.Label(label=rule)
                rule_lbl.set_xalign(0)
                rule_lbl.get_style_context().add_class("dim-label")
                box.pack_start(rule_lbl, False, False, 0)

            for key_sequence, key_label, desc_en, desc_bn in entries:
                glyph = compose(key_sequence)
                box.pack_start(
                    _entry_row(key_label, glyph, desc_en, desc_bn, bangla), False, False, 0
                )

            content.pack_start(frame, False, False, 0)

        content.show_all()

    def toggle_language() -> None:
        state["bangla"] = not state["bangla"]
        render()

    header.pack_start(_build_language_toggle(toggle_language), False, False, 0)

    render()
    return win
