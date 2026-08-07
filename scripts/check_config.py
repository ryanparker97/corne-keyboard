#!/usr/bin/env python3
"""Validate ZMK Kconfig choices that must remain compatible with current ZMK."""
from __future__ import annotations

from pathlib import Path

CONFIG = Path("config/corne.conf")
BUILD = Path("build.yaml")
WORKFLOW = Path(".github/workflows/build.yml")

FORBIDDEN_CONFIG_SNIPPETS = {
    "CONFIG_WS2812_STRIP": "WS2812_STRIP is not a current ZMK user-config symbol; disable underglow with CONFIG_ZMK_RGB_UNDERGLOW=n.",
    "CONFIG_ZMK_KSCAN_DEBOUNCE_": "Do not force deprecated KSCAN debounce Kconfig; leave current shield defaults/devicetree in control.",
    "CONFIG_ZMK_KSCAN=": "Do not force deprecated ZMK KSCAN integration from user config.",
    "CONFIG_KSCAN=": "Do not force Zephyr's deprecated KSCAN symbol from user config.",
    "CONFIG_ZMK_STUDIO=y": "Studio must not be enabled globally because corne_right is a split peripheral.",
    "CONFIG_ZMK_USB=y": "USB must not be enabled globally because corne_right is a split peripheral.",
    "CONFIG_KCONFIG_WARNINGS_AS_ERRORS=n": "Do not suppress Kconfig warnings.",
    "KCONFIG_WARNINGS_AS_ERRORS=OFF": "Do not suppress Kconfig warnings.",
}

REQUIRED_CONFIG_SNIPPETS = [
    "CONFIG_ZMK_RGB_UNDERGLOW=n",
    "CONFIG_ZMK_DISPLAY=y",
    "CONFIG_ZMK_SLEEP=y",
    "CONFIG_ZMK_EXT_POWER=y",
]


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    config_text = CONFIG.read_text(encoding="utf-8")
    all_text = "\n".join(path.read_text(encoding="utf-8") for path in (CONFIG, BUILD, WORKFLOW))

    missing = [snippet for snippet in REQUIRED_CONFIG_SNIPPETS if snippet not in config_text]
    if missing:
        fail("config/corne.conf missing required supported settings: " + ", ".join(missing))

    violations = [f"{snippet}: {reason}" for snippet, reason in FORBIDDEN_CONFIG_SNIPPETS.items() if snippet in all_text]
    if violations:
        fail("Current-ZMK config check failed:\n- " + "\n- ".join(violations))

    print(
        "Config check passed: no undefined WS2812_STRIP, user-forced deprecated KSCAN, "
        "global USB/Studio, or warning-suppression settings; supported Corne options remain."
    )


if __name__ == "__main__":
    main()
