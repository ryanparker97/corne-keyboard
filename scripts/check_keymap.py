#!/usr/bin/env python3
"""Validate the exact four-layer Windows data/DevOps Corne keymap."""
from __future__ import annotations

import re
from pathlib import Path

KEYMAP = Path("config/corne.keymap")

EXPECTED_LAYERS = {
    "base_layer": [
        "&kp ESC", "&kp Q", "&kp W", "&kp E", "&kp R", "&kp T",
        "&kp Y", "&kp U", "&kp I", "&kp O", "&kp P", "&kp BSPC",
        "&kp TAB", "&kp A", "&kp S", "&kp D", "&kp F", "&kp G",
        "&kp H", "&kp J", "&kp K", "&kp L", "&kp SEMI", "&kp SQT",
        "&kp LSHFT", "&kp Z", "&kp X", "&kp C", "&kp V", "&kp B",
        "&kp N", "&kp M", "&kp COMMA", "&kp DOT", "&kp FSLH", "&kp LWIN",
        "&kp LALT", "&mo RAISE", "&kp LCTRL", "&kp SPACE", "&mo LOWER", "&kp RET",
    ],
    "lower_layer": [
        "&kp GRAVE", "&kp N1", "&kp N2", "&kp N3", "&kp N4", "&kp N5",
        "&kp N6", "&kp N7", "&kp N8", "&kp N9", "&kp N0", "&kp DEL",
        "&vim_window_prefix", "&kp LCTRL", "&kp LALT", "&kp LWIN", "&kp LSHFT",
        "&tmux_prefix", "&kp LEFT", "&kp DOWN", "&kp UP", "&kp RIGHT",
        "&kp PG_DN", "&kp PG_UP", "&kp F1", "&kp F2", "&kp F3", "&kp F4",
        "&kp F5", "&kp F6", "&kp F7", "&kp F8", "&kp F9", "&kp F10",
        "&kp F11", "&kp F12", "&kp LCTRL", "&mo RAISE", "&kp LWIN",
        "&kp SPACE", "&mo LOWER", "&kp RET",
    ],
    "raise_layer": [
        "&kp TILDE", "&kp EXCL", "&kp AT", "&kp HASH", "&kp DLLR", "&kp PRCNT",
        "&kp CARET", "&kp AMPS", "&kp STAR", "&kp LPAR", "&kp RPAR", "&kp QUESTION",
        "&kp MINUS", "&kp LCTRL", "&kp LALT", "&kp LWIN", "&kp LSHFT", "&kp EQUAL",
        "&kp LBKT", "&kp LBRC", "&kp COLON", "&kp PIPE", "&kp RBRC", "&kp RBKT",
        "&kp BSLH", "&kp SQT", "&kp DQT", "&kp UNDER", "&kp PLUS", "&kp GRAVE",
        "&kp LT", "&kp GT", "&kp COMMA", "&kp DOT", "&kp FSLH", "&kp SEMI",
        "&kp LCTRL", "&mo RAISE", "&kp LWIN", "&kp SPACE", "&mo LOWER", "&kp RET",
    ],
    "adjust_layer": [
        "&bootloader", "&bt BT_SEL 0", "&bt BT_SEL 1", "&bt BT_SEL 2",
        "&bt BT_SEL 3", "&bt BT_SEL 4", "&kp PSCRN", "&kp LG(LS(S))",
        "&kp LG(S)", "&kp LG(LC(LEFT))", "&kp LG(LC(RIGHT))", "&kp LG(L)",
        "&bt BT_CLR", "&kp C_PREV", "&kp C_PP", "&kp C_NEXT", "&kp C_MUTE",
        "&kp C_VOL_DN", "&none", "&none", "&caps_word", "&kp CAPS", "&none", "&none",
        "&sys_reset", "&kp C_BRI_DN", "&kp C_BRI_UP", "&out OUT_USB", "&out OUT_BLE",
        "&kp C_VOL_UP", "&out OUT_TOG", "&none", "&none", "&none", "&none", "&none",
        "&kp LCTRL", "&mo RAISE", "&kp LWIN", "&kp SPACE", "&mo LOWER", "&kp RET",
    ],
}

REQUIRED_SNIPPETS = (
    '#include <dt-bindings/zmk/outputs.h>',
    "#define BASE   0", "#define LOWER  1", "#define RAISE  2", "#define ADJUST 3",
    'compatible = "zmk,conditional-layers"',
    "if-layers = <LOWER RAISE>", "then-layer = <ADJUST>",
    'display-name = "Base"', 'display-name = "Nav/Num"',
    'display-name = "Symbols"', 'display-name = "System"',
)

MACROS = {
    "vim_window_prefix": "&kp LC(W)",
    "tmux_prefix": "&kp LC(B)",
}

FORBIDDEN_SNIPPETS = (
    "dt-bindings/zmk/rgb.h", "&rgb_ug", "RGB_", "&led_strip", "chain-length",
    "&kscan0", "debounce-press-ms", "debounce-release-ms",
    'compatible = "zmk,behavior-hold-tap"', "&hm_l", "&hm_r",
    "&kp LGUI", "&kp LCMD", "&kp LG(LS(N5))", "&kp LG(SPACE)",
    "&kp LG(TAB)", "&kp LC(LG(Q))", "&kp LW(", "LG(DOT)",
)


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    return re.sub(r"//.*", "", text)


def parse_bindings(text: str, layer: str) -> list[str]:
    match = re.search(rf"{layer}\s*\{{[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;", text)
    if not match:
        return []
    return [
        " ".join(binding.split())
        for binding in re.findall(r"&[A-Za-z0-9_]+(?:\s+[^&\s]+)*", match.group(1))
    ]


def validate_macro(text: str, name: str, binding: str) -> list[str]:
    match = re.search(rf"{name}:\s*{name}\s*\{{([\s\S]*?)\}};", text)
    if not match:
        return [f"missing {name} macro definition"]
    body = match.group(1)
    required = (
        'compatible = "zmk,behavior-macro"', "#binding-cells = <0>",
        "wait-ms = <0>", "tap-ms = <30>", f"bindings = <{binding}>",
    )
    return [f"{name}: missing exact macro setting: {item}" for item in required if item not in body]


def main() -> None:
    text = KEYMAP.read_text(encoding="utf-8")
    code = strip_comments(text)
    errors: list[str] = []

    if code.count("{") != code.count("}"):
        errors.append("unbalanced braces")
    if code.count("<") != code.count(">"):
        errors.append("unbalanced angle brackets")

    errors.extend(
        f"missing required architecture: {snippet}"
        for snippet in REQUIRED_SNIPPETS if snippet not in code
    )
    errors.extend(
        f"forbidden stale hardware/macOS/HRM content: {snippet}"
        for snippet in FORBIDDEN_SNIPPETS if snippet in code
    )
    for name, binding in MACROS.items():
        errors.extend(validate_macro(code, name, binding))
    if code.count('compatible = "zmk,behavior-macro"') != len(MACROS):
        errors.append("expected exactly the Vim Ctrl-W and tmux Ctrl-B macros")

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
        "Keymap check passed: exact four-layer 42-key Windows data/DevOps geometry, "
        "prefix macros, disabled RGB policy, and guarded controls verified."
    )


if __name__ == "__main__":
    main()
