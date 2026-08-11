# Corne v4 Keyboard Mapping

This is an **NJ68-to-Corne transition layout**. It keeps familiar QWERTY typing and a dedicated top-left `ESC`, while moving high-frequency editing keys to the Corne thumb cluster.

This document describes the current ZMK mapping in [`config/corne.keymap`](config/corne.keymap). It is a static documentation snapshot only and does not change firmware behavior.

## NJ68 transition model

An NJ68 gives you a compact keyboard with a number row, dedicated Escape/Tab/Backspace/Enter, arrows, and navigation keys. A Corne has far fewer physical keys, so this layout translates those habits into layers instead of trying to mirror the NJ68 shape exactly.

| NJ68 habit | Corne transition placement |
|---|---|
| Top-left `Esc` | Base top-left `ESC` |
| Top-left `Tab` | `LOWER` + left home-row outer `TAB` |
| Backspace reach | Right outer thumb `BACKSPACE` |
| Enter key | Right middle thumb tap `ENTER` |
| Number row | Hold right middle thumb `LOWER`, then top row `1`-`0`; add Lower left outer thumb for `CTRL+number` |
| Arrow cluster | Hold `LOWER`, then right home-row `LEFT/DOWN/UP/RIGHT` |
| Home/End/Page keys | Hold `LOWER`, then right bottom/home positions |
| Function row | Hold `LOWER`, then left home/bottom rows `F1`-`F12` |
| Symbols | Hold left middle thumb `RAISE` |

## Chosen macOS layout interpretation

The layout remains a conventional Corne 3x6+3 QWERTY layout, but the thumbs and utility layers are oriented around the NJ68 transition and the verified host setup:

- Karabiner-Elements maps `Caps Lock` to **Hyper** (`command+control+option+shift`) when held and `Escape` when tapped.
- `skhd` binds Hyper chords to `yabai` window and space controls.
- Neovim uses `<Space>` as leader, `<C-h/j/k/l>` for window navigation, and `<C-Arrow>` for window resizing.

The firmware therefore sends normal `Caps Lock` on the left home-row pinky key instead of implementing a firmware macro. Dedicated firmware `Escape` is now on the top-left base key; Karabiner can still make Caps tap as Escape on that host. Keeping Caps plain leaves the host Karabiner rule authoritative and makes Hyper chords work with ordinary base keys, Lower numbers, and Lower arrows.

## Layout legend

- Physical layout: Corne 3x6+3, documented as three 12-key finger rows plus six thumb keys.
- Tables are shown left half first, then right half.
- `transparent` (`&trans`) means the key falls through to the next active lower-priority layer.
- `mo N` activates layer `N` only while held.
- `lt N KEY` taps `KEY`, or activates layer `N` while held.
- `kp KEY` sends a normal keycode.
- `LC(KEY)` is ZMK's left-control modifier wrapper, used here for confirmed Neovim Ctrl-arrow resize mappings.

## Layers and activation

| Layer | Number | Name in keymap | Purpose | Activation |
|---|---:|---|---|---|
| `DEF` | 0 | `default_layer` | macOS QWERTY typing with easy top-left Esc, left-pinky Caps/Hyper, and opposite-hand Space/Command thumbs | Active by default |
| `LWR` | 1 | `lower_layer` | Numbers, function keys, navigation, `TAB`, Option | Hold the right middle thumb `ENTER/LOWER` key (`&lt 1 RET`) |
| `RSE` | 2 | `raise_layer` | Symbols, paired punctuation, Ctrl-arrow chords, Option | Hold the left middle thumb `RAISE` key (`&mo 2`) |
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
| Outer thumb | `LEFT OPTION` | `SPACE` |
| Middle thumb | `RAISE` (`&mo 2`) | `ENTER` when tapped / `LOWER` when held (`&lt 1 RET`) |
| Inner thumb | `LEFT GUI` / macOS Command | `BACKSPACE` |

### Non-default layer thumbs

On `LWR`, the left outer thumb is `LEFT CTRL` for comfortable `CTRL+number` shortcuts while the right thumb holds `ENTER/LOWER`; the remaining `LWR` thumb positions are `transparent`. All `RSE` and `ADJ` thumb positions are `transparent`, so they inherit the active lower-priority behavior unless another higher-priority layer overrides them.

## Layer 0: `DEF` / default macOS QWERTY

Source node: `default_layer`.

| Row | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `ESC` `Q` `W` `E` `R` `T` | `Y` `U` `I` `O` `P` `-` |
| Home | `CAPS LOCK` `A` `S` `D` `F` `G` | `H` `J` `K` `L` `;` `'` |
| Bottom | `LEFT SHIFT` `Z` `X` `C` `V` `B` | `N` `M` `,` `.` `/` `LEFT CTRL` |
| Thumbs | `LEFT OPTION` `RAISE` `LEFT GUI` | `SPACE` `ENTER/LOWER` `BACKSPACE` |

Raw bindings by position:

| Position | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `&kp ESC` `&kp Q` `&kp W` `&kp E` `&kp R` `&kp T` | `&kp Y` `&kp U` `&kp I` `&kp O` `&kp P` `&kp MINUS` |
| Home | `&kp CAPS` `&kp A` `&kp S` `&kp D` `&kp F` `&kp G` | `&kp H` `&kp J` `&kp K` `&kp L` `&kp SEMI` `&kp SQT` |
| Bottom | `&kp LSHFT` `&kp Z` `&kp X` `&kp C` `&kp V` `&kp B` | `&kp N` `&kp M` `&kp COMMA` `&kp DOT` `&kp FSLH` `&kp LCTRL` |
| Thumbs | `&kp LALT` `&mo 2` `&kp LGUI` | `&kp SPACE` `&lt 1 RET` `&kp BSPC` |

Displaced base keys from the prior documented layout: `Caps Lock` moved from the left outer thumb to the left home-row outer pinky key; `LEFT CTRL` moved from the left home-row outer key to the right bottom-row outer key; `ESC` moved to the top-left base key; `TAB` moved to Lower left home-row outer; `BACKSPACE` moved from top-row far-right to the right outer thumb; `MINUS` moved onto the top-row far-right key; the previous right-side `RIGHT SHIFT` base key was removed, with `LEFT SHIFT` retained on the left bottom-row outer key.

## Layer 1: `LWR` / numbers, function keys, navigation, Tab, Option

Source node: `lower_layer`. Activated by holding default-layer `ENTER/LOWER` (`&lt 1 RET`) on the right middle thumb. The Lower left outer thumb is `LEFT CTRL`, intended for comfortable `CTRL+number` shortcuts while the right thumb holds Lower.

| Row | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `` ` `` `1` `2` `3` `4` `5` | `6` `7` `8` `9` `0` `DELETE` |
| Home | `TAB` `F1` `F2` `F3` `F4` `F5` | `LEFT` `DOWN` `UP` `RIGHT` `PAGE UP` `transparent` |
| Bottom | `LEFT OPTION` `F6` `F7` `F8` `F9` `F10` | `HOME` `PAGE DOWN` `PAGE UP` `END` `F11` `F12` |
| Thumbs | `LEFT CTRL` `transparent` `transparent` | `transparent` `transparent` `transparent` |

Raw bindings by position:

| Position | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `&kp GRAVE` `&kp N1` `&kp N2` `&kp N3` `&kp N4` `&kp N5` | `&kp N6` `&kp N7` `&kp N8` `&kp N9` `&kp N0` `&kp DEL` |
| Home | `&kp TAB` `&kp F1` `&kp F2` `&kp F3` `&kp F4` `&kp F5` | `&kp LEFT` `&kp DOWN` `&kp UP` `&kp RIGHT` `&kp PG_UP` `&trans` |
| Bottom | `&kp LALT` `&kp F6` `&kp F7` `&kp F8` `&kp F9` `&kp F10` | `&kp HOME` `&kp PG_DN` `&kp PG_UP` `&kp END` `&kp F11` `&kp F12` |
| Thumbs | `&kp LCTRL` `&trans` `&trans` | `&trans` `&trans` `&trans` |

## Layer 2: `RSE` / symbols, paired punctuation, and Ctrl-arrow chords

Source node: `raise_layer`. Activated while holding default-layer `RAISE` (`&mo 2`) on the left middle thumb.

| Row | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `~` `!` `@` `#` `$` `%` | `^` `&` `*` `(` `)` `?` |
| Home | `ESC` `-` `=` `[` `]` `\\` | `CTRL+LEFT` `CTRL+DOWN` `CTRL+UP` `CTRL+RIGHT` `:` `"` |
| Bottom | `LEFT OPTION` `_` `+` `{` `}` `|` | `HOME` `PAGE DOWN` `PAGE UP` `END` `<` `>` |
| Thumbs | `transparent` `transparent` `transparent` | `transparent` `transparent` `transparent` |

Raw bindings by position:

| Position | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `&kp TILDE` `&kp EXCL` `&kp AT` `&kp HASH` `&kp DLLR` `&kp PRCNT` | `&kp CARET` `&kp AMPS` `&kp STAR` `&kp LPAR` `&kp RPAR` `&kp QUESTION` |
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

## Practical common-key coverage baseline

This NJ68 transition layout is checked for the commonly used keys needed for normal typing, shell/editor work, and the verified macOS workflow: all letters, digits, US punctuation pairs, easy top-left `Escape`, Lower `Tab`, `Backspace`, `Delete`, `Enter`, `Space`, `Caps Lock`, standard left-side modifiers, arrows, `Home`, `End`, `Page Up`, `Page Down`, and `F1` through `F12`.

It intentionally does not chase full-size keyboard parity for unconfirmed niche keys such as `Print Screen`, `Scroll Lock`, `Pause`, `Insert`, numpad-only keys, or media controls.

## Host dependencies and verified shortcut rationale

These bindings intentionally depend on host configuration that was read, not modified:

| Evidence | Firmware choice | Resulting use |
|---|---|---|
| `/Users/ryanparker/.config/karabiner/karabiner.json`: `Caps Lock: Hyper when held, Escape when tapped` | Base left home-row pinky key sends `&kp CAPS` | Tap for Escape; hold with keys for `command+control+option+shift` Hyper chords. |
| `/Users/ryanparker/.config/skhd/skhdrc`: `hyper - h/j/k/l` focus windows | Hold Caps/Hyper + base `H/J/K/L` | Focus yabai windows west/south/north/east. |
| `skhdrc`: `hyper - z/f/b/r` | Hold Caps/Hyper + base `Z/F/B/R` | Toggle zoom parent/fullscreen, balance space, rotate space. |
| `skhdrc`: `hyper - 1..5` and `hyper - left/right` | Hold Caps/Hyper + Lower numbers/arrows by holding the Enter/Lower thumb | Focus named spaces `chat`, `terminal`, `web`, `notes`, `default`, or previous/next space. |
| `skhdrc`: `hyper - m` / `hyper - s`, then modal `h/j/k/l` or `1..5` | Hold Caps/Hyper + `M`/`S`, then base directions or Lower numbers by holding the Enter/Lower thumb | Enter move/swap modes and trigger verified yabai warp/swap/space actions. |
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
