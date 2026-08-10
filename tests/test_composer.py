"""Unit tests for the Bornona composer (src/bornona_ibus/composer.py).

Written against the mapping in Bornona.txt. Each test feeds a raw key
sequence (as typed) into `compose()` and asserts the exact Bangla Unicode
output, per SPEC.md's Testing Strategy.
"""

from bornona_ibus.composer import compose


class TestIndependentVowels:
    """h + <vowel-kar-key> -> independent vowel letter (Bornona.txt §1)."""

    def test_a_alone(self):
        assert compose(["A"]) == "অ"

    def test_aa(self):
        assert compose(["h", "a"]) == "আ"

    def test_i(self):
        assert compose(["h", "i"]) == "ই"

    def test_ii(self):
        assert compose(["h", "I"]) == "ঈ"

    def test_u(self):
        assert compose(["h", "u"]) == "উ"

    def test_uu(self):
        assert compose(["h", "U"]) == "ঊ"

    def test_ri(self):
        assert compose(["h", "R"]) == "ঋ"

    def test_e(self):
        assert compose(["h", "e"]) == "এ"

    def test_oi(self):
        assert compose(["h", "E"]) == "ঐ"

    def test_o(self):
        assert compose(["h", "o"]) == "ও"

    def test_ou(self):
        assert compose(["h", "O"]) == "ঔ"


class TestKars:
    """Vowel modifiers applied directly after a consonant (Bornona.txt §2)."""

    def test_kaar(self):
        assert compose(["k", "a"]) == "কা"

    def test_ki(self):
        assert compose(["k", "i"]) == "কি"

    def test_kii(self):
        assert compose(["k", "I"]) == "কী"

    def test_ku(self):
        assert compose(["k", "u"]) == "কু"

    def test_kuu(self):
        assert compose(["k", "U"]) == "কূ"

    def test_kri(self):
        assert compose(["k", "R"]) == "কৃ"

    def test_ke(self):
        assert compose(["k", "e"]) == "কে"

    def test_koi(self):
        assert compose(["k", "E"]) == "কৈ"

    def test_ko(self):
        assert compose(["k", "o"]) == "কো"

    def test_kou(self):
        assert compose(["k", "O"]) == "কৌ"


class TestConsonants:
    """All consonants across the five বর্গ groups (Bornona.txt §3)."""

    @staticmethod
    def _check(key, glyph):
        assert compose([key]) == glyph

    def test_ka_borgo(self):
        for key, glyph in [("k", "ক"), ("K", "খ"), ("g", "গ"), ("G", "ঘ"), ("Q", "ঙ")]:
            self._check(key, glyph)

    def test_cha_borgo(self):
        for key, glyph in [("c", "চ"), ("C", "ছ"), ("j", "জ"), ("J", "ঝ"), ("M", "ঞ")]:
            self._check(key, glyph)

    def test_ta_borgo(self):
        for key, glyph in [("T", "ট"), ("W", "ঠ"), ("D", "ড"), ("w", "ঢ"), ("N", "ণ")]:
            self._check(key, glyph)

    def test_to_borgo(self):
        for key, glyph in [("t", "ত"), ("Y", "থ"), ("d", "দ"), ("y", "ধ"), ("n", "ন")]:
            self._check(key, glyph)

    def test_pa_borgo(self):
        for key, glyph in [("p", "প"), ("F", "ফ"), ("b", "ব"), ("v", "ভ"), ("m", "ম")]:
            self._check(key, glyph)

    def test_others(self):
        for key, glyph in [
            ("z", "য"),
            ("l", "ল"),
            ("S", "শ"),
            ("x", "ষ"),
            ("s", "স"),
            ("H", "হ"),
            ("Z", "ড়"),
            ("X", "ঢ়"),
            ("B", "য়"),
        ]:
            self._check(key, glyph)

    def test_ra_standalone(self):
        # 'r' is a pending key; standalone (unresolved) it flushes to its
        # own glyph.
        assert compose(["r"]) == "র"


class TestConjuncts:
    """Consonant clusters formed via হসন্ত (hosonto)."""

    def test_kkhо(self):
        # ক্ষ = k + h + x
        assert compose(["k", "h", "x"]) == "ক্ষ"

    def test_ng_kh(self):
        # ঙ্ক = Q + h + k
        assert compose(["Q", "h", "k"]) == "ঙ্ক"


class TestHRDisambiguation:
    """h and r are order-sensitive: h+r != r+h (Bornona.txt §4)."""

    def test_h_then_r_is_rofola(self):
        assert compose(["h", "r"]) == "্র"

    def test_r_then_h_is_reph(self):
        assert compose(["r", "h"]) == "র্"

    def test_r_then_unrelated_flushes_ra(self):
        # "ra" -> র (flushed) + া (kar) = রা
        assert compose(["r", "a"]) == "রা"

    def test_h_then_unrelated_flushes_hosonto(self):
        # "h" followed by a consonant that doesn't resolve it: flush হসন্ত,
        # then process the consonant normally -> conjunct.
        assert compose(["k", "h", "m"]) == "ক্ম"


class TestStandaloneHosonto:
    def test_h_alone(self):
        assert compose(["h"]) == "্"

    def test_h_before_space(self):
        assert compose(["h", " "]) == "্ "


class TestSpecialCharsAndPhalas:
    def test_anusvara(self):
        assert compose(["q"]) == "ং"

    def test_bisarga(self):
        assert compose([":"]) == "ঃ"

    def test_chandrabindu(self):
        assert compose(["@"]) == "ঁ"

    def test_khanda_ta(self):
        assert compose(["&"]) == "ৎ"

    def test_taka_sign(self):
        assert compose(["$"]) == "৳"

    def test_zo_fola(self):
        assert compose(["V"]) == "্য"

    def test_ro_fola_alternate_key(self):
        # Shift+p is an alternate single-key way to produce র-ফলা, same
        # output as the two-key h+r sequence.
        assert compose(["P"]) == "্র" == compose(["h", "r"])

    def test_dari(self):
        assert compose(["L"]) == "।"


class TestNumerals:
    def test_all_digits(self):
        expected = "০১২৩৪৫৬৭৮৯"
        for digit, glyph in zip("0123456789", expected, strict=True):
            assert compose([digit]) == glyph
