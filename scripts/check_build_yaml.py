#!/usr/bin/env python3
"""Validate the ZMK build matrix and documented board target.

This intentionally avoids third-party YAML packages so it can run in the
lightweight GitHub Actions validation job before the ZMK build workflow.
"""
from __future__ import annotations

from pathlib import Path

EXPECTED_BOARD = "nice_nano/nrf52840/zmk"
STALE_BOARDS = {"nice_nano_v2"}
EXPECTED_MATRIX = {
    (EXPECTED_BOARD, "corne_left", "corne_v4_left"),
    (EXPECTED_BOARD, "corne_right", "corne_v4_right"),
}
README_REQUIRED_SNIPPETS = [
    f"`{EXPECTED_BOARD}`",
    f"west build -s zmk/app -d build/corne_left -b {EXPECTED_BOARD} -- "
    '-DSHIELD=corne_left -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"',
    f"west build -s zmk/app -d build/corne_right -b {EXPECTED_BOARD} -- "
    '-DSHIELD=corne_right -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"',
]


def fail(message: str) -> None:
    raise SystemExit(message)


def reject_stale_targets(path: Path, text: str) -> None:
    found = sorted(stale for stale in STALE_BOARDS if stale in text)
    if found:
        fail(f"{path} contains stale board target(s): {', '.join(found)}")


def parse_include_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            if current is not None:
                entries.append(current)
            current = {}
            stripped = stripped[2:].strip()
        if current is None or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        current[key.strip()] = value.strip().strip('"\'')

    if current is not None:
        entries.append(current)
    return entries


def main() -> None:
    build_path = Path("build.yaml")
    readme_path = Path("README.md")
    build_text = build_path.read_text(encoding="utf-8")
    readme_text = readme_path.read_text(encoding="utf-8")

    for path, text in ((build_path, build_text), (readme_path, readme_text)):
        reject_stale_targets(path, text)

    if "include:" not in build_text:
        fail("build.yaml missing include matrix")

    actual_matrix = {
        (entry.get("board", ""), entry.get("shield", ""), entry.get("artifact-name", ""))
        for entry in parse_include_entries(build_text)
        if "board" in entry or "shield" in entry or "artifact-name" in entry
    }
    if actual_matrix != EXPECTED_MATRIX:
        expected = "; ".join(" / ".join(item) for item in sorted(EXPECTED_MATRIX))
        actual = "; ".join(" / ".join(item) for item in sorted(actual_matrix)) or "<none>"
        fail(f"build.yaml matrix mismatch. Expected: {expected}. Actual: {actual}")

    missing_readme = [snippet for snippet in README_REQUIRED_SNIPPETS if snippet not in readme_text]
    if missing_readme:
        fail("README.md missing expected board documentation: " + ", ".join(missing_readme))

    print(
        "Build metadata check passed: "
        f"{EXPECTED_BOARD} corne_left and corne_right targets present; stale targets absent."
    )


if __name__ == "__main__":
    main()
