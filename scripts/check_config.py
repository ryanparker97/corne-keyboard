#!/usr/bin/env python3
"""Validate ZMK Kconfig choices that must remain compatible with current ZMK."""
from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

CONFIG = Path("config/corne.conf")
BUILD = Path("build.yaml")
WORKFLOW = Path(".github/workflows/build.yml")

REQUIRED_CONFIG_SETTINGS = {
    "CONFIG_ZMK_RGB_UNDERGLOW": "y",
    "CONFIG_WS2812_STRIP": "y",
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
    "CONFIG_ZMK_BLE_EXPERIMENTAL_CONN": "y",
    "CONFIG_BT_PERIPHERAL_PREF_MIN_INT": "12",
    "CONFIG_BT_PERIPHERAL_PREF_MAX_INT": "12",
    "CONFIG_BT_PERIPHERAL_PREF_LATENCY": "30",
    "CONFIG_BT_PERIPHERAL_PREF_TIMEOUT": "600",
    "CONFIG_ZMK_BLE_KEYBOARD_REPORT_QUEUE_SIZE": "40",
    "CONFIG_ZMK_KSCAN_EVENT_QUEUE_SIZE": "16",
    "CONFIG_ZMK_SPLIT_BLE_CENTRAL_POSITION_QUEUE_SIZE": "16",
    "CONFIG_BT_CTLR_TX_PWR_PLUS_8": "y",
    "CONFIG_BT_BUF_ACL_RX_SIZE": "512",
    "CONFIG_BT_CTLR_DATA_LENGTH_MAX": "251",
    "CONFIG_BT_GATT_ENFORCE_SUBSCRIPTION": "n",
}

REQUIRED_CONFIG_SNIPPETS = [
    f"{symbol}={value}" for symbol, value in REQUIRED_CONFIG_SETTINGS.items()
]

FORBIDDEN_CONFIG_SNIPPETS = {
    "CONFIG_ZMK_KSCAN_DEBOUNCE_": "Do not force deprecated KSCAN debounce Kconfig; leave current shield defaults/devicetree in control.",
    "CONFIG_ZMK_KSCAN=": "Do not force deprecated ZMK KSCAN integration from user config.",
    "CONFIG_KSCAN=": "Do not force Zephyr's deprecated KSCAN symbol from user config.",
    "CONFIG_ZMK_USB=y": "USB must not be enabled globally because corne_right is a split peripheral.",
    "CONFIG_KCONFIG_WARNINGS_AS_ERRORS=n": "Do not suppress Kconfig warnings.",
    "KCONFIG_WARNINGS_AS_ERRORS=OFF": "Do not suppress Kconfig warnings.",
    "CONFIG_BT_CTLR_PHY_2M=y": "Do not force BLE 2M PHY; keep PHY host/controller negotiated for Mac compatibility and range.",
}

KCONFIG_ASSIGNMENT_RE = re.compile(r"^(CONFIG_[A-Za-z0-9_]+)\s*=\s*(.*?)\s*$")


class KconfigAssignment(NamedTuple):
    path: Path
    line_number: int
    symbol: str
    value: str

    @property
    def snippet(self) -> str:
        return f"{self.symbol}={self.value}"


def fail(message: str) -> None:
    raise SystemExit(message)


def strip_inline_comment(line: str) -> str:
    """Remove unquoted comments while preserving quoted Kconfig string values."""
    quote: str | None = None
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
            continue
        if char == "#":
            return line[:index]
    return line


def active_lines(text: str) -> list[tuple[int, str]]:
    """Return non-empty, non-comment logical lines with inline comments removed."""
    lines: list[tuple[int, str]] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = strip_inline_comment(raw_line).strip()
        if line:
            lines.append((line_number, line))
    return lines


def parse_kconfig_assignments(path: Path, text: str) -> list[KconfigAssignment]:
    """Parse active Kconfig assignments, ignoring commented-out examples."""
    assignments: list[KconfigAssignment] = []
    for line_number, line in active_lines(text):
        match = KCONFIG_ASSIGNMENT_RE.match(line)
        if match:
            symbol, value = match.groups()
            assignments.append(KconfigAssignment(path, line_number, symbol, value.strip()))
    return assignments


def format_location(assignment: KconfigAssignment) -> str:
    return f"{assignment.path}:{assignment.line_number}: {assignment.snippet}"


def find_required_config_issues(assignments: list[KconfigAssignment]) -> list[str]:
    issues: list[str] = []
    for symbol, expected_value in REQUIRED_CONFIG_SETTINGS.items():
        active_values = [assignment.value for assignment in assignments if assignment.symbol == symbol]
        if not active_values:
            issues.append(f"{symbol}={expected_value} is not active")
            continue
        unexpected_values = sorted({value for value in active_values if value != expected_value})
        if unexpected_values:
            issues.append(
                f"{symbol} must be exactly {expected_value}; active value(s): "
                + ", ".join(active_values)
            )
    return issues


def forbidden_snippet_matches(
    snippet: str,
    assignments: list[KconfigAssignment],
    active_text_by_path: dict[Path, str],
) -> list[str]:
    if snippet.startswith("CONFIG_") and "=" in snippet:
        symbol, expected_value = snippet.split("=", 1)
        matches = [
            format_location(assignment)
            for assignment in assignments
            if assignment.symbol == symbol and assignment.value == expected_value
        ]
        if matches:
            return matches
    elif snippet.startswith("CONFIG_"):
        matches = [
            format_location(assignment)
            for assignment in assignments
            if assignment.symbol.startswith(snippet)
        ]
        if matches:
            return matches

    return [
        f"{path}: active non-comment text contains {snippet!r}"
        for path, active_text in active_text_by_path.items()
        if snippet in active_text
    ]


def main() -> None:
    text_by_path = {
        path: path.read_text(encoding="utf-8") for path in (CONFIG, BUILD, WORKFLOW)
    }
    config_assignments = parse_kconfig_assignments(CONFIG, text_by_path[CONFIG])
    all_assignments = [
        assignment
        for path, text in text_by_path.items()
        for assignment in parse_kconfig_assignments(path, text)
    ]
    active_text_by_path = {
        path: "\n".join(line for _, line in active_lines(text))
        for path, text in text_by_path.items()
    }

    required_issues = find_required_config_issues(config_assignments)
    if required_issues:
        fail(
            "config/corne.conf missing required active supported settings:\n- "
            + "\n- ".join(required_issues)
        )

    violations = []
    for snippet, reason in FORBIDDEN_CONFIG_SNIPPETS.items():
        for match in forbidden_snippet_matches(snippet, all_assignments, active_text_by_path):
            violations.append(f"{match}: {reason}")
    if violations:
        fail("Current-ZMK config check failed:\n- " + "\n- ".join(violations))

    print(
        "Config check passed: required active Corne/BLE/nice_oled settings are exact; no active "
        "obsolete WS2812_STRIP, user-forced deprecated KSCAN, forced BLE 2M PHY, "
        "global USB/Studio, or warning-suppression settings."
    )


if __name__ == "__main__":
    main()
