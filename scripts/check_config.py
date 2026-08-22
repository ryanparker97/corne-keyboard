#!/usr/bin/env python3
"""Validate supported ZMK/nice_oled Kconfig choices for this Corne."""
from __future__ import annotations

import re
from pathlib import Path

SHARED_CONFIG = Path("config/corne.conf")
LEFT_CONFIG = Path("config/corne_left.conf")
RIGHT_CONFIG = Path("config/corne_right.conf")
BUILD_YAML = Path("build.yaml")

SHARED_REQUIRED = {
    "CONFIG_ZMK_DISPLAY": "y",
    "CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM": "y",
    "CONFIG_NICE_OLED_ON": "y",
    "CONFIG_NICE_OLED_WIDGET_STATUS": "y",
    "CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL": "y",
    "CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CAT": "y",
    "CONFIG_ZMK_STUDIO": "y",
    "CONFIG_ZMK_STUDIO_LOCKING": "n",
    "CONFIG_ZMK_STUDIO_LOCK_ON_DISCONNECT": "n",
}

LEFT_REQUIRED = {
    "CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS": "y",
    "CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED": "y",
    "CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_SYMBOL": "y",
    "CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_SYMBOL_MACOS": "y",
    "CONFIG_NICE_OLED_WIDGET_HID_INDICATORS": "y",
    "CONFIG_ZMK_HID_INDICATORS": "y",
    "CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_BONGO_CAT": "y",
    "CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_BONGO_CAT_ONLY_CAPSLOCK": "y",
}

CENTRAL_ONLY_SYMBOLS = set(LEFT_REQUIRED)

FORBIDDEN_EXACT = {
    "CONFIG_ZMK_USB": "y",
    "CONFIG_ZMK_USB_BOOT": "y",
    "CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_LETTER": "y",
    "CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_SYMBOL_WINDOWS": "y",
    "CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_LUNA": "y",
}
ASSIGNMENT = re.compile(r"^(CONFIG_[A-Za-z0-9_]+)\s*=\s*(.*?)\s*$")


def active_assignments(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        match = ASSIGNMENT.match(line)
        if match:
            result.setdefault(match.group(1), []).append(match.group(2).strip())
    return result


def require_values(path: Path, assignments: dict[str, list[str]], required: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for symbol, expected in required.items():
        values = assignments.get(symbol, [])
        if not values:
            errors.append(f"{path}: missing {symbol}={expected}")
        elif any(value != expected for value in values):
            errors.append(f"{path}: {symbol} must be {expected}; found {values}")
    return errors


def forbid_values(path: Path, assignments: dict[str, list[str]], forbidden: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for symbol, forbidden_value in forbidden.items():
        if forbidden_value in assignments.get(symbol, []):
            errors.append(f"{path}: forbidden active assignment: {symbol}={forbidden_value}")
    return errors


def main() -> None:
    shared_text = SHARED_CONFIG.read_text(encoding="utf-8")
    shared_assignments = active_assignments(shared_text)
    errors: list[str] = []

    errors.extend(require_values(SHARED_CONFIG, shared_assignments, SHARED_REQUIRED))
    errors.extend(forbid_values(SHARED_CONFIG, shared_assignments, FORBIDDEN_EXACT))

    for symbol in CENTRAL_ONLY_SYMBOLS:
        if symbol in shared_assignments:
            errors.append(f"{SHARED_CONFIG}: central-only {symbol} must move to {LEFT_CONFIG}")

    for symbol in ("CONFIG_ZMK_USB", "CONFIG_ZMK_USB_BOOT"):
        if re.search(rf"\b{re.escape(symbol)}\b", shared_text):
            errors.append(f"{symbol} must not appear in shared {SHARED_CONFIG}; build.yaml adds it only to left-side artifacts")

    if not LEFT_CONFIG.exists():
        errors.append(f"missing left/central-only config: {LEFT_CONFIG}")
    else:
        left_assignments = active_assignments(LEFT_CONFIG.read_text(encoding="utf-8"))
        errors.extend(require_values(LEFT_CONFIG, left_assignments, LEFT_REQUIRED))
        errors.extend(forbid_values(LEFT_CONFIG, left_assignments, FORBIDDEN_EXACT))

    if RIGHT_CONFIG.exists():
        right_assignments = active_assignments(RIGHT_CONFIG.read_text(encoding="utf-8"))
        for symbol in CENTRAL_ONLY_SYMBOLS:
            if symbol in right_assignments:
                errors.append(f"{RIGHT_CONFIG}: central-only {symbol} must not be assigned for the right/peripheral half")

    build_text = BUILD_YAML.read_text(encoding="utf-8")
    if "EXTRA_CONF_FILE" in build_text:
        errors.append("build.yaml must not use EXTRA_CONF_FILE for side-specific config; ZMK_CONFIG shield config discovery handles this")

    if errors:
        raise SystemExit("Config check failed:\n- " + "\n- ".join(errors))
    print("Config check passed: shared OLED/cat settings are peripheral-safe; left-only config enables Mac modifier icons and CapsLock bongo indicator without shared USB settings.")


if __name__ == "__main__":
    main()
