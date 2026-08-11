#!/usr/bin/env python3
"""Validate dependency-reproducibility documentation and intentional floating refs."""
from __future__ import annotations

from pathlib import Path

WEST = Path("config/west.yml")
WORKFLOW = Path(".github/workflows/build.yml")
README = Path("README.md")


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    west_text = WEST.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    readme_text = README.read_text(encoding="utf-8")

    required_west = [
        "revision: main",
        "Pin this only after recording a known-good ZMK commit or tag",
    ]
    missing_west = [snippet for snippet in required_west if snippet not in west_text]
    if missing_west:
        fail("config/west.yml missing reproducibility rationale: " + ", ".join(missing_west))

    required_workflow = [
        "uses: zmkfirmware/zmk/.github/workflows/build-user-config.yml@main",
    ]
    missing_workflow = [snippet for snippet in required_workflow if snippet not in workflow_text]
    if missing_workflow:
        fail("workflow missing expected ZMK reusable workflow reference: " + ", ".join(missing_workflow))

    required_readme = [
        "Dependency reproducibility status",
        "No known-good ZMK commit or release tag has been verified in this repository yet",
        "do not replace `main` with an arbitrary commit",
    ]
    missing_readme = [snippet for snippet in required_readme if snippet not in readme_text]
    if missing_readme:
        fail("README.md missing dependency reproducibility guidance: " + ", ".join(missing_readme))

    print(
        "Dependency check passed: ZMK refs remain intentionally floating and README documents "
        "that no known-good pin has been verified yet."
    )


if __name__ == "__main__":
    main()
