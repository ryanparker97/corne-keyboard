#!/usr/bin/env python3
"""Validate supported ZMK Kconfig choices for the current Corne config."""
from __future__ import annotations

import re
from pathlib import Path

CONFIG = Path("config/corne.conf")

REQUIRED = {
    "CONFIG_EC11": "n",
    "CONFIG_EC11_TRIGGER_GLOBAL_THREAD": "n",
    "CONFIG_BT_PERIPHERAL_PREF_MIN_INT": "6",
    "CONFIG_BT_PERIPHERAL_PREF_MAX_INT": "12",
    "CONFIG_BT_PERIPHERAL_PREF_LATENCY": "0",
    "CONFIG_BT_CTLR_PHY_2M": "y",
    "CONFIG_BT_CTLR_TX_PWR_PLUS_8": "y",
    "CONFIG_BT_BUF_ACL_RX_SIZE": "512",
    "CONFIG_BT_CTLR_DATA_LENGTH_MAX": "251",
    "CONFIG_BT_GATT_ENFORCE_SUBSCRIPTION": "n",
    "CONFIG_ZMK_RGB_UNDERGLOW": "n",
    "CONFIG_ZMK_DISPLAY": "y",
    "CONFIG_ZMK_DISPLAY_WORK_QUEUE_DEDICATED": "y",
    "CONFIG_ZMK_IDLE_TIMEOUT": "60000",
    "CONFIG_ZMK_SLEEP": "y",
    "CONFIG_ZMK_IDLE_SLEEP_TIMEOUT": "300000",
    "CONFIG_ZMK_EXT_POWER": "y",
}
FORBIDDEN_ENABLED = {
    "CONFIG_ZMK_STUDIO",
    "CONFIG_ZMK_USB_BOOT",
    "CONFIG_KCONFIG_WARNINGS_AS_ERRORS",
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


def optional_text(path: str) -> str | None:
    file = Path(path)
    if not file.exists():
        return None
    return file.read_text(encoding="utf-8")


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

    for symbol in FORBIDDEN_ENABLED:
        if "y" in assignments.get(symbol, []):
            errors.append(f"forbidden active assignment: {symbol}=y")

    for symbol, values in assignments.items():
        if symbol.startswith("CONFIG_ZMK_RGB_UNDERGLOW") and symbol != "CONFIG_ZMK_RGB_UNDERGLOW":
            if any(value == "y" for value in values):
                errors.append(f"forbidden active RGB underglow option: {symbol}=y")

    oled_source = optional_text("src/display/corne_oled_status_screen.c")
    if oled_source is not None:
        for stale in ("zmk_ble_active_profile_name", "CONFIG_ZMK_WIDGET_WPM_STATUS"):
            if stale in oled_source:
                errors.append(f"OLED source must not use unsupported/stale widget API: {stale}")

    # Root module files are optional in this user-config repository. If present,
    # validate their internal wiring, but do not require missing Kconfig or CMake
    # files just because zephyr/module.yml exists.
    optional_module_checks = {
        "Kconfig": ("config CORNE_SIMPLE_OLED_STATUS_SCREEN", "select LV_USE_LABEL"),
        "CMakeLists.txt": ("CONFIG_CORNE_SIMPLE_OLED_STATUS_SCREEN", "src/display/corne_oled_status_screen.c"),
    }
    for path, snippets in optional_module_checks.items():
        haystack = optional_text(path)
        if haystack is None:
            continue
        for snippet in snippets:
            if snippet not in haystack:
                errors.append(f"{path} missing {snippet}")

    if errors:
        raise SystemExit("Config check failed:\n- " + "\n- ".join(errors))
    print("Config check passed: current encoder-off, low-latency BLE, RGB-disabled, display, sleep, and external-power settings are active.")


if __name__ == "__main__":
    main()
