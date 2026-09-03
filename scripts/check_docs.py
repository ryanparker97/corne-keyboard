#!/usr/bin/env python3
"""Validate user-facing documentation against the macOS data/DevOps keymap."""
from __future__ import annotations

from pathlib import Path

DOCUMENTS = (Path("README.md"), Path("KEYMAP.md"))

LAYER_ROWS = (
    "| Top | `ESC` `Q` `W` `E` `R` `T` | `Y` `U` `I` `O` `P` `BACKSPACE` |",
    "| Home | `TAB` `A` `S` `D` `F` `G` | `H` `J` `K` `L` `;` `'` |",
    "| Bottom | `LEFT SHIFT` `Z` `X` `C` `V` `B` | `N` `M` `,` `.` `/` `RIGHT CTRL` |",
    "| Thumbs | `OPTION` `RAISE` `COMMAND` | `SPACE` `LOWER` `ENTER` |",
    "| Top | `` ` `` `1` `2` `3` `4` `5` | `6` `7` `8` `9` `0` `DELETE` |",
    "| Home | `VIM` `CTRL` `OPTION` `COMMAND` `SHIFT` `TMUX` | `LEFT` `DOWN` `UP` `RIGHT` `PAGE DOWN` `PAGE UP` |",
    "| Bottom | `F1` `F2` `F3` `F4` `F5` `F6` | `F7` `F8` `F9` `F10` `F11` `F12` |",
    "| Thumbs | `CTRL` `RAISE` `COMMAND` | `SPACE` `LOWER` `ENTER` |",
    "| Top | `~` `!` `@` `#` `$` `%` | `^` `&` `*` `(` `)` `?` |",
    "| Home | `-` `CTRL` `OPTION` `COMMAND` `SHIFT` `=` | `[` `{` `:` `|` `}` `]` |",
    "| Bottom | `\\` `'` `\"` `_` `+` `` ` `` | `<` `>` `,` `.` `/` `;` |",
    "| Top | `BOOT` `BT 1` `BT 2` `BT 3` `BT 4` `BT 5` | `CAPTURE` `CAPS WORD` `CAPS LOCK` `SPOTLIGHT` `APP SWITCHER` `LOCK` |",
    "| Home | `BT CLEAR` `MEDIA PREV` `PLAY/PAUSE` `MEDIA NEXT` `MUTE` `VOL DOWN` | `NONE` `NONE` `NONE` `NONE` `NONE` `NONE` |",
    "| Bottom | `RESET` `BRIGHTNESS DOWN` `BRIGHTNESS UP` `USB` `BLE` `VOL UP` | `OUTPUT TOGGLE` `NONE` `NONE` `NONE` `NONE` `NONE` |",
)

REQUIRED_TEXT = (
    "macOS", "data engineering", "DevOps", "plain QWERTY", "no home-row modifiers",
    "Vim", "Ctrl-W", "tmux", "Ctrl-B", "Python", "YAML", "SQL",
    "`&vim_window_prefix`", "`&tmux_prefix`", "`&kp LG(LS(N5))`",
    "`&kp LG(SPACE)`", "`&kp LG(TAB)`", "`&kp LC(LG(Q))`",
    "`&out OUT_USB`", "`&out OUT_BLE`", "`&out OUT_TOG`",
    "RGB underglow is disabled", "`&none`", "42",
)

PRESERVED_ARCHITECTURE = (
    "`nice_nano/nrf52840/zmk`", "`corne_left`", "`corne_right`",
    "`config/corne_left.conf`", "`config/corne_right.conf`",
    "`CONFIG_ZMK_USB_BOOT=y`", "HKRO", "right half", "falls back",
)

FORBIDDEN_TERMS = (
    "Windows-focused", "Windows-oriented", "bilateral home-row", "home-row holds",
    "`&hm_l", "`&hm_r", "Task View", "emoji picker", "RGB_ON", "RGB_OFF",
    "RGB_EFF", "`&rgb_ug", "`&led_strip`", "`&kscan0`", "27 LEDs", "3 ms",
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
        f"{path}: stale documentation term: {term}"
        for term in FORBIDDEN_TERMS if term.lower() in text.lower()
    )
    if text.count("| Thumbs |") != 4:
        errors.append(f"{path}: expected four exact thumb rows")
    return errors


def main() -> None:
    errors = [error for path in DOCUMENTS for error in validate_document(path)]
    if errors:
        raise SystemExit("macOS documentation check failed:\n- " + "\n- ".join(errors))
    print(
        "Documentation check passed: all physical rows, macOS workflows, dual-mode "
        "architecture, guarded controls, and disabled RGB policy match."
    )


if __name__ == "__main__":
    main()
