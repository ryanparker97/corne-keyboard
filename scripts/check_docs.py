#!/usr/bin/env python3
"""Validate user-facing documentation against the Windows data/DevOps keymap."""
from __future__ import annotations

import re
from pathlib import Path

DOCUMENTS = (Path("README.md"), Path("KEYMAP.md"))

LAYER_ROWS = (
    "| Top | `ESC` `Q` `W` `E` `R` `T` | `Y` `U` `I` `O` `P` `BACKSPACE` |",
    "| Home | `TAB` `A` `S` `D` `F` `G` | `H` `J` `K` `L` `;` `'` |",
    "| Bottom | `LEFT SHIFT` `Z` `X` `C` `V` `B` | `N` `M` `,` `.` `/` `WIN` |",
    "| Thumbs | `ALT` `RAISE` `CTRL` | `SPACE` `LOWER` `ENTER` |",
    "| Top | `` ` `` `1` `2` `3` `4` `5` | `6` `7` `8` `9` `0` `DELETE` |",
    "| Home | `VIM` `CTRL` `ALT` `WIN` `SHIFT` `TMUX` | `LEFT` `DOWN` `UP` `RIGHT` `PAGE DOWN` `PAGE UP` |",
    "| Bottom | `F1` `F2` `F3` `F4` `F5` `F6` | `F7` `F8` `F9` `F10` `F11` `F12` |",
    "| Thumbs | `CTRL` `RAISE` `WIN` | `SPACE` `LOWER` `ENTER` |",
    "| Top | `~` `!` `@` `#` `$` `%` | `^` `&` `*` `(` `)` `?` |",
    "| Home | `-` `CTRL` `ALT` `WIN` `SHIFT` `=` | `[` `{` `:` `|` `}` `]` |",
    "| Bottom | `\\` `'` `\"` `_` `+` `` ` `` | `<` `>` `,` `.` `/` `;` |",
    "| Top | `BOOT` `BT 1` `BT 2` `BT 3` `BT 4` `BT 5` | `PRINT SCREEN` `SNIP` `SEARCH` `DESKTOP LEFT` `DESKTOP RIGHT` `LOCK` |",
    "| Home | `BT CLEAR` `MEDIA PREV` `PLAY/PAUSE` `MEDIA NEXT` `MUTE` `VOL DOWN` | `NONE` `NONE` `CAPS WORD` `CAPS LOCK` `NONE` `NONE` |",
    "| Bottom | `RESET` `BRIGHTNESS DOWN` `BRIGHTNESS UP` `USB` `BLE` `VOL UP` | `OUTPUT TOGGLE` `NONE` `NONE` `NONE` `NONE` `NONE` |",
)

REQUIRED_TEXT = (
    "Windows", "data engineering", "DevOps", "plain QWERTY", "no home-row modifiers",
    "Vim", "Ctrl-W", "tmux", "Ctrl-B", "Python", "YAML", "SQL",
    "`&vim_window_prefix`", "`&tmux_prefix`", "`&kp PSCRN`", "`&kp LG(LS(S))`",
    "`&kp LG(S)`", "`&kp LG(LC(LEFT))`", "`&kp LG(LC(RIGHT))`", "`&kp LG(L)`",
    "`&out OUT_USB`", "`&out OUT_BLE`", "`&out OUT_TOG`",
    "`LWIN` is the pinned-supported alias for a standalone Windows modifier",
    "`LG(...)` remains the standard ZMK wrapper for Windows chords",
    "physical Base-layer swap", "Other layers retain their existing modifier clusters",
    "does not expose an `LW(...)` wrapper", "physical `K`", "physical `L`",
    "RGB underglow is disabled", "`&none`", "42",
)

PRESERVED_ARCHITECTURE = (
    "`nice_nano/nrf52840/zmk`", "`corne_left`", "`corne_right`",
    "`config/corne_left.conf`", "`config/corne_right.conf`",
    "`CONFIG_ZMK_USB_BOOT=y`", "HKRO", "right half", "falls back",
)

FORBIDDEN_PATTERNS = (
    r"\bmacOS\b", r"\bOption\b", r"\bCommand\b", r"\bCMD\b",
    r"\bSpotlight\b", r"\bApp switcher\b", r"&kp LGUI", r"&kp LCMD",
    r"&kp LG\(LS\(N5\)\)", r"&kp LG\(SPACE\)", r"&kp LG\(TAB\)",
    r"&kp LC\(LG\(Q\)\)", r"bilateral home-row", r"home-row holds",
    r"Task View", r"emoji picker", r"RGB_ON", r"RGB_OFF", r"RGB_EFF",
    r"&rgb_ug", r"&led_strip", r"&kscan0", r"27 LEDs", r"3 ms",
)


def validate_document(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = [
        f"{path}: missing exact physical row: {row}"
        for row in LAYER_ROWS if row not in text
    ]
    errors.extend(
        f"{path}: missing layout text: {snippet}"
        for snippet in REQUIRED_TEXT if snippet not in text
    )
    errors.extend(
        f"{path}: missing preserved architecture/config text: {snippet}"
        for snippet in PRESERVED_ARCHITECTURE if snippet not in text
    )
    errors.extend(
        f"{path}: stale documentation pattern: {pattern}"
        for pattern in FORBIDDEN_PATTERNS if re.search(pattern, text)
    )
    if text.count("| Thumbs |") != 4:
        errors.append(f"{path}: expected four exact thumb rows")
    return errors


def main() -> None:
    errors = [error for path in DOCUMENTS for error in validate_document(path)]
    if errors:
        raise SystemExit("Windows documentation check failed:\n- " + "\n- ".join(errors))
    print(
        "Documentation check passed: all physical rows, Windows workflows, dual-mode "
        "architecture, guarded controls, and disabled RGB policy match."
    )


if __name__ == "__main__":
    main()
