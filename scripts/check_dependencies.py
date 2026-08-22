#!/usr/bin/env python3
"""Validate dependency pins, OLED docs, and workflow shape."""
from __future__ import annotations

from pathlib import Path

ZMK_REVISION = "6e2ef41e022d555b10f116e395832913f71717b3"
NICE_OLED_REMOTE = "chyuuu"
NICE_OLED_REPOSITORY = "chyuuu/zmk-nice-oled"
NICE_OLED_REVISION = "b2d5cd914b2180cb53766b0302c75818400d2f58"


def main() -> None:
    west = Path("config/west.yml").read_text(encoding="utf-8")
    workflow = Path(".github/workflows/build.yml").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    corne_conf = Path("config/corne.conf").read_text(encoding="utf-8")
    corne_left_conf = Path("config/corne_left.conf").read_text(encoding="utf-8")
    errors: list[str] = []

    for snippet in (
        f"revision: {ZMK_REVISION}",
        f"- name: {NICE_OLED_REMOTE}",
        "url-base: https://github.com/chyuuu",
        "- name: zmk-nice-oled",
        f"remote: {NICE_OLED_REMOTE}",
        f"revision: {NICE_OLED_REVISION}",
    ):
        if snippet not in west:
            errors.append(f"config/west.yml missing {snippet}")

    if f"uses: zmkfirmware/zmk/.github/workflows/build-user-config.yml@{ZMK_REVISION}" not in workflow:
        errors.append("workflow is not pinned to the west ZMK revision")
    for forbidden_job in ("\n  validate:", "\n  validation:"):
        if forbidden_job in workflow:
            errors.append("separate GitHub validation job must not be restored")

    for snippet in (
        "Dependency reproducibility status",
        ZMK_REVISION,
        NICE_OLED_REPOSITORY,
        NICE_OLED_REVISION,
        "LVGL9-compatible",
        "nice_oled",
        "Mac modifier icons",
        "Control, Shift, Option, and Command",
        "CapsLock HID indicator",
        "bongo cat animation",
        "`config/corne_left.conf`",
        "right peripheral build avoids central-only Kconfig warnings",
        "No separate GitHub validation job is configured",
        "Local static validation passes with `python3 scripts/validate.py`",
        "full firmware compilation was not run in this environment",
        "GitHub Actions or a local ZMK/west workspace",
        "`west` is unavailable here",
    ):
        if snippet not in readme:
            errors.append(f"README missing {snippet}")

    for stale in (
        "mctechnology17/zmk-nice-oled",
        "46f824abb2bd41f1287c5c68abd14122af6042a3",
        "compiled successfully at the pinned ZMK revision",
        "verified by successful corne_left",
    ):
        if stale in readme or stale in west or stale in corne_conf or stale in corne_left_conf:
            errors.append(f"stale dependency/build wording remains: {stale}")

    if "LVGL9-compatible chyuuu/zmk-nice-oled fork" not in corne_conf:
        errors.append("config/corne.conf missing dependency note")
    if "CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_SYMBOL_MACOS=y" not in corne_left_conf:
        errors.append("config/corne_left.conf missing Mac modifier symbol setting")
    if "CONFIG_NICE_OLED_WIDGET_HID_INDICATORS_BONGO_CAT_ONLY_CAPSLOCK=y" not in corne_left_conf:
        errors.append("config/corne_left.conf missing CapsLock-only bongo indicator setting")

    if errors:
        raise SystemExit("Dependency check failed:\n- " + "\n- ".join(errors))
    print("Dependency check passed: west pins, workflow, nice_oled docs, and corne.conf dependency note are aligned.")


if __name__ == "__main__":
    main()
