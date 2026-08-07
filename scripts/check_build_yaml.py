#!/usr/bin/env python3
"""Validate the minimal ZMK build matrix without third-party YAML packages."""
from __future__ import annotations

from pathlib import Path

text = Path("build.yaml").read_text(encoding="utf-8")
required = [
    "include:",
    "board: nice_nano_v2",
    "shield: corne_left",
    "shield: corne_right",
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit("build.yaml missing required entries: " + ", ".join(missing))

if text.count("board: nice_nano_v2") < 2:
    raise SystemExit("build.yaml should build both Corne halves with nice_nano_v2")

print("Build metadata check passed: nice_nano_v2 corne_left and corne_right targets present.")
