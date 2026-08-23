# Corne v4 ZMK Configuration for Windows

This repository is a ZMK configuration for a 42-key Corne v4 split keyboard using nice!nano controllers. It is a Windows-focused NJ68-to-Corne transition layout: QWERTY stays familiar, `ESC` and `BACKSPACE` occupy the top corners, and layers replace the missing number row and navigation cluster.

ZMK is pinned to the known-good revision `6e2ef41e022d555b10f116e395832913f71717b3`. The build matrix uses `nice_nano/nrf52840/zmk` with the standard `corne_left` and `corne_right` shields.

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
| `Z` / `X` / `C` / `V` / `B` | `&kp LC(Z)` / `&kp LC(X)` / `&kp LC(C)` / `&kp LC(V)` / `&kp LC(LS(Z))` | Undo, cut, copy, paste, redo |

Bluetooth profile selection is on `Q` through `T`; `CAPS` clears Bluetooth pairing. Bootloader and system reset remain at the bottom-right `/` and `CTRL` positions on `ADJ`. See [KEYMAP.md](KEYMAP.md) for all 42 positions and raw bindings.

## Configuration and safety

`config/corne.conf` provides display support, sleep/external-power support, disabled RGB underglow, and conservative Bluetooth latency preferences. The shared config does not globally enable USB or ZMK Studio because the right half is a split peripheral. The configuration cannot verify physical wiring, battery safety, radio conditions, or successful flashing.

Only flash this configuration to a Corne v4 split with nice!nano v2-compatible controllers and standard `corne_left`/`corne_right` shields. The left and right firmware artifacts are distinct; use the artifact for the half being flashed. Test base keys, thumbs, `LOWER` + `RAISE`, Bluetooth pairing, and guarded boot/reset positions before relying on the keyboard.

## Building

The GitHub Actions workflow first runs repository validation, then builds the two Corne halves. A local ZMK/west workspace can build them with:

```sh
west build -s zmk/app -d build/corne_left -b nice_nano/nrf52840/zmk -- -DSHIELD=corne_left -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
west build -s zmk/app -d build/corne_right -b nice_nano/nrf52840/zmk -- -DSHIELD=corne_right -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
```

## Dependency reproducibility status

`config/west.yml` and the reusable workflow pin ZMK to `6e2ef41e022d555b10f116e395832913f71717b3`. Both `corne_left` and `corne_right` compiled successfully at that revision with the matching Zephyr toolchain. Update both pins together only after rebuilding both halves.

## Validation

Run the static checks without a local ZMK checkout:

```sh
python3 scripts/validate.py
git diff --check
```

The checks validate the four 42-key layers, exact ADJ Windows and Bluetooth/maintenance positions, documentation synchronization, build metadata, current ZMK configuration, and dependency pins. They do not compile firmware or test physical hardware.
