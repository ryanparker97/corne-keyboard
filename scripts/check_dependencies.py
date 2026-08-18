#!/usr/bin/env python3
"""Validate the known-good ZMK revision pin and its documentation."""
from __future__ import annotations

from pathlib import Path

WEST = Path("config/west.yml")
WORKFLOW = Path(".github/workflows/build.yml")
README = Path("README.md")

VERIFIED_ZMK_REVISION = "6e2ef41e022d555b10f116e395832913f71717b3"
PINNED_NICE_OLED_REVISION = "46f824abb2bd41f1287c5c68abd14122af6042a3"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    west_text = WEST.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    readme_text = README.read_text(encoding="utf-8")

    required_west = [
        f"revision: {VERIFIED_ZMK_REVISION}",
        "Pin the exact ZMK revision verified by successful corne_left and",
        "- name: mctechnology17",
        "url-base: https://github.com/mctechnology17",
        "- name: zmk-nice-oled",
        "remote: mctechnology17",
        f"revision: {PINNED_NICE_OLED_REVISION}",
    ]
    missing_west = [snippet for snippet in required_west if snippet not in west_text]
    if missing_west:
        fail("config/west.yml missing reproducibility rationale: " + ", ".join(missing_west))

    required_workflow = [
        "uses: zmkfirmware/zmk/.github/workflows/build-user-config.yml@"
        + VERIFIED_ZMK_REVISION,
    ]
    missing_workflow = [snippet for snippet in required_workflow if snippet not in workflow_text]
    if missing_workflow:
        fail("workflow missing expected ZMK reusable workflow reference: " + ", ".join(missing_workflow))

    required_readme = [
        "Dependency reproducibility status",
        VERIFIED_ZMK_REVISION,
        "Both `corne_left` and `corne_right` compiled successfully",
        "mctechnology17/zmk-nice-oled",
        PINNED_NICE_OLED_REVISION,
        "`nice_oled` shield",
    ]
    missing_readme = [snippet for snippet in required_readme if snippet not in readme_text]
    if missing_readme:
        fail("README.md missing dependency reproducibility guidance: " + ", ".join(missing_readme))

    print(
        "Dependency check passed: west and reusable workflow refs match the documented "
        f"known-good ZMK revision {VERIFIED_ZMK_REVISION}; zmk-nice-oled is pinned "
        f"to {PINNED_NICE_OLED_REVISION}."
    )


if __name__ == "__main__":
    main()
