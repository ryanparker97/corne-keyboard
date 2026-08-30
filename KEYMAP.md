# Corne v4 Windows Keymap

This document mirrors [`config/corne.keymap`](config/corne.keymap): a four-layer, 42-key Windows layout with bilateral home-row modifiers and the supplied Corne geometry.

## Layers and activation

| Layer | Purpose | Activation |
|---|---|---|
| `BASE` | QWERTY and timed home-row modifiers | Default |
| `LOWER` | Numbers, arrows, function keys, and plain modifiers | Hold right-middle `LOWER` |
| `RAISE` | Symbols, Task View, emoji, and plain modifiers | Hold left-middle `RAISE` |
| `ADJUST` | Windows, Bluetooth, output, media, and maintenance controls | Hold `LOWER` + `RAISE` |

`ADJUST` is selected by `if-layers = <LOWER RAISE>; then-layer = <ADJUST>;`.

## Base (`BASE`)

| Row | Left six positions | Right six positions |
|---|---|---|
| Top | `ESC` `Q` `W` `E` `R` `T` | `Y` `U` `I` `O` `P` `BACKSPACE` |
| Home | `TAB` `A/Ctrl` `S/Alt` `D/Windows` `F/Shift` `G` | `H` `J/Shift` `K/Windows` `L/Alt` `;/Ctrl` `'` |
| Bottom | `LEFT SHIFT` `Z` `X` `C` `V` `B` | `N` `M` `,` `.` `/` `RIGHT CTRL` |
| Thumbs | `LEFT ALT` `RAISE` `LEFT CTRL` | `SPACE` `LOWER` `ENTER` |

The separate `TAB`, bottom-right `RIGHT CTRL`, and left-inner `LEFT CTRL` thumb are physical base positions. The thumb is position 38 and remains `LEFT CTRL` on all four layers; the D/K home-row holds remain GUI/Windows modifiers.

### Bilateral home-row modifiers

Both behaviors are balanced hold-taps with a 280 ms tapping term, 150 ms prior-idle requirement, 175 ms quick-tap window, opposite-hand trigger positions, and `hold-trigger-on-release`.

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

## Lower (`LOWER`)

| Row | Left six positions | Right six positions |
|---|---|---|
| Top | `` ` `` `1` `2` `3` `4` `5` | `6` `7` `8` `9` `0` `DELETE` |
| Home | `LEFT` `LEFT CTRL` `LEFT ALT` `LEFT GUI` `LEFT SHIFT` `DOWN` | `UP` `RIGHT SHIFT` `RIGHT GUI` `RIGHT ALT` `RIGHT CTRL` `RIGHT` |
| Bottom | `F1` `F2` `F3` `F4` `F5` `F6` | `F7` `F8` `F9` `F10` `F11` `F12` |
| Thumbs | `LEFT ALT` `RAISE` `LEFT CTRL` | `SPACE` `LOWER` `ENTER` |

The plain CAGS keys act immediately and avoid hold-tap timing while a layer is active.

## Raise (`RAISE`)

| Row | Left six positions | Right six positions |
|---|---|---|
| Top | `~` `!` `@` `#` `$` `%` | `^` `&` `*` `(` `)` `?` |
| Home | `-` `LEFT CTRL` `LEFT ALT` `LEFT GUI` `LEFT SHIFT` `=` | `[` `RIGHT SHIFT` `RIGHT GUI` `RIGHT ALT` `RIGHT CTRL` `]` |
| Bottom | `\\` `:` `"` `_` `+` `{` | `}` `|` `<` `>` `TASK VIEW` `EMOJI` |
| Thumbs | `LEFT ALT` `RAISE` `LEFT CTRL` | `SPACE` `LOWER` `ENTER` |

## Native Windows shortcuts

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

The first two shortcuts are on `RAISE`; the other six are on `ADJUST`.

## Adjust (`ADJUST`)

| Row | Left six positions | Right six positions |
|---|---|---|
| Top | `BOOT` `BT 1` `BT 2` `BT 3` `BT 4` `BT 5` | `PRINT SCREEN` `SNIP` `SEARCH` `DESKTOP LEFT` `DESKTOP RIGHT` `LOCK` |
| Home | `BT CLEAR` `MEDIA PREV` `PLAY/PAUSE` `MEDIA NEXT` `MUTE` `VOL DOWN` | `NONE` `NONE` `NONE` `CAPS LOCK` `NONE` `NONE` |
| Bottom | `RESET` `BRIGHTNESS DOWN` `BRIGHTNESS UP` `USB` `BLE` `VOL UP` | `OUTPUT TOGGLE` `NONE` `NONE` `NONE` `NONE` `NONE` |
| Thumbs | `LEFT ALT` `RAISE` `LEFT CTRL` | `SPACE` `LOWER` `ENTER` |

Bootloader is guarded at physical `ESC`; reset is guarded at physical `LEFT SHIFT`. Profiles use `&bt BT_SEL 0` through `&bt BT_SEL 4`, and pairing clear uses `&bt BT_CLR`. Output controls are `&out OUT_USB`, `&out OUT_BLE`, and `&out OUT_TOG`. Unused positions use `&none`, preventing base actions from leaking through this maintenance layer.

## USB and BLE behavior

The left central is the host-facing half. `config/corne_left.conf` enables USB and BLE, HKRO, basic consumer usages, and `CONFIG_ZMK_USB_BOOT=y` for Windows and BIOS/UEFI compatibility. `config/corne_right.conf` keeps the right half BLE-only; it forwards key positions to the central and is not a standalone USB keyboard.

The three `&out` bindings choose the preferred central output. If that transport is unavailable, pinned ZMK falls back to the other ready transport. Bluetooth profile selection affects the central's host connection, not the right-to-left split link.

RGB underglow is disabled, so no RGB bindings or LED overrides are present.

## Validation

```sh
python3 scripts/validate.py
git diff --check
```

The static checks verify every binding position, both HRM definitions, documentation, current config, build targets, and pinned dependencies.
