"""Draw the Fn-layer diagram used in README.md from keymap.c.

Usage (from the repo root):
    python tools/keymap_svg.py

Reads the first two LAYOUT(...) blocks in keymap.c (base layer, then Fn layer)
and writes keymap.svg next to it. Exits non-zero if a keycode is not in the
tables below, so new keycodes get a proper label instead of a guess.
"""
import re
import sys
from html import escape
from pathlib import Path

KEYMAP_DIR = Path(__file__).resolve().parent.parent / "keyboards/gmmk/gmmk2/p96/iso/keymaps/acooke"

# [x, y, w, h] in key units, in LAYOUT order (from QMK keyboards/gmmk/gmmk2/p96/iso/keyboard.json)
GEO = [[0,0,1,1],[1.25,0,1,1],[2.25,0,1,1],[3.25,0,1,1],[4.25,0,1,1],[5.5,0,1,1],[6.5,0,1,1],[7.5,0,1,1],[8.5,0,1,1],[9.75,0,1,1],[10.75,0,1,1],[11.75,0,1,1],[12.75,0,1,1],[14,0,1,1],[15.25,0,1,1],[16.25,0,1,1],[17.25,0,1,1],[18.25,0,1,1],[0,1.125,1,1],[1,1.125,1,1],[2,1.125,1,1],[3,1.125,1,1],[4,1.125,1,1],[5,1.125,1,1],[6,1.125,1,1],[7,1.125,1,1],[8,1.125,1,1],[9,1.125,1,1],[10,1.125,1,1],[11,1.125,1,1],[12,1.125,1,1],[13,1.125,2,1],[15.25,1.125,1,1],[16.25,1.125,1,1],[17.25,1.125,1,1],[18.25,1.125,1,1],[0,2.125,1.5,1],[1.5,2.125,1,1],[2.5,2.125,1,1],[3.5,2.125,1,1],[4.5,2.125,1,1],[5.5,2.125,1,1],[6.5,2.125,1,1],[7.5,2.125,1,1],[8.5,2.125,1,1],[9.5,2.125,1,1],[10.5,2.125,1,1],[11.5,2.125,1,1],[12.5,2.125,1,1],[13.75,2.125,1.25,2],[15.25,2.125,1,1],[16.25,2.125,1,1],[17.25,2.125,1,1],[18.25,2.125,1,2],[0,3.125,1.75,1],[1.75,3.125,1,1],[2.75,3.125,1,1],[3.75,3.125,1,1],[4.75,3.125,1,1],[5.75,3.125,1,1],[6.75,3.125,1,1],[7.75,3.125,1,1],[8.75,3.125,1,1],[9.75,3.125,1,1],[10.75,3.125,1,1],[11.75,3.125,1,1],[12.75,3.125,1,1],[15.25,3.125,1,1],[16.25,3.125,1,1],[17.25,3.125,1,1],[0,4.125,1.25,1],[1.25,4.125,1,1],[2.25,4.125,1,1],[3.25,4.125,1,1],[4.25,4.125,1,1],[5.25,4.125,1,1],[6.25,4.125,1,1],[7.25,4.125,1,1],[8.25,4.125,1,1],[9.25,4.125,1,1],[10.25,4.125,1,1],[11.25,4.125,1,1],[12.25,4.125,1.75,1],[14.125,4.25,1,1],[15.25,4.125,1,1],[16.25,4.125,1,1],[17.25,4.125,1,1],[18.25,4.125,1,2],[0,5.125,1.25,1],[1.25,5.125,1.25,1],[2.5,5.125,1.25,1],[3.75,5.125,6.25,1],[10,5.125,1,1],[11,5.125,1,1],[12,5.125,1,1],[13.125,5.25,1,1],[14.125,5.25,1,1],[15.125,5.25,1,1],[16.25,5.125,1,1],[17.25,5.125,1,1]]

# Base-layer keycode -> printed legend (UK ISO). Letters, digits and F-keys are handled in base_label().
BASE_LABELS = {
    "KC_ESC": "Esc", "QK_GESC": "Esc", "KC_PSCR": "PrtSc", "KC_DEL": "Del", "KC_INS": "Ins",
    "KC_PGUP": "PgUp", "KC_PGDN": "PgDn", "KC_GRV": "`", "KC_MINS": "-", "KC_EQL": "=",
    "KC_BSPC": "Backspace", "KC_NUM": "Num", "KC_PSLS": "/", "KC_PAST": "*", "KC_PMNS": "−",
    "KC_TAB": "Tab", "KC_LBRC": "[", "KC_RBRC": "]", "KC_ENT": "Enter", "KC_PPLS": "+",
    "KC_CAPS": "Caps", "KC_SCLN": ";", "KC_QUOT": "'", "KC_NUHS": "#", "KC_LSFT": "Shift",
    "KC_NUBS": "\\", "KC_COMM": ",", "KC_DOT": ".", "KC_SLSH": "/", "KC_RSFT": "Shift",
    "KC_UP": "↑", "KC_PENT": "Enter", "KC_LCTL": "Ctrl", "KC_LGUI": "Win", "KC_LALT": "Alt",
    "KC_SPC": "", "KC_RALT": "AltGr", "KC_RCTL": "Ctrl", "KC_LEFT": "←", "KC_DOWN": "↓",
    "KC_RGHT": "→", "KC_PDOT": ".", "KC_APP": "Menu", "KC_RGUI": "Win",
}

# Fn-layer keycode -> (label, colour category). Categories are styled in the SVG below.
FN_LABELS = {
    "RM_TOGG": ("Lights", "light"), "RM_NEXT": ("Effect ▶", "light"), "RM_PREV": ("◀ Effect", "light"),
    "RM_VALU": ("Bright +", "light"), "RM_VALD": ("Bright −", "light"), "RM_HUEU": ("Hue +", "light"),
    "RM_HUED": ("Hue −", "light"), "RM_SATU": ("Sat +", "light"), "RM_SATD": ("Sat −", "light"),
    "RM_SPDU": ("Speed +", "light"), "RM_SPDD": ("Speed −", "light"),
    "LT_RED": ("Red", "red"), "LT_WHITE": ("White", "white"), "LT_RAINBOW": ("Rainbow", "rainbow"),
    "KC_MYCM": ("This PC", "media"), "KC_WHOM": ("Browser", "media"), "KC_CALC": ("Calc", "media"),
    "KC_MSEL": ("Player", "media"), "KC_MPRV": ("Prev", "media"), "KC_MPLY": ("Play", "media"),
    "KC_MNXT": ("Next", "media"), "KC_MSTP": ("Stop", "media"), "KC_MUTE": ("Mute", "media"),
    "KC_VOLU": ("Vol +", "media"), "KC_VOLD": ("Vol −", "media"),
    "NK_TOGG": ("NKRO", "toggle"), "GU_TOGG": ("Win lock", "toggle"), "QK_BOOT": ("Boot", "boot"),
}


def base_label(kc):
    if kc in BASE_LABELS:
        return BASE_LABELS[kc]
    m = re.fullmatch(r"KC_([A-Z0-9])", kc)
    if m:
        return m.group(1)
    m = re.fullmatch(r"KC_(F\d+)", kc)
    if m:
        return m.group(1)
    m = re.fullmatch(r"KC_P(\d)", kc)
    if m:
        return m.group(1)
    if kc.startswith("MO("):
        return "Fn"
    return None


def layers(source):
    # A layer ends at the ")" that is followed by the next "[n] =" or the closing "}" of the array
    blocks = re.findall(r"LAYOUT\((.*?)\)\s*,?\s*(?=\[|\})", re.sub(r"//[^\n]*|/\*.*?\*/", "", source, flags=re.S), re.S)
    out = []
    for b in blocks:
        # MO(_FL) contains parentheses, so split on commas outside them
        out.append([t.strip() for t in re.findall(r"[A-Z_][A-Z0-9_]*\([^)]*\)|[A-Z_][A-Z0-9_]*", b)])
    return out


def main():
    keymap = (KEYMAP_DIR / "keymap.c").read_text(encoding="utf-8")
    found = layers(keymap)
    if len(found) < 2:
        sys.exit("error: could not find the base and Fn LAYOUT blocks in keymap.c")
    base, fn = found[0], found[1]
    if len(base) != len(GEO) or len(fn) != len(GEO):
        sys.exit(f"error: expected {len(GEO)} keys per layer, got base={len(base)} fn={len(fn)}")

    missing = sorted({k for k in base if base_label(k) is None} |
                     {k for k in fn if k not in FN_LABELS and k not in ("_______", "KC_TRNS", "KC_NO", "XXXXXXX")})
    if missing:
        sys.exit("error: add these keycodes to BASE_LABELS or FN_LABELS in tools/keymap_svg.py: " + ", ".join(missing))

    U, PAD = 54, 14
    W, H = 19.25 * U + PAD * 2, 6.25 * U + PAD * 2
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" font-family="Segoe UI, Helvetica, Arial, sans-serif">
<defs><linearGradient id="rb" x1="0" x2="1">
<stop offset="0" stop-color="#e5484d"/><stop offset=".25" stop-color="#f5a524"/><stop offset=".5" stop-color="#30a46c"/><stop offset=".75" stop-color="#3e8ef7"/><stop offset="1" stop-color="#8e4ec6"/></linearGradient></defs>
<style>
.plate{{fill:#2a2e34}} .cap{{fill:#f7f8f9;stroke:#c9ced4}} .dim{{opacity:.45}} .base{{fill:#1b1f24;font-size:11px}}
.fn{{font-size:10.5px;font-weight:700}} .fnkey{{fill:#1b1f24}} .fnkey-t{{fill:#f7f8f9;font-size:11px;font-weight:700}}
.light{{fill:#b86e00}} .media{{fill:#0b7f86}} .toggle{{fill:#2f8a3c}} .boot{{fill:#b0359a}} .red{{fill:#c8252c}} .white{{fill:#5d6670}} .rainbow{{fill:#5b4bd6}}
.bar-light{{fill:#f0a531}} .bar-media{{fill:#3cc4cb}} .bar-toggle{{fill:#5fcf6e}} .bar-boot{{fill:#e57ad3}} .bar-red{{fill:#e5484d}} .bar-white{{fill:#c9ced4}} .bar-rainbow{{fill:url(#rb)}}
@media (prefers-color-scheme: dark) {{
 .plate{{fill:#0b0d10}} .cap{{fill:#2b3038;stroke:#1c2026}} .base{{fill:#e6e9ed}} .fnkey{{fill:#e6e9ed}} .fnkey-t{{fill:#15181c}}
 .light{{fill:#f0a531}} .media{{fill:#3cc4cb}} .toggle{{fill:#5fcf6e}} .boot{{fill:#e57ad3}} .red{{fill:#ff6b6f}} .white{{fill:#e6e9ed}} .rainbow{{fill:#a99bff}}
}}
</style>
<rect class="plate" x="0" y="0" width="{W:.0f}" height="{H:.0f}" rx="14"/>''']

    for i, (x, y, w, h) in enumerate(GEO):
        px, py, pw, ph = PAD + x * U + 2, PAD + y * U + 2, w * U - 4, h * U - 4
        if base[i].startswith("MO("):
            parts.append(f'<rect class="fnkey" x="{px}" y="{py}" width="{pw}" height="{ph}" rx="5"/>'
                         f'<text class="fnkey-t" x="{px+6}" y="{py+16}">Fn</text>')
            continue
        f = FN_LABELS.get(fn[i])
        parts.append(f'<g{"" if f else " class=\"dim\""}><rect class="cap" x="{px}" y="{py}" width="{pw}" height="{ph}" rx="5"/>'
                     f'<text class="base" x="{px+6}" y="{py+16}">{escape(base_label(base[i]))}</text>')
        if f:
            label, cat = f
            parts.append(f'<rect class="bar-{cat}" x="{px}" y="{py+ph-4}" width="{pw}" height="4" rx="2"/>'
                         f'<text class="fn {cat}" x="{px+6}" y="{py+ph-10}">{escape(label)}</text>')
        parts.append("</g>")
    parts.append("</svg>\n")

    out = KEYMAP_DIR / "keymap.svg"
    out.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {out.relative_to(KEYMAP_DIR.parents[6]).as_posix()}")


if __name__ == "__main__":
    main()
