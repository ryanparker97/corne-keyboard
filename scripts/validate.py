#!/usr/bin/env python3
"""Run all repository-local validation checks."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CHECKS = [
    "scripts/check_keymap.py",
    "scripts/check_keymap_doc.py",
    "scripts/check_build_yaml.py",
    "scripts/check_config.py",
    "scripts/check_dependencies.py",
]


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    for check in CHECKS:
        print(f"==> {check}", flush=True)
        result = subprocess.run([sys.executable, check], cwd=repo)
        if result.returncode != 0:
            return result.returncode
    print("All local validation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
