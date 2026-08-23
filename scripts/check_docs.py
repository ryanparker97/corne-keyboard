#!/usr/bin/env python3
"""Validate exact Windows ADJ mapping rows in each user-facing document."""
from __future__ import annotations

from pathlib import Path

DOCUMENTS = (Path("README.md"), Path("KEYMAP.md"))
WINDOWS_ADJ_ROWS = (
    ("`Y`", "`&kp PSCRN`", "Print Screen"),
    ("`U`", "`&kp LG(LS(S))`", "Win+Shift+S: screen snip"),
    ("`I`", "`&kp LG(V)`", "Win+V: Clipboard history"),
    ("`O`", "`&kp LG(S)`", "Win+S: Search"),
    ("`P`", "`&kp LG(TAB)`", "Win+Tab: Task View"),
    ("Top-right `BACKSPACE`", "`&kp LG(L)`", "Win+L: lock Windows"),
    ("`A`", "`&kp LC(A)`", "Ctrl+A: select all"),
    ("`S`", "`&kp LC(S)`", "Ctrl+S: save"),
    ("`D`", "`&kp LG(R)`", "Win+R: Run"),
    ("`F`", "`&kp LC(F)`", "Ctrl+F: find"),
    ("`G`", "`&kp LG(LEFT)`", "Win+Left: snap window left"),
    ("`H`", "`&kp LG(RIGHT)`", "Win+Right: snap window right"),
    ("`Z`", "`&kp LC(Z)`", "Ctrl+Z: undo"),
    ("`X`", "`&kp LC(X)`", "Ctrl+X: cut"),
    ("`C`", "`&kp LC(C)`", "Ctrl+C: copy"),
    ("`V`", "`&kp LC(V)`", "Ctrl+V: paste"),
    ("`B`", "`&kp LC(LS(Z))`", "Ctrl+Shift+Z: redo"),
)
FORBIDDEN_HOST_ASSUMPTIONS = ("macOS", "Karabiner", "skhd", "yabai", "Spotlight")


def markdown_row(position: str, binding: str, action: str) -> str:
    """Return the required position, binding, and behavior table row."""
    return f"| {position} | {binding} | {action} |"


def validate_document(path: Path) -> list[str]:
    """Return all Windows workflow documentation errors for one document."""
    text = path.read_text(encoding="utf-8")
    missing_rows = [
        markdown_row(*row) for row in WINDOWS_ADJ_ROWS if markdown_row(*row) not in text
    ]
    errors = [f"{path}: missing exact Windows ADJ row: {row}" for row in missing_rows]
    obsolete = [
        term for term in FORBIDDEN_HOST_ASSUMPTIONS if term.lower() in text.lower()
    ]
    if obsolete:
        errors.append(f"{path}: obsolete host assumptions: {', '.join(obsolete)}")
    return errors


def main() -> None:
    errors = [error for path in DOCUMENTS for error in validate_document(path)]
    if errors:
        raise SystemExit("Windows documentation check failed:\n- " + "\n- ".join(errors))
    print("Documentation check passed: each document has exact native Windows ADJ rows.")


if __name__ == "__main__":
    main()
