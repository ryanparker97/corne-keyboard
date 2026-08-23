# Corne v4 ZMK Configuration for Windows

This repository is a ZMK configuration for a 42-key Corne v4 split keyboard using nice!nano controllers. It is a Windows-focused NJ68-to-Corne transition layout: QWERTY stays familiar, `ESC` and `BACKSPACE` occupy the top corners, and layers replace the missing number row and navigation cluster.

ZMK is pinned to the known-good revision `6e2ef41e022d555b10f116e395832913f71717b3`. The build matrix uses `nice_nano/nrf52840/zmk` with `corne_left nice_oled`, `corne_right nice_oled`, and `settings_reset` targets.

## Layout overview

- `DEF`: QWERTY, `CAPS LOCK`, and separate thumb `LEFT ALT`, `RAISE`, `LEFT GUI` (the Windows key), `SPACE`, `LOWER`, and `ENTER`.
- `LWR`: numbers, `TAB`, navigation, `DELETE`, `F1`-`F12`, and a left-thumb `CTRL` for `CTRL+number`.
- `RSE`: symbols, paired punctuation, and `CTRL+ARROW` editing/navigation chords.
- `ADJ`: Bluetooth profiles, native Windows shortcuts, bootloader, and reset. Hold `LOWER` and `RAISE` together to activate it.

The firmware emits plain `CAPS LOCK`; it has no host remapper or window-manager dependency. `LEFT GUI` is the Windows key. `ADJ` actions are built into the keyboard and use standard Windows shortcuts.

## ADJ Windows shortcuts

The position names below are physical positions from the base layer, not the key emitted while `ADJ` is active. `LG` means Left GUI (Windows key), `LS` means Left Shift, and `LC` means Left Control.

| Physical position | Exact ZMK binding | Windows behavior |
|---|---|---|
| `Y` | `&kp PSCRN` | Print Screen |
| `U` | `&kp LG(LS(S))` | Win+Shift+S: screen snip |
| `I` | `&kp LG(V)` | Win+V: Clipboard history |
| `O` | `&kp LG(S)` | Win+S: Search |
| `P` | `&kp LG(TAB)` | Win+Tab: Task View |
| Top-right `BACKSPACE` | `&kp LG(L)` | Win+L: lock Windows |
| `A` | `&kp LC(A)` | Ctrl+A: select all |
| `S` | `&kp LC(S)` | Ctrl+S: save |
| `D` | `&kp LG(R)` | Win+R: Run |
| `F` | `&kp LC(F)` | Ctrl+F: find |
| `G` | `&kp LG(LEFT)` | Win+Left: snap window left |
| `H` | `&kp LG(RIGHT)` | Win+Right: snap window right |
| `Z` | `&kp LC(Z)` | Ctrl+Z: undo |
| `X` | `&kp LC(X)` | Ctrl+X: cut |
| `C` | `&kp LC(C)` | Ctrl+C: copy |
| `V` | `&kp LC(V)` | Ctrl+V: paste |
| `B` | `&kp LC(LS(Z))` | Ctrl+Shift+Z: redo |

Bluetooth profile selection is on `Q` through `T`; `CAPS` clears Bluetooth pairing. Bootloader and system reset remain at the bottom-right `/` and `CTRL` positions on `ADJ`. See [KEYMAP.md](KEYMAP.md) for all 42 positions and raw bindings.

## Configuration and safety

`config/corne.conf` provides display support, sleep/external-power support, disabled RGB underglow, and conservative Bluetooth latency preferences. The shared config does not globally enable USB or ZMK Studio because the right half is a split peripheral. The configuration cannot verify physical wiring, battery safety, radio conditions, or successful flashing.

Only flash this configuration to a Corne v4 split with nice!nano v2-compatible controllers. The build uses generic Corne shields rather than a separate `corne_v4` shield: `corne_left nice_oled` and `corne_right nice_oled`. GitHub Actions labels its uploaded half-firmware artifacts `corne_v4_left` and `corne_v4_right`; use the artifact for the half being flashed. Test base keys, thumbs, `LOWER` + `RAISE`, Bluetooth pairing, and guarded boot/reset positions before relying on the keyboard.

## Building

The GitHub Actions workflow first runs repository validation, then builds the two Corne halves and a settings-reset image. A local ZMK/west workspace can build the same matrix with:

```sh
west build -s zmk/app -d build/corne_left -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_left nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
west build -s zmk/app -d build/corne_right -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_right nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
west build -s zmk/app -d build/settings_reset -b nice_nano/nrf52840/zmk -- -DSHIELD="settings_reset" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
```

Each local command writes its firmware to `zephyr/zmk.uf2` inside its build directory: `build/corne_left/zephyr/zmk.uf2`, `build/corne_right/zephyr/zmk.uf2`, or `build/settings_reset/zephyr/zmk.uf2`. The GitHub Actions matrix labels the uploaded half-firmware artifacts `corne_v4_left` and `corne_v4_right`; those are CI artifact labels, not local output filenames. The settings-reset firmware clears stored ZMK settings, including Bluetooth pairing, when flashed; reflash the normal half firmware afterward.

## Dependency reproducibility status

`config/west.yml` and the reusable workflow pin ZMK to `6e2ef41e022d555b10f116e395832913f71717b3`. The `chyuuu/zmk-nice-oled` module is pinned to `b2d5cd914b2180cb53766b0302c75818400d2f58`, an LVGL9-compatible revision. These pins are chosen for reproducibility; update them together only after rebuilding both halves.

Local static validation passes with `python3 scripts/validate.py`; full firmware compilation was not run in this environment. Use GitHub Actions or a local ZMK/west workspace for a firmware build. If `west` is unavailable here, install it in that workspace before running the build commands.

## Validation

Run the static checks without a local ZMK checkout:

```sh
python3 scripts/validate.py
git diff --check
```

The checks validate the four 42-key layers, exact ADJ Windows and Bluetooth/maintenance positions, documentation synchronization, build metadata, current ZMK configuration, and dependency pins. They do not compile firmware or test physical hardware.
