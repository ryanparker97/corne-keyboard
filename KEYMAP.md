# Corne v4 Windows Keymap

This document mirrors [`config/corne.keymap`](config/corne.keymap), a 42-key Corne v4 QWERTY layout for Windows. It preserves NJ68 transition priorities: corner `ESC`/`BACKSPACE`, a separate right-thumb `SPACE`/`LOWER`/`ENTER` cluster, and predictable number, symbol, navigation, and utility layers.

## Layers and activation

| Layer | Purpose | Activation |
|---|---|---|
| `DEF` | Windows QWERTY base layer | Default |
| `LWR` | Numbers, function keys, navigation, `TAB`, and `CTRL` thumb | Hold right-middle `LOWER` (`&mo 1`) |
| `RSE` | Symbols, paired punctuation, and Ctrl-arrow chords | Hold left-middle `RAISE` (`&mo 2`) |
| `ADJ` | Bluetooth, Windows shortcuts, bootloader, and reset | Hold `LOWER` and `RAISE` together |

`ADJ` is a ZMK conditional layer: `if-layers = <LWR RSE>; then-layer = <ADJ>;`. `&trans` falls through to a lower-priority active layer. `LG`, `LS`, and `LC` in a binding mean Left GUI (Windows key), Left Shift, and Left Control.

## Default layer (`DEF`)

| Row | Left six positions | Right six positions |
|---|---|---|
| Top | `ESC` `Q` `W` `E` `R` `T` | `Y` `U` `I` `O` `P` `BACKSPACE` |
| Home | `CAPS LOCK` `A` `S` `D` `F` `G` | `H` `J` `K` `L` `;` `'` |
| Bottom | `LEFT SHIFT` `Z` `X` `C` `V` `B` | `N` `M` `,` `.` `/` `LEFT CTRL` |
| Thumbs | `LEFT ALT` `RAISE` `LEFT GUI` | `SPACE` `LOWER` `ENTER` |

`CAPS LOCK` is a plain firmware key; no external host remapper is required. The left GUI thumb sends the Windows key. `LOWER` is momentary and `ENTER` is its own right-inner thumb key.

## Lower (`LWR`) and Raise (`RSE`)

`LWR` top row supplies `` ` 1 2 3 4 5`` and `6 7 8 9 0 DELETE`. Its home row supplies `TAB`, `F1`-`F5`, arrows, and `PAGE UP`; its bottom row supplies `LEFT ALT`, `F6`-`F12`, `HOME`, `PAGE DOWN`, `PAGE UP`, and `END`. The left-outer thumb becomes `LEFT CTRL`, enabling held `LOWER` + thumb + number shortcuts.

`RSE` supplies paired symbols. Its right home row emits `CTRL+LEFT`, `CTRL+DOWN`, `CTRL+UP`, and `CTRL+RIGHT`; these are normal Windows Ctrl-arrow events. Minus is on the second left home-row position of `RSE`.

## Adjust (`ADJ`) Windows workflow

Actions are labeled by physical base-layer position. The exact bindings below are the firmware behavior; no host automation is assumed.

| Physical position | Exact ZMK binding | Windows action |
|---|---|---|
| `Y` | `&kp PSCRN` | Print Screen |
| `U` | `&kp LG(LS(S))` | Win+Shift+S screen snip |
| `I` | `&kp LG(V)` | Win+V Clipboard history |
| `O` | `&kp LG(S)` | Win+S Search |
| `P` | `&kp LG(TAB)` | Win+Tab Task View |
| Top-right `BACKSPACE` | `&kp LG(L)` | Win+L lock Windows |
| `A` | `&kp LC(A)` | Ctrl+A select all |
| `S` | `&kp LC(S)` | Ctrl+S save |
| `D` | `&kp LG(R)` | Win+R Run |
| `F` | `&kp LC(F)` | Ctrl+F find |
| `G` | `&kp LG(LEFT)` | Win+Left snap left |
| `H` | `&kp LG(RIGHT)` | Win+Right snap right |
| `Z` | `&kp LC(Z)` | Ctrl+Z undo |
| `X` | `&kp LC(X)` | Ctrl+X cut |
| `C` | `&kp LC(C)` | Ctrl+C copy |
| `V` | `&kp LC(V)` | Ctrl+V paste |
| `B` | `&kp LC(LS(Z))` | Ctrl+Shift+Z redo |

The remaining `ADJ` positions retain Bluetooth and maintenance controls:

| Physical positions | Exact binding | Behavior |
|---|---|---|
| `Q` through `T` | `&bt BT_SEL 0` through `&bt BT_SEL 4` | Select Bluetooth profiles 1 through 5 |
| `CAPS` | `&bt BT_CLR` | Clear Bluetooth pairing information |
| `/` | `&bootloader` | Enter bootloader |
| Bottom-right `CTRL` | `&sys_reset` | System reset |

All other ADJ finger and thumb positions are transparent. This preserves the 42-key layer shape and avoids moving Bluetooth, bootloader, or reset controls.

## Validation

```sh
python3 scripts/validate.py
git diff --check
```

The static keymap check verifies 42 bindings on every layer and exact ADJ positions. The documentation check independently requires this file and `README.md` to describe the native Windows bindings.
