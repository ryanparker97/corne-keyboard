#!/usr/bin/env python3
"""Validate the native-wireless ZMK build matrix and documented local commands."""
from __future__ import annotations

from pathlib import Path

EXPECTED_BOARD = "nice_nano/nrf52840/zmk"
LEGACY_BOARD = "nice_nano" + "_v2"
EXPECTED_ENTRIES = {
    (EXPECTED_BOARD, "corne_left nice_oled", "corne_v4_left", "", ""),
    (EXPECTED_BOARD, "corne_right nice_oled", "corne_v4_right", "", ""),
    (EXPECTED_BOARD, "settings_reset", "settings_reset", "", ""),
}
README_SNIPPETS = [
    "`corne_v4_left`",
    "`corne_v4_right`",
    "`settings_reset`",
    "`nice_nano/nrf52840/zmk`",
    "`corne_left nice_oled`",
    "`corne_right nice_oled`",
    "generic Corne shields rather than a separate `corne_v4` shield",
    "Normal firmware artifacts type over Bluetooth LE only",
    "`CONFIG_ZMK_USB=n`",
    "No normal artifact enables ZMK Studio",
    "bootloader volume over USB",
    'west build -s zmk/app -d build/corne_left -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_left nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"',
    'west build -s zmk/app -d build/corne_right -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_right nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"',
    'west build -s zmk/app -d build/settings_reset -b nice_nano/nrf52840/zmk -- -DSHIELD="settings_reset" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"',
]


def parse_include_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in text.splitlines():
        stripped = raw_line.split("#", 1)[0].strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            if current is not None:
                entries.append(current)
            current = {}
            stripped = stripped[2:].strip()
        if current is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip().strip('"\'')
    if current is not None:
        entries.append(current)
    return entries


def entry_tuple(entry: dict[str, str]) -> tuple[str, str, str, str, str]:
    return (
        entry.get("board", ""),
        entry.get("shield", ""),
        entry.get("artifact-name", ""),
        entry.get("snippet", ""),
        entry.get("cmake-args", ""),
    )


def main() -> None:
    build_text = Path("build.yaml").read_text(encoding="utf-8")
    readme_text = Path("README.md").read_text(encoding="utf-8")
    config_text = Path("config/corne.conf").read_text(encoding="utf-8")
    entries = parse_include_entries(build_text)
    matrix = {entry_tuple(entry) for entry in entries if entry}
    errors: list[str] = []
    if matrix != EXPECTED_ENTRIES:
        errors.append(f"build.yaml matrix mismatch: {matrix}")
    if len(entries) != len(EXPECTED_ENTRIES):
        errors.append(f"build.yaml should contain {len(EXPECTED_ENTRIES)} include entries, found {len(entries)}")
    if LEGACY_BOARD in build_text + readme_text:
        errors.append(f"legacy {LEGACY_BOARD} target found")
    for stale in ("corne_v4_left_studio", "corne_v4_right_studio", "studio-rpc-usb-uart"):
        if stale in build_text + readme_text:
            errors.append(f"Studio artifact/snippet found: {stale}")
    for symbol in ("CONFIG_ZMK_STUDIO=y", "CONFIG_ZMK_USB=y", "CONFIG_ZMK_USB_BOOT=y"):
        if symbol in build_text + config_text:
            errors.append(f"normal config/build must not enable {symbol}")
    if "CONFIG_ZMK_USB=n" not in config_text:
        errors.append("shared config/corne.conf must explicitly disable CONFIG_ZMK_USB")
    if "cmake-args" in build_text or "snippet:" in build_text:
        errors.append("normal build matrix must not contain cmake-args or snippets")
    for stale in ("corne_v3_1_left", "corne_v3_1_right", "corne_v3_1_left_studio"):
        if stale in build_text + readme_text:
            errors.append(f"stale artifact name found: {stale}")
    for snippet in README_SNIPPETS:
        if snippet not in readme_text:
            errors.append(f"README missing snippet: {snippet}")
    if errors:
        raise SystemExit("Build metadata check failed:\n- " + "\n- ".join(errors))
    print("Build metadata check passed: Corne v4 left/right BLE-only artifacts and settings_reset are documented and validated.")


if __name__ == "__main__":
    main()
