#!/usr/bin/env python3
"""Validate dependency pins and current Windows configuration boundaries."""
from __future__ import annotations

from pathlib import Path

ZMK_REVISION = "6e2ef41e022d555b10f116e395832913f71717b3"
NICE_OLED_REMOTE = "chyuuu"
NICE_OLED_REPOSITORY = "chyuuu/zmk-nice-oled"
NICE_OLED_REVISION = "b2d5cd914b2180cb53766b0302c75818400d2f58"


def require_snippets(text: str, snippets: tuple[str, ...], source: str) -> list[str]:
    """Return missing required snippets for one source file."""
    return [f"{source} missing: {snippet}" for snippet in snippets if snippet not in text]


def main() -> None:
    west = Path("config/west.yml").read_text(encoding="utf-8")
    workflow = Path(".github/workflows/build.yml").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    keymap = Path("config/corne.keymap").read_text(encoding="utf-8")
    corne_conf = Path("config/corne.conf").read_text(encoding="utf-8")
    errors: list[str] = []

    errors.extend(
        require_snippets(
            west,
            (
                f"revision: {ZMK_REVISION}",
                f"- name: {NICE_OLED_REMOTE}",
                "url-base: https://github.com/chyuuu",
                "- name: zmk-nice-oled",
                f"remote: {NICE_OLED_REMOTE}",
                f"revision: {NICE_OLED_REVISION}",
            ),
            "config/west.yml",
        )
    )
    workflow_pin = (
        "uses: zmkfirmware/zmk/.github/workflows/build-user-config.yml@"
        f"{ZMK_REVISION}"
    )
    errors.extend(require_snippets(workflow, (workflow_pin,), ".github/workflows/build.yml"))
    errors.extend(
        require_snippets(
            readme,
            (
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
            ),
            "README.md",
        )
    )

    tracked_text = "\n".join((readme, corne_conf, west, workflow, keymap))
    forbidden = (
        "corne_v3_1",
        "corne_v4_left_studio",
        "corne_v4_right_studio",
        "studio-rpc-usb-uart",
        "&out OUT_USB",
        "&out OUT_TOG",
        "macOS",
        "Karabiner",
        "skhd",
        "yabai",
    )
    errors.extend(f"stale or prohibited wording remains: {term}" for term in forbidden if term in tracked_text)
    if "CONFIG_ZMK_STUDIO=y" in tracked_text:
        errors.append("normal tracked config/docs must not enable Studio")
    if "#include <dt-bindings/zmk/outputs.h>" in keymap or "&out" in keymap:
        errors.append("keymap must not include output-switching behavior")

    if errors:
        raise SystemExit("Dependency check failed:\n- " + "\n- ".join(errors))
    print("Dependency check passed: pinned ZMK/nice_oled dependencies and Windows configuration boundaries are aligned.")


if __name__ == "__main__":
    main()
