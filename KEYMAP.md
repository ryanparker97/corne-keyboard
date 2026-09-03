# Corne v4 macOS data engineering / DevOps keymap

This is the exact physical reference for [`config/corne.keymap`](config/corne.keymap): a plain QWERTY, 42-key macOS layout tuned for data engineering and DevOps. It has no home-row modifiers or other dual-role letter keys.

## Activation

| Layer | Purpose | Activation |
|---|---|---|
| `BASE` / Base | Plain QWERTY and dedicated macOS modifiers | Default |
| `LOWER` / Nav/Num | Numbers, navigation, Vim/tmux prefixes, F-keys | Hold `LOWER` |
| `RAISE` / Symbols | Python/data/ops symbols | Hold `RAISE` |
| `ADJUST` / System | macOS, Bluetooth, output, media, maintenance | Hold `LOWER` + `RAISE` |

The conditional layer uses `if-layers = <LOWER RAISE>; then-layer = <ADJUST>;`.

## Base

| Row | Left six positions | Right six positions |
|---|---|---|
| Top | `ESC` `Q` `W` `E` `R` `T` | `Y` `U` `I` `O` `P` `BACKSPACE` |
| Home | `TAB` `A` `S` `D` `F` `G` | `H` `J` `K` `L` `;` `'` |
| Bottom | `LEFT SHIFT` `Z` `X` `C` `V` `B` | `N` `M` `,` `.` `/` `RIGHT CTRL` |
| Thumbs | `OPTION` `RAISE` `COMMAND` | `SPACE` `LOWER` `ENTER` |

Every letter is an ordinary key. Option and Command occupy left thumbs; Control and Shift are dedicated edge keys. There is no tap-duration decision.

## Lower / Nav/Num

| Row | Left six positions | Right six positions |
|---|---|---|
| Top | `` ` `` `1` `2` `3` `4` `5` | `6` `7` `8` `9` `0` `DELETE` |
| Home | `VIM` `CTRL` `OPTION` `COMMAND` `SHIFT` `TMUX` | `LEFT` `DOWN` `UP` `RIGHT` `PAGE DOWN` `PAGE UP` |
| Bottom | `F1` `F2` `F3` `F4` `F5` `F6` | `F7` `F8` `F9` `F10` `F11` `F12` |
| Thumbs | `CTRL` `RAISE` `COMMAND` | `SPACE` `LOWER` `ENTER` |

The navigation row places arrows on physical H/J/K/L. Layer modifiers are ordinary held keys, enabling Option-arrow word movement, Command-arrow line/document movement, and Shift selection on macOS.

`VIM` is `&vim_window_prefix`, an exact macro that taps and releases `Ctrl-W`. `TMUX` is `&tmux_prefix`, which taps and releases stock tmux `Ctrl-B`. Keep Lower held and tap an arrow after either prefix to select a Vim window or tmux pane. The macro releases Control before the follow-up key.

## Raise / Symbols

| Row | Left six positions | Right six positions |
|---|---|---|
| Top | `~` `!` `@` `#` `$` `%` | `^` `&` `*` `(` `)` `?` |
| Home | `-` `CTRL` `OPTION` `COMMAND` `SHIFT` `=` | `[` `{` `:` `|` `}` `]` |
| Bottom | `\` `'` `"` `_` `+` `` ` `` | `<` `>` `,` `.` `/` `;` |
| Thumbs | `CTRL` `RAISE` `COMMAND` | `SPACE` `LOWER` `ENTER` |

The shifted-number symbols stay in familiar order. The right home row groups Python/data structures and YAML operators. The layer directly covers common Python, PySpark, SQL, YAML/JSON, Terraform/HCL, shell, Docker, and Kubernetes syntax without macros that type commands or deployment operations.

## Adjust / System

| Row | Left six positions | Right six positions |
|---|---|---|
| Top | `BOOT` `BT 1` `BT 2` `BT 3` `BT 4` `BT 5` | `CAPTURE` `CAPS WORD` `CAPS LOCK` `SPOTLIGHT` `APP SWITCHER` `LOCK` |
| Home | `BT CLEAR` `MEDIA PREV` `PLAY/PAUSE` `MEDIA NEXT` `MUTE` `VOL DOWN` | `NONE` `NONE` `NONE` `NONE` `NONE` `NONE` |
| Bottom | `RESET` `BRIGHTNESS DOWN` `BRIGHTNESS UP` `USB` `BLE` `VOL UP` | `OUTPUT TOGGLE` `NONE` `NONE` `NONE` `NONE` `NONE` |
| Thumbs | `CTRL` `RAISE` `COMMAND` | `SPACE` `LOWER` `ENTER` |

### macOS shortcuts

| Physical position | Exact binding | Action |
|---|---|---|
| `Y` / Capture | `&kp LG(LS(N5))` | Shift-Command-5 capture/recording UI |
| `O` / Spotlight | `&kp LG(SPACE)` | Spotlight |
| `P` / App switcher | `&kp LG(TAB)` | Switch applications |
| Top-right / Lock | `&kp LC(LG(Q))` | Lock screen |

Caps Word supports SQL keywords and constants; traditional Caps Lock remains beside it.

Bootloader is guarded at physical `ESC`, reset at physical `LEFT SHIFT`, profile selection at `Q`–`T`, and clear pairing at `TAB`. USB/BLE/output controls remain `&out OUT_USB`, `&out OUT_BLE`, and `&out OUT_TOG` at physical `C`, `V`, and `N`. Every unavailable position is `&none`, not transparent.

RGB underglow is disabled. There are no RGB controls or LED overrides, and former RGB positions are blocked with `&none`. The keymap also leaves Corne v4 shield scan/debounce defaults in control.

## Hardware and host behavior

The build architecture remains `nice_nano/nrf52840/zmk` with `corne_left` and `corne_right`. `config/corne_left.conf` enables USB/BLE central behavior, HKRO, consumer usages, and `CONFIG_ZMK_USB_BOOT=y`; `config/corne_right.conf` keeps the right half BLE-only. The right half forwards positions and is not an independent USB keyboard.

The output preference set by `&out` falls back to the other ready host transport when needed. Bluetooth profiles are central-host pairings and do not replace the split link.

Flash only matching Corne v4 artifacts. Static checks cannot validate hardware, radio links, flashing, or whether host shortcut settings have been remapped.

## Validation

```sh
python3 scripts/validate.py
git diff --check
```

Validation checks every one of the 42 positions on all layers, exact macro definitions, guarded System placement, docs, RGB policy, current config, build targets, and dependency pins.
