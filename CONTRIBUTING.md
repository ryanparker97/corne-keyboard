# Contributing

This repository uses a lightweight GitHub Flow based on the current `master` branch. It does **not** use classic GitFlow with a long-lived `develop` branch or release branches.

## Workflow

1. Synchronize local `master` without rewriting it:

   ```sh
   git switch master
   git pull --ff-only origin master
   ```

2. Create a short-lived branch with an intent-specific prefix:

   ```sh
   git switch -c feature/short-description
   # or: fix/short-description
   # or: docs/short-description
   ```

3. Keep each change focused. When layout behavior changes, update the keymap bindings and comments, checker expectations, `README.md`, and `KEYMAP.md` together so physical positions and documented behavior stay synchronized.

4. Run local validation before opening a pull request:

   ```sh
   python3 scripts/validate.py
   git diff --check
   ```

5. Push the branch and open a pull request against `master`. Describe layout intent and physical positions, firmware/hardware risk, and any dependency-ref changes.

6. Let both existing CI jobs pass:
   - `Validate keymap and build metadata`
   - `Build Corne firmware`

   For firmware-affecting changes, confirm the build produces artifacts for both `corne_v4_left` and `corne_v4_right`.

7. Merge the reviewed pull request, then delete the short-lived branch locally and remotely. Do not maintain parallel `develop` or release integration branches.

Repository checks are static and CI builds firmware, but neither proves physical hardware safety or successful flashing. Follow the README hardware and flashing caveats before using artifacts.
