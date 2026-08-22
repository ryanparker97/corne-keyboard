#!/usr/bin/env python3
"""Validate dependency pins and current Corne documentation anchors."""
from __future__ import annotations

from pathlib import Path

ZMK_REVISION = "6e2ef41e022d555b10f116e395832913f71717b3"
NICE_OLED_REMOTE = "chyuuu"
NICE_OLED_REPOSITORY = "chyuuu/zmk-nice-oled"
NICE_OLED_REVISION = "b2d5cd914b2180cb53766b0302c75818400d2f58"


def joined(*parts: str) -> str:
    return "".join(parts)


def main() -> None:
    west = Path("config/west.yml").read_text(encoding="utf-8")
    workflow = Path(".github/workflows/build.yml").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    keymap_doc = Path("KEYMAP.md").read_text(encoding="utf-8")
    corne_conf = Path("config/corne.conf").read_text(encoding="utf-8")
    keymap = Path("config/corne.keymap").read_text(encoding="utf-8")
    build = Path("build.yaml").read_text(encoding="utf-8")
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
        "pins are chosen for reproducibility",
        "Local static validation passes with `python3 scripts/validate.py`",
        "full firmware compilation was not run in this environment",
        "GitHub Actions or a local ZMK/west workspace",
        "`west` is unavailable here",
    ):
        if snippet not in readme:
            errors.append(f"README missing dependency note: {snippet}")

    stale_readme_claims = (
        "CONFIG_ZMK_USB=n",
        "CONFIG_BT_CTLR_PHY_2M=n",
        "CONFIG_BT_DEVICE_NAME",
        "CONFIG_CORNE_SIMPLE_OLED_STATUS_SCREEN",
        "CONFIG_NICE_OLED_WIDGET_STATUS",
        "CONFIG_NICE_OLED_WIDGET_WPM",
        "CONFIG_NICE_OLED_WIDGET_ANIMATION_PERIPHERAL",
        "CONFIG_NICE_OLED_WIDGET_STATIC_IMAGE_PERIPHERAL",
        "CONFIG_NICE_OLED_WIDGET_HID_INDICATORS",
        "CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS",
        "disables ZMK USB",
        "only typing output",
        "Bluetooth LE only",
        "static configured device name",
        "simple layer/BLE/name OLED",
    )
    for claim in stale_readme_claims:
        if claim in readme:
            errors.append(f"README contains stale inactive config claim: {claim}")

    readme_required = (
        "generic Corne shields rather than a separate `corne_v4` shield",
        "`nice_nano/nrf52840/zmk`",
        "`corne_left`",
        "`corne_right`",
        "`corne_v4_left`",
        "`corne_v4_right`",
        "Left thumbs, outer -> inner:  LALT  RAISE  LWIN",
        "Right thumbs, inner -> outer: SPACE  LOWER  ENTER",
        "Raw default thumb bindings are `&kp LALT  &mo RSE  &kp LWIN    &kp SPACE  &mo LWR  &kp RET`",
        "RGB underglow/per-key LED support is disabled",
        "no active `CONFIG_ZMK_RGB_UNDERGLOW*` settings",
        "does not add an `&led_strip` chain-length override",
        "Win+Shift+S",
        "Ctrl+Y",
        "Previous",
    )
    for snippet in readme_required:
        if snippet not in readme:
            errors.append(f"README missing updated hardware/config note: {snippet}")

    keymap_required = (
        "generic `corne_left`/`corne_right` shields",
        "native-wireless 42-key Corne v4",
        "Left thumbs, outer -> inner:  LALT  RAISE  LWIN",
        "Right thumbs, inner -> outer: SPACE  LOWER  ENTER",
        "Raw bindings: &kp LALT  &mo RSE  &kp LWIN    &kp SPACE  &mo LWR  &kp RET",
        "On `LWR`, the left outer thumb is `LCTRL` and the remaining thumbs are transparent",
        "On `RSE` and `ADJ`, all thumbs are transparent",
        "Windows utility chords",
        "Media controls",
        "no `&rgb_ug` bindings and no `&led_strip` chain-length override",
        "display-name` values `DEF`, `LWR`, `RSE`, and `ADJ`",
    )
    for snippet in keymap_required:
        if snippet not in keymap_doc:
            errors.append(f"KEYMAP missing updated hardware/keymap note: {snippet}")

    forbidden_visible = (
        "corne_v3_1",
        "corne_v4_left_studio",
        "corne_v4_right_studio",
        "studio-rpc-usb-uart",
        "RGB controls",
        "&out OUT_USB",
        "&out OUT_TOG",
        joined("m", "acOS"),
        joined("M", "ac"),
        joined("Kara", "biner"),
        joined("s", "khd"),
        joined("ya", "bai"),
        joined("Com", "mand"),
        joined("L", "GUI"),
        joined("R", "GUI"),
        joined("m", "acos"),
    )
    tracked_text = "\n".join((readme, keymap_doc, corne_conf, west, workflow, build, keymap))
    for stale in forbidden_visible:
        if stale in tracked_text:
            errors.append(f"stale or prohibited wording remains: {stale}")

    if "CONFIG_ZMK_STUDIO=y" in tracked_text:
        errors.append("normal tracked config/docs must not enable Studio")
    if "#include <dt-bindings/zmk/outputs.h>" in keymap or "&out" in keymap:
        errors.append("keymap must not include output-switching behavior")

    if errors:
        raise SystemExit("Dependency check failed:\n- " + "\n- ".join(errors))
    print("Dependency check passed: pins, generic Corne v4 docs, and current Windows keymap documentation are aligned.")


if __name__ == "__main__":
    main()
