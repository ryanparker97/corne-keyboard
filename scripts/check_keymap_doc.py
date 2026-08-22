#!/usr/bin/env python3
"""Validate KEYMAP.md mirrors the accepted Corne thumb layout."""
from __future__ import annotations

from pathlib import Path

KEYMAP_DOC = Path("KEYMAP.md")

EXPECTED_THUMB_BLOCK = (
    "Left thumbs, outer -> inner:  LALT  RAISE  CMD\n"
    "Right thumbs, inner -> outer: SPACE  LOWER  ENTER\n"
    "Raw bindings: &kp LALT  &mo RSE  &kp LGUI    &kp SPACE  &mo LWR  &kp RET"
)
EXPECTED_DIAGRAM_THUMBS = "              LALT RSE CMD    SPACE LWR RET"
EXPECTED_PROSE = (
    "macOS Command is on the inner-left thumb as `LGUI`. "
    "Space is on the inner-right thumb."
)
STALE_THUMB_TOKENS = (
    "Left thumbs, outer -> inner:  LALT  RAISE  SPACE",
    "Right thumbs, inner -> outer: RGUI  LOWER  ENTER",
    "Raw bindings: &kp LALT  &mo RSE  &kp SPACE",
    "Space is on the inner-left thumb",
    "`RGUI` is macOS Command",
    "LALT RSE SPACE    RGUI LWR RET",
)


def main() -> None:
    text = KEYMAP_DOC.read_text(encoding="utf-8")
    errors: list[str] = []

    if EXPECTED_THUMB_BLOCK not in text:
        errors.append("missing exact Mac thumb row/raw binding block")
    if EXPECTED_PROSE not in text:
        errors.append("missing Command-left/Space-right thumb prose")

    diagram_count = text.count(EXPECTED_DIAGRAM_THUMBS)
    if diagram_count != 4:
        errors.append(f"expected 4 layer thumb diagrams, found {diagram_count}")

    for token in STALE_THUMB_TOKENS:
        if token in text:
            errors.append(f"stale thumb documentation remains: {token}")

    if errors:
        raise SystemExit("KEYMAP.md check failed:\n- " + "\n- ".join(errors))
    print("KEYMAP.md check passed: thumb block, raw bindings, prose, and four layer diagrams match the Mac layout.")


if __name__ == "__main__":
    main()
