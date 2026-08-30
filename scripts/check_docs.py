#!/usr/bin/env python3
"""Validate user-facing documentation against the Windows keymap."""
from __future__ import annotations

from pathlib import Path

DOCUMENTS = (Path("README.md"), Path("KEYMAP.md"))
WINDOWS_ROWS = (
    ("`/`", "`&kp LG(TAB)`", "Win+Tab: Task View"),
    ("Bottom-right `CTRL`", "`&kp LG(DOT)`", "Win+Period: emoji picker"),
    ("`Y`", "`&kp PSCRN`", "Print Screen"),
    ("`U`", "`&kp LG(LS(S))`", "Win+Shift+S: screen snip"),
    ("`I`", "`&kp LG(S)`", "Win+S: Search"),
    ("`O`", "`&kp LG(LC(LEFT))`", "Win+Ctrl+Left: previous virtual desktop"),
    ("`P`", "`&kp LG(LC(RIGHT))`", "Win+Ctrl+Right: next virtual desktop"),
    ("Top-right `BACKSPACE`", "`&kp LG(L)`", "Win+L: lock Windows"),
)
REQUIRED_ARCHITECTURE = (
    "bilateral home-row modifiers",
    "`TAB`",
    "`LEFT CTRL` thumb",
    "`RIGHT CTRL`",
    "`&hm_l LCTRL A`",
    "`&hm_l LALT S`",
    "`&hm_l LGUI D`",
    "`&hm_l LSHFT F`",
    "`&hm_r RSHFT J`",
    "`&hm_r RGUI K`",
    "`&hm_r RALT L`",
    "`&hm_r RCTRL SEMI`",
    "`&out OUT_USB`",
    "`&out OUT_BLE`",
    "`&out OUT_TOG`",
    "RGB underglow is disabled",
)
FORBIDDEN_TERMS = (
    "macOS",
    "Karabiner",
    "skhd",
    "yabai",
    "Spotlight",
    "RGB_ON",
    "RGB_OFF",
    "RGB_EFF",
    "settings_reset",
    "nice_oled",
)
DUAL_MODE_SNIPPETS = (
    "`config/corne_left.conf`",
    "`config/corne_right.conf`",
    "`CONFIG_ZMK_USB_BOOT=y`",
    "HKRO",
    "BIOS/UEFI",
    "right half",
    "falls back",
)
CTRL_THUMB_MARKERS = {
    Path("README.md"): ("`LEFT ALT`/`RAISE`/`LEFT CTRL` thumbs", 1),
    Path("KEYMAP.md"): (
        "| Thumbs | `LEFT ALT` `RAISE` `LEFT CTRL` | `SPACE` `LOWER` `ENTER` |",
        4,
    ),
}


def markdown_row(position: str, binding: str, action: str) -> str:
    return f"| {position} | {binding} | {action} |"


def validate_document(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = [
        f"{path}: missing exact Windows shortcut row: {markdown_row(*row)}"
        for row in WINDOWS_ROWS
        if markdown_row(*row) not in text
    ]
    errors.extend(
        f"{path}: missing architecture/config text: {snippet}"
        for snippet in REQUIRED_ARCHITECTURE
        if snippet not in text
    )
    errors.extend(
        f"{path}: missing dual-mode documentation: {snippet}"
        for snippet in DUAL_MODE_SNIPPETS
        if snippet not in text
    )
    errors.extend(
        f"{path}: stale documentation term: {term}"
        for term in FORBIDDEN_TERMS
        if term.lower() in text.lower()
    )
    marker, expected_count = CTRL_THUMB_MARKERS[path]
    actual_count = text.count(marker)
    if actual_count != expected_count:
        errors.append(
            f"{path}: expected {expected_count} Ctrl thumb diagram marker(s), found {actual_count}"
        )
    return errors


def main() -> None:
    errors = [error for path in DOCUMENTS for error in validate_document(path)]
    if errors:
        raise SystemExit("Windows documentation check failed:\n- " + "\n- ".join(errors))
    print("Documentation check passed: layout, Windows shortcuts, dual-mode output, BIOS compatibility, and RGB state match.")


if __name__ == "__main__":
    main()
