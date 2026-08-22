#!/usr/bin/env python3
"""Validate the ZMK build matrix and documented local commands."""
from __future__ import annotations

from pathlib import Path

EXPECTED_BOARD = "nice_nano/nrf52840/zmk"
LEGACY_BOARD = "nice_nano" + "_v2"
RIGHT_STUDIO_ARTIFACT = "corne_v4_right" + "_studio"
EXPECTED_ENTRIES = {
    (
        EXPECTED_BOARD,
        "corne_left nice_oled",
        "corne_v4_left",
        "",
        "-DCONFIG_ZMK_USB=y -DCONFIG_ZMK_USB_BOOT=y",
    ),
    (EXPECTED_BOARD, "corne_right nice_oled", "corne_v4_right", "", ""),
    (
        EXPECTED_BOARD,
        "corne_left nice_oled",
        "corne_v4_left_studio",
        "studio-rpc-usb-uart",
        "-DCONFIG_ZMK_STUDIO=y -DCONFIG_ZMK_USB=y -DCONFIG_ZMK_USB_BOOT=y",
    ),
    (EXPECTED_BOARD, "settings_reset", "settings_reset", "", ""),
}
README_SNIPPETS = [
    "`corne_v4_left`",
    "`corne_v4_right`",
    "`corne_v4_left_studio`",
    "`settings_reset`",
    "`nice_nano/nrf52840/zmk`",
    "`corne_left nice_oled`",
    "`corne_right nice_oled`",
    "generic Corne shields rather than a separate `corne_v4` shield",
    "`studio-rpc-usb-uart`",
    "`CONFIG_ZMK_STUDIO`",
    "`CONFIG_ZMK_USB`",
    "`CONFIG_ZMK_USB_BOOT`",
    "plug USB into the left half",
    "right half still talks to the left half over split BLE",
    'west build -s zmk/app -d build/corne_left -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_left nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD" -DCONFIG_ZMK_USB=y -DCONFIG_ZMK_USB_BOOT=y',
    'west build -s zmk/app -d build/corne_right -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_right nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"',
    'west build -s zmk/app -d build/corne_left_studio -b nice_nano/nrf52840/zmk -S studio-rpc-usb-uart -- -DSHIELD="corne_left nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD" -DCONFIG_ZMK_STUDIO=y -DCONFIG_ZMK_USB=y -DCONFIG_ZMK_USB_BOOT=y',
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
    if RIGHT_STUDIO_ARTIFACT in build_text + readme_text:
        errors.append("right-hand Studio artifact found")
    for symbol in ("CONFIG_ZMK_STUDIO", "CONFIG_ZMK_USB", "CONFIG_ZMK_USB_BOOT"):
        if symbol in config_text:
            errors.append(f"{symbol} must not appear in shared config/corne.conf")
    for stale in ("corne_v3_1_left", "corne_v3_1_right", "corne_v3_1_left_studio"):
        if stale in build_text + readme_text:
            errors.append(f"stale artifact name found: {stale}")
    for snippet in README_SNIPPETS:
        if snippet not in readme_text:
            errors.append(f"README missing snippet: {snippet}")
    if errors:
        raise SystemExit("Build metadata check failed:\n- " + "\n- ".join(errors))
    print("Build metadata check passed: Corne v4 left, right, left Studio, and settings_reset artifacts are documented and validated.")


if __name__ == "__main__":
    main()
