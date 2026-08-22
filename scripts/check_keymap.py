#!/usr/bin/env python3
"""Static sanity checks for the Corne ZMK keymap."""
from __future__ import annotations

import re
from pathlib import Path

KEYMAP = Path("config/corne.keymap")
EXPECTED_LAYERS = ("default_layer", "lower_layer", "raise_layer", "adjust_layer")
DEFAULT_THUMBS = ["&kp LALT", "&mo RSE", "&kp LWIN", "&kp SPACE", "&mo LWR", "&kp RET"]
LOWER_THUMBS = ["&kp LCTRL", "&trans", "&trans", "&trans", "&trans", "&trans"]
TRANSPARENT_THUMBS = ["&trans"] * 6


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


def joined(*parts: str) -> str:
    return "".join(parts)


def expect_positions(bindings: list[str], expected: dict[int, str], layer: str, errors: list[str]) -> None:
    for index, value in expected.items():
        actual = bindings[index] if len(bindings) > index else "<missing>"
        if actual != value:
            errors.append(f"{layer} position {index}: expected {value}, found {actual}")


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

    thumb_expectations = {
        "default_layer": DEFAULT_THUMBS,
        "lower_layer": LOWER_THUMBS,
        "raise_layer": TRANSPARENT_THUMBS,
        "adjust_layer": TRANSPARENT_THUMBS,
    }
    for layer, expected in thumb_expectations.items():
        bindings = parsed.get(layer, [])
        actual = bindings[36:42] if len(bindings) >= 42 else []
        if actual != expected:
            errors.append(f"{layer}: expected thumb row {expected}, found {actual}")

    expect_positions(parsed.get("default_layer", []), {
        0: "&kp ESC",
        11: "&kp BSPC",
        12: "&kp CAPS",
        35: "&kp LCTRL",
        36: "&kp LALT",
        37: "&mo RSE",
        38: "&kp LWIN",
        39: "&kp SPACE",
        40: "&mo LWR",
        41: "&kp RET",
    }, "default_layer", errors)

    expect_positions(parsed.get("lower_layer", []), {
        0: "&kp GRAVE",
        12: "&kp TAB",
        22: "&kp PG_UP",
        24: "&kp LALT",
        30: "&kp HOME",
        31: "&kp PG_DN",
        32: "&kp PG_UP",
        36: "&kp LCTRL",
        37: "&trans",
        41: "&trans",
    }, "lower_layer", errors)

    expect_positions(parsed.get("raise_layer", []), {
        12: "&kp ESC",
        13: "&kp MINUS",
        18: "&kp LC(LEFT)",
        19: "&kp LC(DOWN)",
        20: "&kp LC(UP)",
        21: "&kp LC(RIGHT)",
        24: "&kp LALT",
        36: "&trans",
        41: "&trans",
    }, "raise_layer", errors)

    required_text = [
        '#include <dt-bindings/zmk/outputs.h>',
        'compatible = "zmk,conditional-layers"',
        "if-layers = <LWR RSE>",
        "then-layer = <ADJ>",
        "left outer->inner: LALT, RAISE, LWIN; right inner->outer: SPACE, LOWER, ENTER.",
        "Windows utility top-right order",
        "Editing left side",
        "Media right home order",
        "Output bottom-right order",
    ]
    for token in required_text:
        if token not in text:
            errors.append(f"missing required keymap text: {token}")

    adjust = parsed.get("adjust_layer", [])
    required_adjust_bindings = [
        "&bt BT_SEL 0", "&bt BT_SEL 1", "&bt BT_SEL 2", "&bt BT_SEL 3", "&bt BT_SEL 4", "&bt BT_CLR",
        "&kp PSCRN", "&kp LG(LS(S))", "&kp LG(V)", "&kp LG(S)", "&kp LG(TAB)", "&kp LG(L)",
        "&kp LC(A)", "&kp LC(S)", "&kp LC(F)", "&kp LC(Z)", "&kp LC(X)", "&kp LC(C)", "&kp LC(V)", "&kp LC(Y)",
        "&kp C_PREV", "&kp C_PP", "&kp C_NEXT", "&kp C_MUTE", "&kp C_VOL_DN", "&kp C_VOL_UP",
        "&out OUT_USB", "&out OUT_BLE", "&out OUT_TOG",
        "&bootloader", "&sys_reset",
    ]
    for binding in required_adjust_bindings:
        if binding not in adjust:
            errors.append(f"adjust_layer missing {binding}")

    expect_positions(adjust, {
        6: "&kp PSCRN",
        7: "&kp LG(LS(S))",
        8: "&kp LG(V)",
        9: "&kp LG(S)",
        10: "&kp LG(TAB)",
        11: "&kp LG(L)",
        13: "&kp LC(A)",
        14: "&kp LC(S)",
        16: "&kp LC(F)",
        18: "&kp C_PREV",
        19: "&kp C_PP",
        20: "&kp C_NEXT",
        21: "&kp C_MUTE",
        22: "&kp C_VOL_DN",
        23: "&kp C_VOL_UP",
        25: "&kp LC(Z)",
        26: "&kp LC(X)",
        27: "&kp LC(C)",
        28: "&kp LC(V)",
        29: "&kp LC(Y)",
        30: "&out OUT_USB",
        31: "&out OUT_BLE",
        32: "&out OUT_TOG",
        34: "&bootloader",
        35: "&sys_reset",
    }, "adjust_layer", errors)

    obsolete_thumb_phrases = ("outer-" "right thumb", "right outer" "->inner")
    forbidden_tokens = (
        "zmk,behavior-hold-tap",
        "CONFIG_WS2812_STRIP",
        "#include <dt-bindings/zmk/rgb.h>",
        "&rgb_ug",
        "&led_strip",
        "chain-length",
        joined("m", "acOS"),
        joined("M", "ac"),
        joined("Kara", "biner"),
        joined("s", "khd"),
        joined("ya", "bai"),
        joined("Com", "mand"),
        joined("L", "GUI"),
        joined("R", "GUI"),
        joined("m", "acos"),
        *obsolete_thumb_phrases,
    )
    for token in forbidden_tokens:
        if token in text:
            errors.append(f"obsolete/forbidden token remains: {token}")

    if errors:
        fail(errors)
    print("Keymap check passed: four 42-binding layers, NJ68 Windows thumbs, converted utility/editing chords, media/output controls, and disabled RGB are present.")


if __name__ == "__main__":
    main()
