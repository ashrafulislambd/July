"""Bornona fixed-layout key→glyph mapping.

This module is the sole source of truth for how raw key symbols translate
to Bangla Unicode output. It is derived directly from ``Bornona.txt`` at the
repository root — any change here must be checked against that file first
(see SPEC.md's Boundaries section).

Two kinds of entries exist because two keys (``h`` and ``r``) are
order-sensitive: what they produce depends on the key that follows them.

- ``SINGLE_KEY``: every key's own glyph when it is *not* part of a
  recognized two-key sequence (this includes ``h`` and ``r``'s own glyphs,
  used when a pending key must be flushed unresolved).
- ``TWO_KEY_SEQUENCES``: keyed by ``(pending_key, next_key)``, covering the
  independent vowel forms, র-ফলা, and রেফ.
- ``PENDING_KEYS``: the set of keys that must be held as "pending" for one
  step, awaiting the next key, before they can be resolved or flushed.
"""

from __future__ import annotations

# Keys that may begin a two-key sequence and must be buffered for one step
# before being resolved (against TWO_KEY_SEQUENCES) or flushed (using their
# own SINGLE_KEY glyph).
PENDING_KEYS: frozenset[str] = frozenset({"h", "r"})

# Every key's own glyph, used whenever it is not consumed as the second half
# of a two-key sequence from TWO_KEY_SEQUENCES.
SINGLE_KEY: dict[str, str] = {
    # 1. Vowels — independent form (see TWO_KEY_SEQUENCES for h+<vowel>)
    "A": "অ",
    # 2. Vowel modifiers / kars
    "a": "া",
    "i": "ি",
    "I": "ী",
    "u": "ু",
    "U": "ূ",
    "R": "ৃ",
    "e": "ে",
    "E": "ৈ",
    "o": "ো",
    "O": "ৌ",
    # 3. Consonants — ক-বর্গ
    "k": "ক",
    "K": "খ",
    "g": "গ",
    "G": "ঘ",
    "Q": "ঙ",
    # চ-বর্গ
    "c": "চ",
    "C": "ছ",
    "j": "জ",
    "J": "ঝ",
    "M": "ঞ",
    # ট-বর্গ
    "T": "ট",
    "W": "ঠ",
    "D": "ড",
    "w": "ঢ",
    "N": "ণ",
    # ত-বর্গ
    "t": "ত",
    "Y": "থ",
    "d": "দ",
    "y": "ধ",
    "n": "ন",
    # প-বর্গ
    "p": "প",
    "F": "ফ",
    "b": "ব",
    "v": "ভ",
    "m": "ম",
    # অন্তঃস্থ & উষ্ম বর্ণ (Others)
    "z": "য",
    "r": "র",
    "l": "ল",
    "S": "শ",
    "x": "ষ",
    "s": "স",
    "H": "হ",
    "Z": "ড়",
    "X": "ঢ়",
    "B": "য়",
    # 4. Special characters & phalas
    "h": "্",  # হসন্ত (virama) own glyph, used when flushed unresolved
    "q": "ং",  # অনুস্বার
    ":": "ঃ",  # বিসর্গ
    "@": "ঁ",  # চন্দ্রবিন্দু (Shift+2)
    "&": "ৎ",  # খণ্ড ত (Shift+7)
    "$": "৳",  # টাকা চিহ্ন
    "V": "্য",  # য-ফলা (Shift+v)
    "P": "্র",  # র-ফলা, alternate single-key (Shift+p) — same output as h+r
    "L": "।",  # দাড়ি, Bangla full stop (Shift+l)
    # 5. Numerals
    "0": "০",
    "1": "১",
    "2": "২",
    "3": "৩",
    "4": "৪",
    "5": "৫",
    "6": "৬",
    "7": "৭",
    "8": "৮",
    "9": "৯",
}

# Two-key sequences: (pending_key, next_key) -> composed output.
TWO_KEY_SEQUENCES: dict[tuple[str, str], str] = {
    # Independent vowels: h + <vowel-kar-key> -> full vowel letter
    ("h", "a"): "আ",
    ("h", "i"): "ই",
    ("h", "I"): "ঈ",
    ("h", "u"): "উ",
    ("h", "U"): "ঊ",
    ("h", "R"): "ঋ",
    ("h", "e"): "এ",
    ("h", "E"): "ঐ",
    ("h", "o"): "ও",
    ("h", "O"): "ঔ",
    # র-ফলা / রেফ — order sensitive
    ("h", "r"): "্র",  # র-ফলা
    ("r", "h"): "র্",  # রেফ
}
