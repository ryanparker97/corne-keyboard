#!/usr/bin/env python3
"""Validate the complete four-layer Windows Corne keymap."""
from __future__ import annotations

import re
from pathlib import Path

KEYMAP = Path("config/corne.keymap")

EXPECTED_LAYERS = {
    "base_layer": [
        "&kp ESC", "&kp Q", "&kp W", "&kp E", "&kp R", "&kp T",
        "&kp Y", "&kp U", "&kp I", "&kp O", "&kp P", "&kp BSPC",
        "&kp TAB", "&hm_l LCTRL A", "&hm_l LALT S", "&hm_l LGUI D",
        "&hm_l LSHFT F", "&kp G", "&kp H", "&hm_r RSHFT J",
        "&hm_r RGUI K", "&hm_r RALT L", "&hm_r RCTRL SEMI", "&kp SQT",
        "&kp LSHFT", "&kp Z", "&kp X", "&kp C", "&kp V", "&kp B",
        "&kp N", "&kp M", "&kp COMMA", "&kp DOT", "&kp FSLH", "&kp RCTRL",
        "&kp LALT", "&mo RAISE", "&kp LCTRL", "&kp SPACE", "&mo LOWER", "&kp RET",
    ],
    "lower_layer": [
        "&kp GRAVE", "&kp N1", "&kp N2", "&kp N3", "&kp N4", "&kp N5",
        "&kp N6", "&kp N7", "&kp N8", "&kp N9", "&kp N0", "&kp DEL",
        "&kp LEFT", "&kp LCTRL", "&kp LALT", "&kp LGUI", "&kp LSHFT", "&kp DOWN",
        "&kp UP", "&kp RSHFT", "&kp RGUI", "&kp RALT", "&kp RCTRL", "&kp RIGHT",
        "&kp F1", "&kp F2", "&kp F3", "&kp F4", "&kp F5", "&kp F6",
        "&kp F7", "&kp F8", "&kp F9", "&kp F10", "&kp F11", "&kp F12",
        "&kp LALT", "&mo RAISE", "&kp LCTRL", "&kp SPACE", "&mo LOWER", "&kp RET",
    ],
    "raise_layer": [
        "&kp TILDE", "&kp EXCL", "&kp AT", "&kp HASH", "&kp DLLR", "&kp PRCNT",
        "&kp CARET", "&kp AMPS", "&kp STAR", "&kp LPAR", "&kp RPAR", "&kp QUESTION",
        "&kp MINUS", "&kp LCTRL", "&kp LALT", "&kp LGUI", "&kp LSHFT", "&kp EQUAL",
        "&kp LBKT", "&kp RSHFT", "&kp RGUI", "&kp RALT", "&kp RCTRL", "&kp RBKT",
        "&kp BSLH", "&kp COLON", "&kp DQT", "&kp UNDER", "&kp PLUS", "&kp LBRC",
        "&kp RBRC", "&kp PIPE", "&kp LT", "&kp GT", "&kp LG(TAB)", "&kp LG(DOT)",
        "&kp LALT", "&mo RAISE", "&kp LCTRL", "&kp SPACE", "&mo LOWER", "&kp RET",
    ],
    "adjust_layer": [
        "&bootloader", "&bt BT_SEL 0", "&bt BT_SEL 1", "&bt BT_SEL 2",
        "&bt BT_SEL 3", "&bt BT_SEL 4", "&kp PSCRN", "&kp LG(LS(S))",
        "&kp LG(S)", "&kp LG(LC(LEFT))", "&kp LG(LC(RIGHT))", "&kp LG(L)",
        "&bt BT_CLR", "&kp C_PREV", "&kp C_PP", "&kp C_NEXT", "&kp C_MUTE",
        "&kp C_VOL_DN", "&none", "&none", "&none", "&kp CAPS", "&none", "&none",
        "&sys_reset", "&kp C_BRI_DN", "&kp C_BRI_UP", "&out OUT_USB", "&out OUT_BLE",
        "&kp C_VOL_UP", "&out OUT_TOG", "&none", "&none", "&none", "&none", "&none",
        "&kp LALT", "&mo RAISE", "&kp LCTRL", "&kp SPACE", "&mo LOWER", "&kp RET",
    ],
}

REQUIRED_SNIPPETS = (
    '#include <dt-bindings/zmk/outputs.h>',
    "#define BASE  0",
    "#define LOWER 1",
    "#define RAISE 2",
    "#define ADJUST 3",
    'compatible = "zmk,behavior-hold-tap"',
    'flavor = "balanced"',
    "tapping-term-ms = <280>",
    "require-prior-idle-ms = <150>",
    "quick-tap-ms = <175>",
    "hold-trigger-on-release",
    'compatible = "zmk,conditional-layers"',
    "if-layers = <LOWER RAISE>",
    "then-layer = <ADJUST>",
)

FORBIDDEN_SNIPPETS = (
    "dt-bindings/zmk/rgb.h",
    "&rgb_ug",
    "RGB_ON",
    "RGB_OFF",
    "RGB_EFF",
    "&led_strip",
    "LG(LS(N3))",
    "LG(LS(N4))",
    "LG(LS(N5))",
    "LC(LG(Q))",
    "LC(LG(SPACE))",
    "LG(GRAVE)",
)

CTRL_THUMB_DIAGRAM = "| ALT  RSE  CTRL | SPC  LWR  RET |"


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    return re.sub(r"//.*", "", text)


def parse_bindings(text: str, layer: str) -> list[str]:
    match = re.search(
        rf"{layer}\s*\{{[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;", text
    )
    if not match:
        return []
    return [
        " ".join(binding.split())
        for binding in re.findall(r"&[A-Za-z0-9_]+(?:\s+[^&\s]+)*", match.group(1))
    ]


def check_opposite_hand_triggers(text: str, errors: list[str]) -> None:
    expected = {
        "hm_l": list(range(6, 12)) + list(range(18, 24)) + list(range(30, 36)) + list(range(39, 42)),
        "hm_r": list(range(0, 6)) + list(range(12, 18)) + list(range(24, 30)) + list(range(36, 39)),
    }
    for behavior, positions in expected.items():
        match = re.search(
            rf"{behavior}:\s*[^{{]+\{{[\s\S]*?hold-trigger-key-positions\s*=\s*<([\s\S]*?)>;",
            text,
        )
        if not match:
            errors.append(f"{behavior}: missing opposite-hand trigger positions")
            continue
        actual = [int(value) for value in re.findall(r"\d+", match.group(1))]
        if actual != positions:
            errors.append(f"{behavior}: trigger positions differ: expected {positions}, found {actual}")


def main() -> None:
    text = KEYMAP.read_text(encoding="utf-8")
    code = strip_comments(text)
    errors: list[str] = []

    if code.count("{") != code.count("}"):
        errors.append("unbalanced braces")
    if code.count("<") != code.count(">"):
        errors.append("unbalanced angle brackets")

    for snippet in REQUIRED_SNIPPETS:
        if snippet not in code:
            errors.append(f"missing required architecture: {snippet}")
    for snippet in FORBIDDEN_SNIPPETS:
        if snippet in code:
            errors.append(f"forbidden stale macOS/RGB binding: {snippet}")

    if code.count('compatible = "zmk,behavior-hold-tap"') != 2:
        errors.append("expected exactly two bilateral hold-tap behaviors")
    if text.count(CTRL_THUMB_DIAGRAM) != 4:
        errors.append("expected all four layer diagrams to show the position 38 Ctrl thumb")
    check_opposite_hand_triggers(code, errors)

    for layer, expected in EXPECTED_LAYERS.items():
        actual = parse_bindings(code, layer)
        if len(actual) != 42:
            errors.append(f"{layer}: expected 42 bindings, found {len(actual)}")
        for index, expected_binding in enumerate(expected):
            actual_binding = actual[index] if index < len(actual) else "<missing>"
            if actual_binding != expected_binding:
                errors.append(
                    f"{layer} position {index}: expected {expected_binding}, found {actual_binding}"
                )

    if errors:
        raise SystemExit("Keymap check failed:\n- " + "\n- ".join(errors))

    print(
        "Keymap check passed: exact four-layer 42-key Windows geometry, bilateral HRMs, "
        "native Windows shortcuts, and guarded BT/output/boot/reset controls verified."
    )


if __name__ == "__main__":
    main()
