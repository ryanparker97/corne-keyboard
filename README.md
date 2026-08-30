# Corne v4 ZMK Configuration for Windows

This repository builds a Windows-focused ZMK layout for a 42-key Corne v4 split using nice!nano-compatible controllers. It preserves the supplied bilateral home-row modifiers and physical layer geometry while replacing the source layout's host shortcuts with native Windows actions.

ZMK is pinned to the known-good revision `6e2ef41e022d555b10f116e395832913f71717b3`. The build matrix uses `nice_nano/nrf52840/zmk` with the generic `corne_left` and `corne_right` shields and produces `corne_v4_left` and `corne_v4_right` artifacts.

## Layout overview

- `BASE`: familiar QWERTY with corner `ESC`/`BACKSPACE`, base `TAB`, bottom-right `RIGHT CTRL`, and `LEFT ALT`/`RAISE`/`LEFT CTRL` thumbs.
- `LOWER`: digits, arrows, immediate plain CAGS modifiers, and `F1`-`F12`.
- `RAISE`: symbols, immediate plain CAGS modifiers, Task View, and the Windows emoji picker.
- `ADJUST`: guarded Bluetooth, output, media, brightness, boot/reset controls, and Windows shortcuts. Hold `LOWER` and `RAISE` together.

The bilateral home-row modifiers retain the supplied balanced 280 ms profile, 150 ms prior-idle gate, 175 ms quick-tap window, opposite-hand triggers, and release triggering. Same-hand rolls resolve as taps; cross-hand chords can resolve as holds.

The `LEFT CTRL` thumb is physical position 38 on all four layers. The D/K home-row holds remain the left and right GUI/Windows modifiers.

| Tap | Hold | Exact binding |
|---|---|---|
| `A` | Left Ctrl | `&hm_l LCTRL A` |
| `S` | Left Alt | `&hm_l LALT S` |
| `D` | Left GUI / Windows | `&hm_l LGUI D` |
| `F` | Left Shift | `&hm_l LSHFT F` |
| `J` | Right Shift | `&hm_r RSHFT J` |
| `K` | Right GUI / Windows | `&hm_r RGUI K` |
| `L` | Right Alt | `&hm_r RALT L` |
| `;` | Right Ctrl | `&hm_r RCTRL SEMI` |

## Native Windows shortcuts

Position names refer to physical base positions. `LG`, `LC`, and `LS` mean GUI/Windows, Ctrl, and Shift.

| Physical position | Exact ZMK binding | Windows action |
|---|---|---|
| `/` | `&kp LG(TAB)` | Win+Tab: Task View |
| Bottom-right `CTRL` | `&kp LG(DOT)` | Win+Period: emoji picker |
| `Y` | `&kp PSCRN` | Print Screen |
| `U` | `&kp LG(LS(S))` | Win+Shift+S: screen snip |
| `I` | `&kp LG(S)` | Win+S: Search |
| `O` | `&kp LG(LC(LEFT))` | Win+Ctrl+Left: previous virtual desktop |
| `P` | `&kp LG(LC(RIGHT))` | Win+Ctrl+Right: next virtual desktop |
| Top-right `BACKSPACE` | `&kp LG(L)` | Win+L: lock Windows |

Task View and emoji are on `RAISE`; the remaining rows are on `ADJUST`.

## Guarded controls

`ADJUST` keeps bootloader on the physical `ESC` position and system reset on physical `LEFT SHIFT`. Bluetooth profile selection remains on `Q` through `T`, with `&bt BT_CLR` on physical `TAB`. Output selection remains available as `&out OUT_USB`, `&out OUT_BLE`, and `&out OUT_TOG` on physical `C`, `V`, and `N`. These controls require both layer thumbs; unused `ADJUST` positions are blocked with `&none`.

The output bindings run on the left central. They set the preferred transport; pinned ZMK automatically falls back to the other ready transport when the preferred one is unavailable. The right half forwards key positions to the central over BLE and is not a standalone USB keyboard.

Media previous, play/pause, next, mute, and volume-down are on physical `A` through `G`; brightness down/up are on `Z`/`X`, volume up is on `B`, and Caps Lock is on `L`. RGB underglow is disabled, so the keymap intentionally contains no RGB controls. See [KEYMAP.md](KEYMAP.md) for all 42 positions.

## Configuration and safety

`config/corne.conf` holds settings shared by both halves: disabled encoder/RGB hardware, display and power behavior, supported connection preferences, and ZMK's aggregate Bluetooth compatibility option. It keeps pinned defaults for report, scan, and split queues and deliberately omits low-level PHY/ACL/data-length/GATT overrides.

At the pinned revision, ZMK loads `config/corne_left.conf` and `config/corne_right.conf` after the shared `config/corne.conf`. The left central explicitly enables both `CONFIG_ZMK_USB=y` and BLE. It also enables HKRO, basic consumer usages, and `CONFIG_ZMK_USB_BOOT=y` for conservative Windows, BIOS/UEFI, and BitLocker compatibility. The right peripheral explicitly keeps BLE enabled and sets `CONFIG_ZMK_USB=n`, avoiding the unsatisfied split-central dependency caused by a shared USB assignment. ZMK Studio remains disabled.

Only flash these artifacts to compatible Corne v4 hardware. Use the artifact matching the half being flashed, then test base keys, HRM holds, both layer thumbs, output selection, Bluetooth pairing, and guarded boot/reset positions before relying on the keyboard. Static checks cannot validate wiring, batteries, radio conditions, or flashing.

## Building

The GitHub Actions workflow validates the repository and builds the two entries in `build.yaml`. Equivalent commands in an initialized ZMK/west workspace are:

```sh
west build -s zmk/app -d build/corne_left -b nice_nano/nrf52840/zmk -- -DSHIELD=corne_left -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
west build -s zmk/app -d build/corne_right -b nice_nano/nrf52840/zmk -- -DSHIELD=corne_right -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
```

Each command writes `zephyr/zmk.uf2` under its build directory. The artifact labels are CI names, not local output filenames.

## Dependency reproducibility status

`config/west.yml` and the reusable workflow pin ZMK to `6e2ef41e022d555b10f116e395832913f71717b3`. Update both references together only after building both halves. Build status: both `corne_left` and `corne_right` completed full pinned-source firmware builds with the documented commands and target configs.

## Validation

```sh
python3 scripts/validate.py
git diff --check
```

The checks validate all four 42-key layers, exact HRM behavior/positions, native Windows chords, guarded controls, disabled RGB state, build metadata, config, documentation, and dependency pins.
