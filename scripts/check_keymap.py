#!/usr/bin/env python3
"""Static sanity checks for the Corne ZMK keymap."""
from __future__ import annotations

import re
from pathlib import Path

KEYMAP = Path("config/corne.keymap")
EXPECTED_LAYERS = ("default_layer", "lower_layer", "raise_layer", "adjust_layer")
EXPECTED_THUMBS = ["&kp LALT", "&mo RSE", "&kp LGUI", "&kp SPACE", "&mo LWR", "&kp RET"]


def fail(errors: list[str]) -> None:
    raise SystemExit("Keymap check failed:\n- " + "\n- ".join(errors))


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    return re.sub(r"//.*", "", text)


def normalize_bindings(raw: str) -> list[str]:
    return [" ".join(binding.split()) for binding in re.findall(r"&[A-Za-z0-9_]+(?:\s+[^&\s]+)*", raw)]


def layer_bindings(text: str, layer: str) -> list[str] | None:
    match = re.search(rf"{layer}\s*\{{[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;", text)
    return normalize_bindings(match.group(1)) if match else None


def main() -> None:
    text = KEYMAP.read_text(encoding="utf-8")
    active = strip_comments(text)
    errors: list[str] = []

    if active.count("{") != active.count("}"):
        errors.append("unbalanced braces")
    if active.count("<") != active.count(">"):
        errors.append("unbalanced angle brackets")

    parsed: dict[str, list[str]] = {}
    for layer in EXPECTED_LAYERS:
        bindings = layer_bindings(active, layer)
        if bindings is None:
            errors.append(f"missing bindings for {layer}")
            continue
        parsed[layer] = bindings
        if len(bindings) != 42:
            errors.append(f"{layer}: expected 42 bindings, found {len(bindings)}")
        if bindings[36:42] != EXPECTED_THUMBS:
            errors.append(f"{layer}: expected thumb row {EXPECTED_THUMBS}, found {bindings[36:42]}")

    default = parsed.get("default_layer", [])
    expected_default_positions = {
        0: "&kp ESC",
        11: "&kp BSPC",
        12: "&kp CAPS",
        35: "&kp LCTRL",
        36: "&kp LALT",
        37: "&mo RSE",
        38: "&kp LGUI",
        39: "&kp SPACE",
        40: "&mo LWR",
        41: "&kp RET",
    }
    for index, expected in expected_default_positions.items():
        actual = default[index] if len(default) > index else "<missing>"
        if actual != expected:
            errors.append(f"default_layer position {index}: expected {expected}, found {actual}")

    required_text = [
        '#include <dt-bindings/zmk/outputs.h>',
        '#include <dt-bindings/zmk/rgb.h>',
        'compatible = "zmk,conditional-layers"',
        "if-layers = <LWR RSE>",
        "then-layer = <ADJ>",
        "left outer->inner: LALT, RAISE, CMD; right inner->outer: SPACE, LOWER, ENTER.",
        "inner-left thumb",
        "Space on the inner-right thumb",
        "pinned/upstream ZMK Corne nice_nano overlay defines &led_strip",
        "&led_strip",
        "chain-length = <27>",
    ]
    for token in required_text:
        if token not in text:
            errors.append(f"missing required keymap text: {token}")

    adjust = parsed.get("adjust_layer", [])
    required_adjust_bindings = [
        "&bt BT_SEL 0", "&bt BT_SEL 1", "&bt BT_SEL 2", "&bt BT_SEL 3", "&bt BT_SEL 4", "&bt BT_CLR",
        "&rgb_ug RGB_EFF", "&rgb_ug RGB_TOG", "&rgb_ug RGB_ON", "&rgb_ug RGB_OFF", "&rgb_ug RGB_HUI", "&rgb_ug RGB_SAI",
        "&out OUT_USB", "&out OUT_BLE", "&out OUT_TOG",
        "&bootloader", "&sys_reset",
    ]
    for binding in required_adjust_bindings:
        if binding not in adjust:
            errors.append(f"adjust_layer missing {binding}")

    expected_adjust_positions = {
        30: "&out OUT_USB",
        31: "&out OUT_BLE",
        32: "&out OUT_TOG",
        34: "&bootloader",
        35: "&sys_reset",
    }
    for index, expected in expected_adjust_positions.items():
        actual = adjust[index] if len(adjust) > index else "<missing>"
        if actual != expected:
            errors.append(f"adjust_layer position {index}: expected {expected}, found {actual}")

    obsolete_thumb_phrases = ("outer-" "right thumb", "right outer" "->inner")
    for token in ("zmk,behavior-hold-tap", "CONFIG_WS2812_STRIP", "&kp RGUI", *obsolete_thumb_phrases):
        if token in text:
            errors.append(f"obsolete/forbidden token remains: {token}")

    if errors:
        fail(errors)
    print("Keymap check passed: four 42-binding layers, required thumb rows, ADJ BT/RGB/output controls, and LED chain-length 27 are present.")


if __name__ == "__main__":
    main()
