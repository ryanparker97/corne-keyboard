#!/usr/bin/env python3
"""Validate the current ZMK build matrix and documented local targets."""
from __future__ import annotations

import re
from pathlib import Path

EXPECTED_BOARD = "nice_nano/nrf52840/zmk"
LEGACY_BOARD = "nice_nano" + "_v2"
EXPECTED_ENTRIES = {
    (EXPECTED_BOARD, "corne_left nice_oled", "corne_v4_left", "", ""),
    (EXPECTED_BOARD, "corne_right nice_oled", "corne_v4_right", "", ""),
    (EXPECTED_BOARD, "settings_reset", "settings_reset", "", ""),
}
REQUIRED_README_SNIPPETS = (
    "`corne_v4_left`",
    "`corne_v4_right`",
    "`settings_reset`",
    "`nice_nano/nrf52840/zmk`",
    "`corne_left nice_oled`",
    "`corne_right nice_oled`",
    "generic Corne shields rather than a separate `corne_v4` shield",
    'west build -s zmk/app -d build/corne_left -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_left nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"',
    'west build -s zmk/app -d build/corne_right -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_right nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"',
    'west build -s zmk/app -d build/settings_reset -b nice_nano/nrf52840/zmk -- -DSHIELD="settings_reset" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"',
)
ASSIGNMENT = re.compile(r"^(CONFIG_[A-Za-z0-9_]+)\s*=\s*(.*?)\s*$")


def uncommented_lines(text: str) -> list[str]:
    """Return non-empty lines with shell/YAML comments removed."""
    result: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if line:
            result.append(line)
    return result


def parse_include_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for stripped in uncommented_lines(text):
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


def active_config_assignments(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for line in uncommented_lines(text):
        match = ASSIGNMENT.match(line)
        if match:
            result.setdefault(match.group(1), []).append(match.group(2).strip())
    return result


def main() -> None:
    build_text = Path("build.yaml").read_text(encoding="utf-8")
    readme_text = Path("README.md").read_text(encoding="utf-8")
    config_text = Path("config/corne.conf").read_text(encoding="utf-8")
    entries = parse_include_entries(build_text)
    matrix = {entry_tuple(entry) for entry in entries if entry}
    config = active_config_assignments(config_text)
    active_build_text = "\n".join(uncommented_lines(build_text))
    errors: list[str] = []

    if matrix != EXPECTED_ENTRIES:
        errors.append(f"build.yaml matrix mismatch: {matrix}")
    if len(entries) != len(EXPECTED_ENTRIES):
        errors.append(f"build.yaml should contain {len(EXPECTED_ENTRIES)} include entries, found {len(entries)}")
    if LEGACY_BOARD in active_build_text or LEGACY_BOARD in readme_text:
        errors.append(f"legacy {LEGACY_BOARD} target found")

    for entry in entries:
        artifact_name = entry.get("artifact-name", "<unnamed>")
        if entry.get("snippet", ""):
            errors.append(f"normal build {artifact_name} must not set snippet")
        if entry.get("cmake-args", ""):
            errors.append(f"normal build {artifact_name} must not set cmake-args")

    for stale in ("corne_v4_left_studio", "corne_v4_right_studio", "studio-rpc-usb-uart"):
        if stale in active_build_text + readme_text:
            errors.append(f"Studio artifact/snippet found: {stale}")
    for symbol in ("CONFIG_ZMK_STUDIO", "CONFIG_ZMK_USB_BOOT"):
        if f"{symbol}=y" in active_build_text or "y" in config.get(symbol, []):
            errors.append(f"normal config/build must not enable {symbol}=y")

    for stale in ("corne_v3_1_left", "corne_v3_1_right", "corne_v3_1_left_studio"):
        if stale in active_build_text + readme_text:
            errors.append(f"stale artifact name found: {stale}")
    for snippet in REQUIRED_README_SNIPPETS:
        if snippet not in readme_text:
            errors.append(f"README missing snippet: {snippet}")

    if errors:
        raise SystemExit("Build metadata check failed:\n- " + "\n- ".join(errors))
    print("Build metadata check passed: Corne v4 left/right nice_oled artifacts and settings_reset are documented and contain no active snippets or cmake args.")


if __name__ == "__main__":
    main()
