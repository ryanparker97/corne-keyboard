#!/usr/bin/env python3
"""Validate supported ZMK Kconfig choices for this wireless Corne."""
from __future__ import annotations

import re
from pathlib import Path

CONFIG = Path("config/corne.conf")

REQUIRED = {
    "CONFIG_ZMK_DISPLAY": "y",
    "CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM": "y",
    "CONFIG_NICE_OLED_ON": "y",
    "CONFIG_NICE_OLED_WIDGET_STATUS": "n",
    "CONFIG_CORNE_SIMPLE_OLED_STATUS_SCREEN": "y",
    "CONFIG_BT_DEVICE_NAME": "\"Corne\"",
    "CONFIG_NICE_OLED_WIDGET_WPM": "n",
    "CONFIG_NICE_OLED_WIDGET_WPM_LUNA": "n",
    "CONFIG_NICE_OLED_WIDGET_WPM_BONGO_CAT": "n",
    "CONFIG_NICE_OLED_WIDGET_RESPONSIVE": "n",
    "CONFIG_NICE_OLED_WIDGET_RESPONSIVE_BONGO_CAT": "n",
    "CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL": "n",
    "CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL_CAT": "n",
    "CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL": "n",
    "CONFIG_NICE_OLED_WIDGET_HID_INDICATORS": "n",
    "CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS": "n",
    "CONFIG_ZMK_SLEEP": "y",
    "CONFIG_ZMK_EXT_POWER": "y",
    "CONFIG_ZMK_BLE": "y",
    "CONFIG_ZMK_USB": "n",
    "CONFIG_ZMK_BLE_EXPERIMENTAL_CONN": "y",
    "CONFIG_BT_PERIPHERAL_PREF_MIN_INT": "12",
    "CONFIG_BT_PERIPHERAL_PREF_MAX_INT": "12",
    "CONFIG_BT_PERIPHERAL_PREF_LATENCY": "30",
    "CONFIG_BT_PERIPHERAL_PREF_TIMEOUT": "600",
    "CONFIG_ZMK_BLE_KEYBOARD_REPORT_QUEUE_SIZE": "40",
    "CONFIG_ZMK_KSCAN_EVENT_QUEUE_SIZE": "16",
    "CONFIG_ZMK_SPLIT_BLE_CENTRAL_POSITION_QUEUE_SIZE": "16",
    "CONFIG_BT_CTLR_PHY_2M": "n",
    "CONFIG_BT_GATT_ENFORCE_SUBSCRIPTION": "n",
}

FORBIDDEN_PREFIXES = (
    "CONFIG_WS2812_STRIP",
    "CONFIG_ZMK_KSCAN_DEBOUNCE_",
    "CONFIG_ZMK_RGB_UNDERGLOW",
)
FORBIDDEN_EXACT = {
    "CONFIG_ZMK_RGB_UNDERGLOW_AUTO_OFF_USB": "y",
    "CONFIG_ZMK_STUDIO": "y",
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
    module_yml = Path("zephyr/module.yml").read_text(encoding="utf-8")
    module_kconfig = Path("Kconfig").read_text(encoding="utf-8")
    module_cmake = Path("CMakeLists.txt").read_text(encoding="utf-8")
    oled_source = Path("src/display/corne_oled_status_screen.c").read_text(encoding="utf-8")
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

    if re.search(r"\bCONFIG_ZMK_STUDIO\b", text):
        errors.append(f"CONFIG_ZMK_STUDIO must not appear in shared {CONFIG}")
    if re.search(r"\bCONFIG_ZMK_USB_BOOT\s*=\s*y\b", text):
        errors.append(f"CONFIG_ZMK_USB_BOOT must not be enabled in shared {CONFIG}")

    for snippet in (
        "Corne v4 + nice!nano wireless settings for Windows hosts",
        "Native-wireless typing only",
        "CONFIG_ZMK_USB=n",
        "RGB underglow/per-key LEDs are intentionally disabled",
        "LVGL9-compatible chyuuu/zmk-nice-oled fork",
        "only layer, Bluetooth status, and CONFIG_BT_DEVICE_NAME",
    ):
        if snippet not in text:
            errors.append(f"config/corne.conf missing comment: {snippet}")

    module_required = {
        "zephyr/module.yml": (module_yml, ("cmake: .", "kconfig: Kconfig", "board_root: .")),
        "Kconfig": (module_kconfig, ("config CORNE_SIMPLE_OLED_STATUS_SCREEN", "select LV_USE_LABEL")),
        "CMakeLists.txt": (module_cmake, ("CONFIG_CORNE_SIMPLE_OLED_STATUS_SCREEN", "src/display/corne_oled_status_screen.c")),
        "src/display/corne_oled_status_screen.c": (
            oled_source,
            (
                "CONFIG_BT_DEVICE_NAME",
                "zmk_keymap_highest_layer_active",
                "zmk_ble_active_profile_is_connected",
                "zmk_split_bt_peripheral_is_connected",
            ),
        ),
    }
    for path, (haystack, snippets) in module_required.items():
        for snippet in snippets:
            if snippet not in haystack:
                errors.append(f"{path} missing {snippet}")

    for stale in ("zmk_ble_active_profile_name", "CONFIG_ZMK_WIDGET_WPM_STATUS"):
        if stale in oled_source:
            errors.append(f"OLED source must not use unsupported/stale widget API: {stale}")

    if errors:
        raise SystemExit("Config check failed:\n- " + "\n- ".join(errors))
    print("Config check passed: Windows BLE, USB-disabled native-wireless power, and simple layer/BLE/name OLED settings are active while RGB underglow remains disabled.")


if __name__ == "__main__":
    main()
