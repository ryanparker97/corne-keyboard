# Corne v4 Keyboard Mapping

This document describes the current ZMK mapping in [`config/corne.keymap`](config/corne.keymap). It is a static documentation snapshot only and does not change firmware behavior.

## Chosen macOS layout interpretation

The layout remains a conventional Corne 3x6+3 QWERTY layout, but the thumbs and utility layers are oriented around the verified host setup:

- Karabiner-Elements maps `Caps Lock` to **Hyper** (`command+control+option+shift`) when held and `Escape` when tapped.
- `skhd` binds Hyper chords to `yabai` window and space controls.
- Neovim uses `<Space>` as leader, `<C-h/j/k/l>` for window navigation, and `<C-Arrow>` for window resizing.

The firmware therefore sends normal `Caps Lock` on the left home-row pinky key instead of implementing a firmware macro. That keeps the host Karabiner rule authoritative and makes Hyper chords work with ordinary base keys, Lower numbers, and Lower arrows.

## Layout legend

- Physical layout: Corne 3x6+3, documented as three 12-key finger rows plus six thumb keys.
- Tables are shown left half first, then right half.
- `transparent` (`&trans`) means the key falls through to the next active lower-priority layer.
- `mo N` activates layer `N` only while held.
- `kp KEY` sends a normal keycode.
- `LC(KEY)` is ZMK's left-control modifier wrapper, used here for confirmed Neovim Ctrl-arrow resize mappings.

## Layers and activation

| Layer | Number | Name in keymap | Purpose | Activation |
|---|---:|---|---|---|
| `DEF` | 0 | `default_layer` | macOS QWERTY typing with left-pinky Caps/Hyper plus opposite-hand Space and Command thumbs | Active by default |
| `LWR` | 1 | `lower_layer` | Numbers, function keys, navigation, `ESC`, Option | Hold the left thumb `LOWER` key (`&mo 1`) |
| `RSE` | 2 | `raise_layer` | Symbols, paired punctuation, Ctrl-arrow chords, Option | Hold the right thumb `RAISE` key (`&mo 2`) |
| `ADJ` | 3 | `adjust_layer` | Bluetooth, modifiers, bootloader, reset | Conditional tri-layer when `LWR` and `RSE` are both active |

The `ADJ` layer is configured with ZMK conditional layers:

```dts
if-layers = <LWR RSE>;
then-layer = <ADJ>;
```

## Thumb keys

### Default layer pinky and thumb keys

The dedicated Caps key is on the left home-row outer key, reachable by the left pinky. Karabiner-Elements turns that plain `Caps Lock` into Hyper when held and Escape when tapped.

| Position | Left inner cluster | Right inner cluster |
|---|---|---|
| Outer thumb | `LEFT OPTION` | `LEFT GUI` / macOS Command |
| Middle thumb | `LOWER` (`&mo 1`) | `RAISE` (`&mo 2`) |
| Inner thumb | `SPACE` | `ENTER` |

### Non-default layer thumbs

All thumb positions on `LWR`, `RSE`, and `ADJ` are `transparent`, so they inherit the active lower-priority behavior unless another higher-priority layer overrides them.

## Layer 0: `DEF` / default macOS QWERTY

Source node: `default_layer`.

| Row | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `TAB` `Q` `W` `E` `R` `T` | `Y` `U` `I` `O` `P` `BACKSPACE` |
| Home | `CAPS LOCK` `A` `S` `D` `F` `G` | `H` `J` `K` `L` `;` `'` |
| Bottom | `LEFT SHIFT` `Z` `X` `C` `V` `B` | `N` `M` `,` `.` `/` `LEFT CTRL` |
| Thumbs | `LEFT OPTION` `LOWER` `SPACE` | `LEFT GUI` `RAISE` `ENTER` |

Raw bindings by position:

| Position | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `&kp TAB` `&kp Q` `&kp W` `&kp E` `&kp R` `&kp T` | `&kp Y` `&kp U` `&kp I` `&kp O` `&kp P` `&kp BSPC` |
| Home | `&kp CAPS` `&kp A` `&kp S` `&kp D` `&kp F` `&kp G` | `&kp H` `&kp J` `&kp K` `&kp L` `&kp SEMI` `&kp SQT` |
| Bottom | `&kp LSHFT` `&kp Z` `&kp X` `&kp C` `&kp V` `&kp B` | `&kp N` `&kp M` `&kp COMMA` `&kp DOT` `&kp FSLH` `&kp LCTRL` |
| Thumbs | `&kp LALT` `&mo 1` `&kp SPACE` | `&kp LGUI` `&mo 2` `&kp RET` |

Displaced base keys from the prior documented layout: `Caps Lock` moved from the left outer thumb to the left home-row outer pinky key; `LEFT CTRL` moved from the left home-row outer key to the right bottom-row outer key; the previous right-side `RIGHT SHIFT` base key was removed, with `LEFT SHIFT` retained on the left bottom-row outer key.

## Layer 1: `LWR` / numbers, function keys, navigation, escape, Option

Source node: `lower_layer`. Activated while holding default-layer `LOWER` (`&mo 1`).

| Row | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `` ` `` `1` `2` `3` `4` `5` | `6` `7` `8` `9` `0` `DELETE` |
| Home | `ESC` `F1` `F2` `F3` `F4` `F5` | `LEFT` `DOWN` `UP` `RIGHT` `PAGE UP` `transparent` |
| Bottom | `LEFT OPTION` `F6` `F7` `F8` `F9` `F10` | `HOME` `PAGE DOWN` `PAGE UP` `END` `F11` `F12` |
| Thumbs | `transparent` `transparent` `transparent` | `transparent` `transparent` `transparent` |

Raw bindings by position:

| Position | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `&kp GRAVE` `&kp N1` `&kp N2` `&kp N3` `&kp N4` `&kp N5` | `&kp N6` `&kp N7` `&kp N8` `&kp N9` `&kp N0` `&kp DEL` |
| Home | `&kp ESC` `&kp F1` `&kp F2` `&kp F3` `&kp F4` `&kp F5` | `&kp LEFT` `&kp DOWN` `&kp UP` `&kp RIGHT` `&kp PG_UP` `&trans` |
| Bottom | `&kp LALT` `&kp F6` `&kp F7` `&kp F8` `&kp F9` `&kp F10` | `&kp HOME` `&kp PG_DN` `&kp PG_UP` `&kp END` `&kp F11` `&kp F12` |
| Thumbs | `&trans` `&trans` `&trans` | `&trans` `&trans` `&trans` |

## Layer 2: `RSE` / symbols, paired punctuation, and Ctrl-arrow chords

Source node: `raise_layer`. Activated while holding default-layer `RAISE` (`&mo 2`).

| Row | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `~` `!` `@` `#` `$` `%` | `^` `&` `*` `(` `)` `BACKSPACE` |
| Home | `ESC` `-` `=` `[` `]` `\\` | `CTRL+LEFT` `CTRL+DOWN` `CTRL+UP` `CTRL+RIGHT` `:` `"` |
| Bottom | `LEFT OPTION` `_` `+` `{` `}` `|` | `HOME` `PAGE DOWN` `PAGE UP` `END` `<` `>` |
| Thumbs | `transparent` `transparent` `transparent` | `transparent` `transparent` `transparent` |

Raw bindings by position:

| Position | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `&kp TILDE` `&kp EXCL` `&kp AT` `&kp HASH` `&kp DLLR` `&kp PRCNT` | `&kp CARET` `&kp AMPS` `&kp STAR` `&kp LPAR` `&kp RPAR` `&kp BSPC` |
| Home | `&kp ESC` `&kp MINUS` `&kp EQUAL` `&kp LBKT` `&kp RBKT` `&kp BSLH` | `&kp LC(LEFT)` `&kp LC(DOWN)` `&kp LC(UP)` `&kp LC(RIGHT)` `&kp COLON` `&kp DQT` |
| Bottom | `&kp LALT` `&kp UNDER` `&kp PLUS` `&kp LBRC` `&kp RBRC` `&kp PIPE` | `&kp HOME` `&kp PG_DN` `&kp PG_UP` `&kp END` `&kp LT` `&kp GT` |
| Thumbs | `&trans` `&trans` `&trans` | `&trans` `&trans` `&trans` |

## Layer 3: `ADJ` / Bluetooth, modifiers, and system

Source node: `adjust_layer`. Activated only while both `LWR` and `RSE` are active.

| Row | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `transparent` `BT profile 1` `BT profile 2` `BT profile 3` `BT profile 4` `BT profile 5` | `transparent` `transparent` `transparent` `transparent` `transparent` `transparent` |
| Home | `BT clear` `CAPS LOCK` `LEFT GUI` `LEFT OPTION` `LEFT CTRL` `LEFT SHIFT` | `transparent` `transparent` `transparent` `transparent` `transparent` `transparent` |
| Bottom | `transparent` `transparent` `transparent` `transparent` `transparent` `transparent` | `transparent` `transparent` `transparent` `transparent` `BOOTLOADER` `SYSTEM RESET` |
| Thumbs | `transparent` `transparent` `transparent` | `transparent` `transparent` `transparent` |

Raw bindings by position:

| Position | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `&trans` `&bt BT_SEL 0` `&bt BT_SEL 1` `&bt BT_SEL 2` `&bt BT_SEL 3` `&bt BT_SEL 4` | `&trans` `&trans` `&trans` `&trans` `&trans` `&trans` |
| Home | `&bt BT_CLR` `&kp CAPS` `&kp LGUI` `&kp LALT` `&kp LCTRL` `&kp LSHFT` | `&trans` `&trans` `&trans` `&trans` `&trans` `&trans` |
| Bottom | `&trans` `&trans` `&trans` `&trans` `&trans` `&trans` | `&trans` `&trans` `&trans` `&trans` `&bootloader` `&sys_reset` |
| Thumbs | `&trans` `&trans` `&trans` | `&trans` `&trans` `&trans` |

## Host dependencies and verified shortcut rationale

These bindings intentionally depend on host configuration that was read, not modified:

| Evidence | Firmware choice | Resulting use |
|---|---|---|
| `/Users/ryanparker/.config/karabiner/karabiner.json`: `Caps Lock: Hyper when held, Escape when tapped` | Base left home-row pinky key sends `&kp CAPS` | Tap for Escape; hold with keys for `command+control+option+shift` Hyper chords. |
| `/Users/ryanparker/.config/skhd/skhdrc`: `hyper - h/j/k/l` focus windows | Hyper thumb + base `H/J/K/L` | Focus yabai windows west/south/north/east. |
| `skhdrc`: `hyper - z/f/b/r` | Hyper thumb + base `Z/F/B/R` | Toggle zoom parent/fullscreen, balance space, rotate space. |
| `skhdrc`: `hyper - 1..5` and `hyper - left/right` | Hyper thumb + Lower numbers/arrows | Focus named spaces `chat`, `terminal`, `web`, `notes`, `default`, or previous/next space. |
| `skhdrc`: `hyper - m` / `hyper - s`, then modal `h/j/k/l` or `1..5` | Hyper thumb + `M`/`S`, then base directions or Lower numbers | Enter move/swap modes and trigger verified yabai warp/swap/space actions. |
| Neovim `lua/ryanparker/core/keymaps.lua`: leader is `<Space>` | Thumb `SPACE` remains unchanged | Preserves leader mappings. |
| Neovim `keymaps.lua`: `<C-h/j/k/l>` window navigation | Base `LEFT CTRL` plus `H/J/K/L` remains unchanged | Produces confirmed Neovim navigation chords without firmware macros. |
| Neovim `keymaps.lua`: `<C-Up/Down/Left/Right>` window resizing | Raise right home-row sends `CTRL+LEFT/DOWN/UP/RIGHT` | Direct access to confirmed Neovim resize chords. |

## Notes on special keycodes

| Legend | Source binding | Meaning documented from keymap |
|---|---|---|
| `BT profile 1` through `BT profile 5` | `&bt BT_SEL 0` through `&bt BT_SEL 4` | Select one of five configured ZMK Bluetooth profiles |
| `BT clear` | `&bt BT_CLR` | Clear Bluetooth pairing information via ZMK Bluetooth behavior |
| `BOOTLOADER` | `&bootloader` | Invoke the ZMK bootloader behavior |
| `SYSTEM RESET` | `&sys_reset` | Invoke the ZMK system reset behavior |
