#!/usr/bin/env python3
"""Static sanity checks for the Corne ZMK keymap."""
from __future__ import annotations

import re
from pathlib import Path

KEYMAP = Path("config/corne.keymap")
EXPECTED_LAYERS = ("default_layer", "lower_layer", "raise_layer", "adjust_layer")
EXPECTED_THUMBS = ["&kp LALT", "&mo RSE", "&kp SPACE", "&kp RWIN", "&mo LWR", "&kp RET"]


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
        38: "&kp SPACE",
        39: "&kp RWIN",
        40: "&mo LWR",
        41: "&kp RET",
    }
    for index, expected in expected_default_positions.items():
        actual = default[index] if len(default) > index else "<missing>"
        if actual != expected:
            errors.append(f"default_layer position {index}: expected {expected}, found {actual}")

    required_text = [
        '#include <dt-bindings/zmk/outputs.h>',
        'compatible = "zmk,conditional-layers"',
        "if-layers = <LWR RSE>",
        "then-layer = <ADJ>",
        "left outer->inner: LALT, RAISE, SPACE; right inner->outer: RWIN, LOWER, ENTER.",
        "Windows key (RWIN) on the inner-right thumb",
        "Windows utility top-right order",
        "Media right home order",
    ]
    for token in required_text:
        if token not in text:
            errors.append(f"missing required keymap text: {token}")

    adjust = parsed.get("adjust_layer", [])
    required_adjust_bindings = [
        "&bt BT_SEL 0", "&bt BT_SEL 1", "&bt BT_SEL 2", "&bt BT_SEL 3", "&bt BT_SEL 4", "&bt BT_CLR",
        "&kp PSCRN", "&kp LG(LS(S))", "&kp LG(V)", "&kp LG(S)", "&kp LG(TAB)", "&kp LG(L)",
        "&kp C_PREV", "&kp C_PP", "&kp C_NEXT", "&kp C_MUTE", "&kp C_VOL_DN", "&kp C_VOL_UP",
        "&out OUT_USB", "&out OUT_BLE", "&out OUT_TOG",
        "&bootloader", "&sys_reset",
    ]
    for binding in required_adjust_bindings:
        if binding not in adjust:
            errors.append(f"adjust_layer missing {binding}")

    expected_adjust_positions = {
        6: "&kp PSCRN",
        7: "&kp LG(LS(S))",
        8: "&kp LG(V)",
        9: "&kp LG(S)",
        10: "&kp LG(TAB)",
        11: "&kp LG(L)",
        18: "&kp C_PREV",
        19: "&kp C_PP",
        20: "&kp C_NEXT",
        21: "&kp C_MUTE",
        22: "&kp C_VOL_DN",
        23: "&kp C_VOL_UP",
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
    for token in (
        "zmk,behavior-hold-tap",
        "CONFIG_WS2812_STRIP",
        "#include <dt-bindings/zmk/rgb.h>",
        "&rgb_ug",
        "&led_strip",
        "chain-length",
        "&kp RGUI",
        "RGUI",
        "macOS",
        "Command",
        *obsolete_thumb_phrases,
    ):
        if token in text:
            errors.append(f"obsolete/forbidden token remains: {token}")

    if errors:
        fail(errors)
    print("Keymap check passed: four 42-binding layers, RWIN thumbs, Windows ADJ utilities/media, output controls, and no RGB/LED override are present.")


if __name__ == "__main__":
    main()
