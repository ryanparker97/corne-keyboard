#!/usr/bin/env python3
"""Static sanity checks for the Corne ZMK keymap."""

from __future__ import annotations

import re
from pathlib import Path

KEYMAP = Path("config/corne.keymap")
EXPECTED_LAYERS = {
    "default_layer": 42,
    "lower_layer": 42,
    "raise_layer": 42,
    "adjust_layer": 42,
}

text = KEYMAP.read_text(encoding="utf-8")
without_block_comments = re.sub(r"/\*[\s\S]*?\*/", "", text)
without_comments = re.sub(r"//.*", "", without_block_comments)

errors: list[str] = []
if without_comments.count("{") != without_comments.count("}"):
    errors.append("unbalanced braces")
if without_comments.count("<") != without_comments.count(">"):
    errors.append("unbalanced angle brackets")

for layer, expected in EXPECTED_LAYERS.items():
    pattern = rf"{layer}\s*\{{[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;"
    match = re.search(pattern, without_comments)
    if not match:
        errors.append(f"missing bindings for {layer}")
        continue
    bindings = re.findall(r"&[A-Za-z0-9_]+", match.group(1))
    if len(bindings) != expected:
        errors.append(f"{layer}: expected {expected} bindings, found {len(bindings)}")

required_tokens = [
    'compatible = "zmk,conditional-layers"',
    "if-layers = <LWR RSE>",
    "then-layer = <ADJ>",
    "&bt BT_SEL 0",
    "&bootloader",
    "&sys_reset",
    "&kp CAPS",
    "&kp LGUI",
    "&kp LALT",
    "&kp ESC",
    "&kp LC(LEFT)",
    "&kp LC(DOWN)",
    "&kp LC(UP)",
    "&kp LC(RIGHT)",
]
for token in required_tokens:
    if token not in text:
        errors.append(f"missing required token: {token}")

# Default layer physical placement checks. Keep Command and Space plain thumb keys
# on opposite hands, and keep Caps as a plain left pinky base key for the
# host Karabiner Hyper/Escape rule.
default_match = re.search(
    r"default_layer\s*\{[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;", without_comments
)
if default_match:
    default_bindings = re.findall(
        r"&[A-Za-z0-9_]+(?:\s+[^&\s]+)?", default_match.group(1)
    )
    normalized = [" ".join(binding.split()) for binding in default_bindings]
    expected_positions = {
        12: "&kp CAPS",
        35: "&kp LCTRL",
        36: "&kp LALT",
        37: "&mo 2",
        38: "&kp LGUI",
        39: "&kp SPACE",
        40: "&mo 1",
        41: "&kp RET",
    }
    for index, expected in expected_positions.items():
        if len(normalized) <= index or normalized[index] != expected:
            actual = normalized[index] if len(normalized) > index else "<missing>"
            errors.append(
                f"default_layer position {index}: expected {expected}, found {actual}"
            )

forbidden_tokens = [
    "zmk,behavior-hold-tap",
    "LC(LA(LS(LGUI)))",
]
for token in forbidden_tokens:
    if token in text:
        errors.append(f"obsolete custom behavior remains: {token}")

if errors:
    raise SystemExit("Keymap check failed:\n- " + "\n- ".join(errors))

print(
    "Keymap check passed: 4 layers, 42 bindings per layer, tri-layer/system bindings, plain Caps/Space/Command/Enter placement, macOS modifiers, ESC, and Ctrl-arrow chords present."
)
