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

layer_bindings: dict[str, list[str]] = {}
for layer, expected in EXPECTED_LAYERS.items():
    pattern = rf"{layer}\s*\{{[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;"
    match = re.search(pattern, without_comments)
    if not match:
        errors.append(f"missing bindings for {layer}")
        continue
    raw_bindings = match.group(1)
    bindings = re.findall(r"&[A-Za-z0-9_]+", raw_bindings)
    if len(bindings) != expected:
        errors.append(f"{layer}: expected {expected} bindings, found {len(bindings)}")
    layer_bindings[layer] = [
        " ".join(binding.split())
        for binding in re.findall(r"&[A-Za-z0-9_]+(?:\s+[^&\s]+)*", raw_bindings)
    ]

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
    "&kp QUESTION",
    "#include <dt-bindings/zmk/rgb.h>",
    "&rgb_ug RGB_EFF",
    "&rgb_ug RGB_TOG",
    "&rgb_ug RGB_ON",
    "&rgb_ug RGB_OFF",
    "&rgb_ug RGB_HUI",
    "&rgb_ug RGB_SAI",
]
for token in required_tokens:
    if token not in text:
        errors.append(f"missing required token: {token}")

common_key_baseline_by_layer = {
    # Practical compact-keyboard baseline: validate the parsed bindings from
    # the actual layers, not just token presence anywhere in comments/docs.
    # Avoid full-size/niche parity keys unless they become a confirmed workflow
    # requirement.
    "default_layer": {
        "letters": [f"&kp {letter}" for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"],
        "base_punctuation": [
            "&kp SEMI",
            "&kp SQT",
            "&kp COMMA",
            "&kp DOT",
            "&kp FSLH",
        ],
        "base_editing_modifiers": [
            "&kp ESC",
            "&kp BSPC",
            "&kp RET",
            "&kp SPACE",
            "&mo 1",
            "&kp CAPS",
            "&kp LSHFT",
            "&kp LCTRL",
            "&kp LALT",
            "&kp LGUI",
        ],
    },
    "lower_layer": {
        "digits": [f"&kp N{digit}" for digit in range(10)],
        "lower_symbol_punctuation": ["&kp GRAVE"],
        "lower_editing_navigation": [
            "&kp TAB",
            "&kp DEL",
            "&kp LEFT",
            "&kp DOWN",
            "&kp UP",
            "&kp RIGHT",
            "&kp HOME",
            "&kp END",
            "&kp PG_UP",
            "&kp PG_DN",
        ],
        "function_keys": [f"&kp F{number}" for number in range(1, 13)],
    },
    "raise_layer": {
        "paired_symbol_punctuation": [
            "&kp TILDE",
            "&kp MINUS",
            "&kp UNDER",
            "&kp EQUAL",
            "&kp PLUS",
            "&kp LBKT",
            "&kp RBKT",
            "&kp LBRC",
            "&kp RBRC",
            "&kp BSLH",
            "&kp PIPE",
            "&kp COLON",
            "&kp DQT",
            "&kp LT",
            "&kp GT",
            "&kp QUESTION",
            "&kp EXCL",
            "&kp AT",
            "&kp HASH",
            "&kp DLLR",
            "&kp PRCNT",
            "&kp CARET",
            "&kp AMPS",
            "&kp STAR",
            "&kp LPAR",
            "&kp RPAR",
        ],
        "editor_resize_chords": [
            "&kp LC(LEFT)",
            "&kp LC(DOWN)",
            "&kp LC(UP)",
            "&kp LC(RIGHT)",
        ],
    },
}
for layer, groups in common_key_baseline_by_layer.items():
    actual = set(layer_bindings.get(layer, []))
    for group, bindings in groups.items():
        for binding in bindings:
            if binding not in actual:
                errors.append(f"{layer}: missing common {group} binding: {binding}")

MIRRORED_THUMB_POSITIONS = {
    36: "&kp LALT",
    37: "&mo 2",
    38: "&kp LGUI",
    39: "&kp SPACE",
    40: "&mo 1",
    41: "&kp RET",
}

# Default layer physical placement checks. Keep Command and Space plain thumb keys
# on opposite hands, use separate Lower and Enter right thumbs, and keep Caps as
# a plain left pinky base key for the host Karabiner Hyper/Escape rule.
default_match = re.search(
    r"default_layer\s*\{[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;", without_comments
)
if default_match:
    default_bindings = re.findall(
        r"&[A-Za-z0-9_]+(?:\s+[^&\s]+)*", default_match.group(1)
    )
    normalized = [" ".join(binding.split()) for binding in default_bindings]
    expected_positions = {
        0: "&kp ESC",
        11: "&kp BSPC",
        12: "&kp CAPS",
        35: "&kp LCTRL",
        **MIRRORED_THUMB_POSITIONS,
    }
    for index, expected in expected_positions.items():
        if len(normalized) <= index or normalized[index] != expected:
            actual = normalized[index] if len(normalized) > index else "<missing>"
            errors.append(
                f"default_layer position {index}: expected {expected}, found {actual}"
            )

# ADJ physical placement checks. Validate every position so macOS shortcuts cannot
# shift the Bluetooth selectors, RGB controls, clear action, or guarded boot/reset controls.
adjust_bindings = layer_bindings.get("adjust_layer", [])
expected_adjust_bindings = [
    "&trans",
    "&bt BT_SEL 0",
    "&bt BT_SEL 1",
    "&bt BT_SEL 2",
    "&bt BT_SEL 3",
    "&bt BT_SEL 4",
    "&kp LG(LS(N3))",
    "&kp LG(LS(N4))",
    "&kp LG(LS(N5))",
    "&kp LG(SPACE)",
    "&kp LG(TAB)",
    "&kp LC(LG(Q))",
    "&bt BT_CLR",
    "&kp LG(A)",
    "&kp LG(S)",
    "&trans",
    "&kp LG(F)",
    "&trans",
    "&rgb_ug RGB_EFF",
    "&rgb_ug RGB_TOG",
    "&rgb_ug RGB_ON",
    "&rgb_ug RGB_OFF",
    "&rgb_ug RGB_HUI",
    "&rgb_ug RGB_SAI",
    "&trans",
    "&kp LG(Z)",
    "&kp LG(X)",
    "&kp LG(C)",
    "&kp LG(V)",
    "&kp LG(LS(Z))",
    "&trans",
    "&trans",
    "&trans",
    "&trans",
    "&bootloader",
    "&sys_reset",
    "&kp LALT",
    "&mo 2",
    "&kp LGUI",
    "&kp SPACE",
    "&mo 1",
    "&kp RET",
]
for index, expected in enumerate(expected_adjust_bindings):
    if len(adjust_bindings) <= index or adjust_bindings[index] != expected:
        actual = adjust_bindings[index] if len(adjust_bindings) > index else "<missing>"
        errors.append(
            f"adjust_layer position {index}: expected {expected}, found {actual}"
        )

# Non-default thumb rows intentionally mirror the base layer so Option, Raise,
# Command, Space, Lower, and Enter remain available while any layer is active.
for layer in ("lower_layer", "raise_layer", "adjust_layer"):
    bindings = layer_bindings.get(layer, [])
    for index, expected in MIRRORED_THUMB_POSITIONS.items():
        if len(bindings) <= index or bindings[index] != expected:
            actual = bindings[index] if len(bindings) > index else "<missing>"
            errors.append(
                f"{layer} position {index}: expected mirrored thumb {expected}, found {actual}"
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
    "Keymap check passed: 4 layers, 42 bindings per layer, confirmed mirrored thumb rows, Backspace/Space/Lower/Enter positions, exact ADJ macOS shortcuts, full RGB underglow controls, BT/boot/reset safety positions, ESC, Ctrl-arrow chords, and practical common-key coverage present."
)
