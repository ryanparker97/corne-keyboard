#!/usr/bin/env python3
"""Validate that each user-facing document matches the Windows ADJ workflow."""
from __future__ import annotations

from pathlib import Path

DOCUMENTS = (Path("README.md"), Path("KEYMAP.md"))
REQUIRED_BY_DOCUMENT = (
    "Windows",
    "Print Screen",
    "Win+Shift+S",
    "Clipboard history",
    "Win+V",
    "Win+S",
    "Task View",
    "Win+Tab",
    "Win+L",
    "Win+R",
    "Win+Left",
    "Win+Right",
    "&kp PSCRN",
    "&kp LG(LS(S))",
    "&kp LG(V)",
    "&kp LG(S)",
    "&kp LG(TAB)",
    "&kp LG(L)",
    "&kp LG(R)",
    "&kp LG(LEFT)",
    "&kp LG(RIGHT)",
)
FORBIDDEN_HOST_ASSUMPTIONS = ("macOS", "Karabiner", "skhd", "yabai", "Spotlight")


def main() -> None:
    errors: list[str] = []
    for path in DOCUMENTS:
        text = path.read_text(encoding="utf-8")
        missing = [snippet for snippet in REQUIRED_BY_DOCUMENT if snippet not in text]
        if missing:
            errors.append(f"{path}: missing Windows documentation: {', '.join(missing)}")
        obsolete = [
            term for term in FORBIDDEN_HOST_ASSUMPTIONS if term.lower() in text.lower()
        ]
        if obsolete:
            errors.append(f"{path}: obsolete host assumptions: {', '.join(obsolete)}")

    if errors:
        raise SystemExit("Windows documentation check failed:\n- " + "\n- ".join(errors))

    print("Documentation check passed: each document describes the native Windows ADJ bindings.")


if __name__ == "__main__":
    main()
