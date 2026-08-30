#!/usr/bin/env python3
"""Validate ZMK Kconfig choices that must remain compatible with current ZMK."""
from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

SHARED_CONFIG = Path("config/corne.conf")
LEFT_CONFIG = Path("config/corne_left.conf")
RIGHT_CONFIG = Path("config/corne_right.conf")
CONFIGS = (SHARED_CONFIG, LEFT_CONFIG, RIGHT_CONFIG)
BUILD = Path("build.yaml")
WORKFLOW = Path(".github/workflows/build.yml")

REQUIRED_SHARED_SETTINGS = {
    "CONFIG_EC11": "n",
    "CONFIG_EC11_TRIGGER_GLOBAL_THREAD": "n",
    "CONFIG_ZMK_RGB_UNDERGLOW": "n",
    "CONFIG_ZMK_DISPLAY": "y",
    "CONFIG_ZMK_DISPLAY_WORK_QUEUE_DEDICATED": "y",
    "CONFIG_ZMK_IDLE_TIMEOUT": "60000",
    "CONFIG_ZMK_SLEEP": "y",
    "CONFIG_ZMK_IDLE_SLEEP_TIMEOUT": "300000",
    "CONFIG_ZMK_EXT_POWER": "y",
    "CONFIG_ZMK_BLE_EXPERIMENTAL_FEATURES": "y",
    "CONFIG_BT_PERIPHERAL_PREF_MIN_INT": "12",
    "CONFIG_BT_PERIPHERAL_PREF_MAX_INT": "12",
    "CONFIG_BT_PERIPHERAL_PREF_LATENCY": "30",
    "CONFIG_BT_PERIPHERAL_PREF_TIMEOUT": "600",
    "CONFIG_BT_CTLR_TX_PWR_PLUS_8": "y",
}

REQUIRED_TARGET_SETTINGS = {
    LEFT_CONFIG: {
        "CONFIG_ZMK_USB": "y",
        "CONFIG_ZMK_BLE": "y",
        "CONFIG_ZMK_USB_BOOT": "y",
        "CONFIG_ZMK_HID_REPORT_TYPE_HKRO": "y",
        "CONFIG_ZMK_HID_CONSUMER_REPORT_USAGES_BASIC": "y",
    },
    RIGHT_CONFIG: {
        "CONFIG_ZMK_USB": "n",
        "CONFIG_ZMK_BLE": "y",
    },
}

FORBIDDEN_CONFIG_SNIPPETS = {
    "CONFIG_WS2812_STRIP": "WS2812_STRIP is not a current ZMK user-config symbol; disable underglow with CONFIG_ZMK_RGB_UNDERGLOW=n.",
    "CONFIG_ZMK_KSCAN_DEBOUNCE_": "Do not force deprecated KSCAN debounce Kconfig; leave current shield defaults/devicetree in control.",
    "CONFIG_ZMK_KSCAN=": "Do not force deprecated ZMK KSCAN integration from user config.",
    "CONFIG_KSCAN=": "Do not force Zephyr's deprecated KSCAN symbol from user config.",
    "CONFIG_ZMK_STUDIO=y": "Studio is not required for dual-mode keyboard operation.",
    "CONFIG_KCONFIG_WARNINGS_AS_ERRORS=n": "Do not suppress Kconfig warnings.",
    "KCONFIG_WARNINGS_AS_ERRORS=OFF": "Do not suppress Kconfig warnings.",
    "CONFIG_BT_CTLR_PHY_2M=y": "Do not force BLE 2M PHY; the aggregate experimental setting disables it for Windows compatibility and range.",
    "CONFIG_ZMK_BLE_EXPERIMENTAL_CONN=": "Use CONFIG_ZMK_BLE_EXPERIMENTAL_FEATURES=y rather than a contradictory separate connection assignment.",
    "CONFIG_ZMK_BLE_EXPERIMENTAL_SEC=": "Use CONFIG_ZMK_BLE_EXPERIMENTAL_FEATURES=y rather than a contradictory separate security assignment.",
    "CONFIG_BT_BUF_ACL_RX_SIZE": "Do not force a low-level ACL receive size in user config.",
    "CONFIG_BT_CTLR_DATA_LENGTH_MAX": "Do not force controller data length in user config.",
    "CONFIG_BT_GATT_ENFORCE_SUBSCRIPTION": "Do not override GATT subscription enforcement in user config.",
    "CONFIG_ZMK_BLE_KEYBOARD_REPORT_QUEUE_SIZE": "Use the pinned ZMK report queue default unless measurements justify an override.",
    "CONFIG_ZMK_KSCAN_EVENT_QUEUE_SIZE": "Use the pinned ZMK scan queue default unless measurements justify an override.",
    "CONFIG_ZMK_SPLIT_BLE_CENTRAL_POSITION_QUEUE_SIZE": "Use the pinned ZMK split queue default unless measurements justify an override.",
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


def find_required_config_issues(
    assignments: list[KconfigAssignment], required: dict[str, str]
) -> list[str]:
    issues: list[str] = []
    for symbol, expected_value in required.items():
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
    required_paths = (*CONFIGS, BUILD, WORKFLOW)
    missing_paths = [path for path in required_paths if not path.is_file()]
    if missing_paths:
        fail("Missing required configuration file(s): " + ", ".join(map(str, missing_paths)))

    text_by_path = {
        path: path.read_text(encoding="utf-8") for path in required_paths
    }
    assignments_by_config = {
        path: parse_kconfig_assignments(path, text_by_path[path]) for path in CONFIGS
    }
    all_assignments = [
        assignment
        for path, text in text_by_path.items()
        for assignment in parse_kconfig_assignments(path, text)
    ]
    active_text_by_path = {
        path: "\n".join(line for _, line in active_lines(text))
        for path, text in text_by_path.items()
    }

    required_issues = [
        f"{SHARED_CONFIG}: {issue}"
        for issue in find_required_config_issues(
            assignments_by_config[SHARED_CONFIG], REQUIRED_SHARED_SETTINGS
        )
    ]
    for path, required in REQUIRED_TARGET_SETTINGS.items():
        required_issues.extend(
            f"{path}: {issue}"
            for issue in find_required_config_issues(assignments_by_config[path], required)
        )
    if required_issues:
        fail("Missing required active supported settings:\n- " + "\n- ".join(required_issues))

    shared_usb = [
        assignment
        for assignment in assignments_by_config[SHARED_CONFIG]
        if assignment.symbol in {"CONFIG_ZMK_USB", "CONFIG_ZMK_USB_BOOT"}
    ]
    if shared_usb:
        fail(
            "USB settings must be target-specific, not shared with corne_right:\n- "
            + "\n- ".join(format_location(assignment) for assignment in shared_usb)
        )

    violations = []
    for snippet, reason in FORBIDDEN_CONFIG_SNIPPETS.items():
        for match in forbidden_snippet_matches(snippet, all_assignments, active_text_by_path):
            violations.append(f"{match}: {reason}")
    if violations:
        fail("Current-ZMK config check failed:\n- " + "\n- ".join(violations))

    print(
        "Config check passed: shared settings are safe; left is explicit USB+BLE HKRO/boot, "
        "right is explicit BLE-only; no speculative queue/PHY/ACL, global USB/Studio, "
        "deprecated KSCAN, or warning-suppression settings."
    )


if __name__ == "__main__":
    main()
