#!/usr/bin/env python3
"""Validate dependency pins used by west and GitHub Actions."""
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
    keymap_doc = Path("KEYMAP.md").read_text(encoding="utf-8")
    corne_conf = Path("config/corne.conf").read_text(encoding="utf-8")
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
    for snippet in (
        "Dependency reproducibility status",
        ZMK_REVISION,
        NICE_OLED_REPOSITORY,
        NICE_OLED_REVISION,
        "LVGL9-compatible",
        "image descriptors for the pinned ZMK/LVGL 9 stack",
        "nice_oled",
        "pins are chosen for reproducibility",
        "Local static validation passes with `python3 scripts/validate.py`",
        "full firmware compilation was not run in this environment",
        "GitHub Actions or a local ZMK/west workspace",
        "`west` is unavailable here",
    ):
        if snippet not in readme:
            errors.append(f"README missing {snippet}")
    for stale in (
        "verified by successful corne_left",
        "compiled successfully at the pinned ZMK revision",
        "Repository HEAD documented that both",
    ):
        if stale in readme or stale in west:
            errors.append(f"stale compile verification wording remains: {stale}")
    for stale in (
        "mctechnology17/zmk-nice-oled",
        "46f824abb2bd41f1287c5c68abd14122af6042a3",
    ):
        if stale in readme or stale in west or stale in corne_conf:
            errors.append(f"stale zmk-nice-oled dependency remains: {stale}")
    for snippet in (
        "LVGL9-compatible chyuuu/zmk-nice-oled fork",
    ):
        if snippet not in corne_conf:
            errors.append(f"config/corne.conf missing dependency note: {snippet}")
    for snippet in (
        "right thumbs inner-to-outer",
        "inner-right thumb",
        "pinned/upstream ZMK Corne `nice_nano` overlay defines the `led_strip` node",
        "&led_strip { chain-length = <27>; };",
        "CONFIG_ZMK_RGB_UNDERGLOW_BRT_MAX=40",
        "USB_DEVICE_STACK",
        "default output prefers USB",
        "&out OUT_USB",
        "&out OUT_BLE",
        "&out OUT_TOG",
    ):
        if snippet not in readme:
            errors.append(f"README missing updated hardware/config note: {snippet}")
    for snippet in (
        "right thumbs inner-to-outer",
        "inner-right thumb",
        "pinned/upstream ZMK Corne `nice_nano` overlay defines the `led_strip` node",
        "&led_strip { chain-length = <27>; };",
        "&out OUT_USB",
        "&out OUT_BLE",
        "&out OUT_TOG",
        "ZMK prefers USB by default",
    ):
        if snippet not in keymap_doc:
            errors.append(f"KEYMAP missing updated hardware/keymap note: {snippet}")

    if errors:
        raise SystemExit("Dependency check failed:\n- " + "\n- ".join(errors))
    print("Dependency check passed: west, workflow, LVGL9-compatible zmk-nice-oled fork, README, and corne.conf pins are aligned.")


if __name__ == "__main__":
    main()
