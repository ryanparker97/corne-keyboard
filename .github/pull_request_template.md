## Summary

Describe the change, its intent, and the physical key positions affected.

## Checklist

- [ ] Layout intent and every changed physical position are documented unambiguously.
- [ ] Each Corne layer still contains exactly 42 bindings.
- [ ] Keymap bindings/comments, checker expectations, `README.md`, and `KEYMAP.md` are synchronized where applicable.
- [ ] `python3 scripts/validate.py` passes locally.
- [ ] `git diff --check` passes locally.
- [ ] CI job `Validate keymap and build metadata` passes.
- [ ] CI job `Build Corne firmware` passes.
- [ ] CI provides both `corne_v3_1_left` and `corne_v3_1_right` artifacts for firmware-affecting changes.
- [ ] Hardware compatibility, bootloader/reset placement, and flashing risk were reviewed; no physical verification is claimed unless performed.
- [ ] Changes to floating or pinned dependency refs (`config/west.yml` or reusable workflow refs) are identified and justified with known-good build evidence.
