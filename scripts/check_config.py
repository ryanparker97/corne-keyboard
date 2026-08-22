#!/usr/bin/env python3
"""Validate supported ZMK Kconfig choices for this wireless Corne."""
from __future__ import annotations

import re
from pathlib import Path

CONFIG = Path("config/corne.conf")

REQUIRED = {
    "CONFIG_ZMK_RGB_UNDERGLOW": "y",
    "CONFIG_ZMK_RGB_UNDERGLOW_ON_START": "n",
    "CONFIG_ZMK_RGB_UNDERGLOW_BRT_START": "15",
    "CONFIG_ZMK_RGB_UNDERGLOW_BRT_MAX": "40",
    "CONFIG_ZMK_RGB_UNDERGLOW_AUTO_OFF_IDLE": "y",
    "CONFIG_ZMK_DISPLAY": "y",
    "CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM": "y",
    "CONFIG_NICE_OLED_ON": "y",
    "CONFIG_NICE_OLED_WIDGET_STATUS": "y",
    "CONFIG_NICE_OLED_WIDGET_WPM": "y",
    "CONFIG_NICE_OLED_WIDGET_WPM_LUNA": "y",
    "CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT": "n",
    "CONFIG_NICE_OLED_WIDGET_RESPONSIVE_BONGO_CAT": "n",
    "CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL": "y",
    "CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CAT": "y",
    "CONFIG_ZMK_SLEEP": "y",
    "CONFIG_ZMK_EXT_POWER": "y",
    "CONFIG_ZMK_BLE": "y",
    "CONFIG_ZMK_BLE_EXPERIMENTAL_FEATURES": "y",
    "CONFIG_ZMK_BLE_EXPERIMENTAL_CONN": "y",
    "CONFIG_BT_PERIPHERAL_PREF_MIN_INT": "12",
    "CONFIG_BT_PERIPHERAL_PREF_MAX_INT": "12",
    "CONFIG_BT_PERIPHERAL_PREF_LATENCY": "30",
    "CONFIG_BT_PERIPHERAL_PREF_TIMEOUT": "600",
    "CONFIG_ZMK_BLE_KEYBOARD_REPORT_QUEUE_SIZE": "40",
    "CONFIG_ZMK_KSCAN_EVENT_QUEUE_SIZE": "16",
    "CONFIG_ZMK_SPLIT_BLE_CENTRAL_POSITION_QUEUE_SIZE": "16",
    "CONFIG_BT_CTLR_TX_PWR_PLUS_8": "y",
    "CONFIG_ZMK_KSCAN_DEBOUNCE_PRESS_MS": "1",
    "CONFIG_ZMK_KSCAN_DEBOUNCE_RELEASE_MS": "5",
    "CONFIG_ZMK_HID_CONSUMER_REPORT_USAGES_BASIC": "y",
    "CONFIG_ZMK_STUDIO": "y",
    "CONFIG_ZMK_STUDIO_LOCKING": "n",
    "CONFIG_ZMK_STUDIO_LOCK_ON_DISCONNECT": "n",
}

FORBIDDEN_PREFIXES = (
    "CONFIG_WS2812_STRIP",
)
FORBIDDEN_EXACT = {
    "CONFIG_ZMK_RGB_UNDERGLOW_AUTO_OFF_USB": "y",
    "CONFIG_ZMK_USB": "y",
    "CONFIG_ZMK_USB_BOOT": "y",
    "CONFIG_KCONFIG_WARNINGS_AS_ERRORS": "n",
    "CONFIG_BT_CTLR_PHY_2M": "y",
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


def main() -> None:
    text = CONFIG.read_text(encoding="utf-8")
    assignments = active_assignments(text)
    errors: list[str] = []

    for symbol, expected in REQUIRED.items():
        values = assignments.get(symbol, [])
        if not values:
            errors.append(f"missing {symbol}={expected}")
        elif any(value != expected for value in values):
            errors.append(f"{symbol} must be {expected}; found {values}")

    for symbol, values in assignments.items():
        if any(symbol.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            errors.append(f"forbidden active symbol: {symbol}")
        if symbol in FORBIDDEN_EXACT and FORBIDDEN_EXACT[symbol] in values:
            errors.append(f"forbidden active assignment: {symbol}={FORBIDDEN_EXACT[symbol]}")

    for symbol in ("CONFIG_ZMK_USB", "CONFIG_ZMK_USB_BOOT"):
        if re.search(rf"\b{re.escape(symbol)}\b", text):
            errors.append(f"{symbol} must not appear in shared {CONFIG}")

    if errors:
        raise SystemExit("Config check failed:\n- " + "\n- ".join(errors))
    print("Config check passed: RGB, BLE, power, nice_oled, debounce, HID, and unlocked Studio settings are active without forbidden USB settings.")


if __name__ == "__main__":
    main()
