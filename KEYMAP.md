# Corne v3.1 Keyboard Mapping

This is an **NJ68-to-Corne transition layout**. It keeps familiar QWERTY typing with dedicated top-left `ESC` and top-right `BACKSPACE`, while assigning separate `SPACE`, momentary `LOWER`, and `ENTER` keys to the right thumb cluster and mirroring the base thumb keys on non-default layers.

This document describes the current ZMK mapping in [`config/corne.keymap`](config/corne.keymap). It is a static documentation snapshot only and does not change firmware behavior.

Target hardware for the generated firmware is a standard Corne v3.1 42-key split with nice!nano v2-compatible controllers and 128x32 SSD1306 OLEDs built with `corne_left nice_oled` and `corne_right nice_oled`.

## NJ68 transition model

An NJ68 gives you a compact keyboard with a number row, dedicated Escape/Tab/Backspace/Enter, arrows, and navigation keys. A Corne has far fewer physical keys, so this layout translates those habits into layers instead of trying to mirror the NJ68 shape exactly.

| NJ68 habit | Corne transition placement |
|---|---|
| Top-left `Esc` | Base top-left `ESC` |
| Top-right Backspace reach | Base top-right `BACKSPACE` |
| Top-left `Tab` | `LOWER` + left home-row outer `TAB` |
| Enter key | Right-inner thumb `ENTER` |
| Number row | Hold right-middle thumb `LOWER`, then top row `1`-`0`; the prior Lower left-thumb `CTRL+number` shortcut is removed |
| Arrow cluster | Hold right-middle thumb `LOWER`, then right home-row `LEFT/DOWN/UP/RIGHT` |
| Home/End/Page keys | Hold `LOWER`, then right bottom/home positions |
| Function row | Hold `LOWER`, then left home/bottom rows `F1`-`F12` |
| Symbols, including Minus | Hold left-middle thumb `RAISE` |
| Bluetooth/macOS/system actions | Hold right-middle `LOWER` and left-middle `RAISE` together for `ADJ` |

## Chosen macOS layout interpretation

The layout remains a conventional Corne 3x6+3 QWERTY layout, but the thumbs and utility layers are oriented around the NJ68 transition and the verified host setup:

- Karabiner-Elements maps `Caps Lock` to **Hyper** (`command+control+option+shift`) when held and `Escape` when tapped.
- `skhd` binds those host-produced Hyper chords to `yabai` window and space controls.
- Neovim uses `<Space>` as leader, `<C-h/j/k/l>` for window navigation, and `<C-Arrow>` for window resizing.
- `ADJ` emits 14 fixed macOS productivity chords directly from ZMK firmware and adds guarded RGB underglow controls; these do not require Karabiner, skhd/yabai, or Neovim.

The firmware sends normal `Caps Lock` on the left home-row pinky key instead of implementing Hyper. Dedicated firmware `Escape` is on the top-left base key; Karabiner can still make Caps tap as Escape on that host. Keeping Caps plain leaves the host Karabiner rule authoritative and makes Hyper chords work with ordinary base keys, Lower numbers, and Lower arrows.

## Layout legend

- Physical layout: Corne 3x6+3, documented as three 12-key finger rows plus six thumb keys.
- Tables are shown left half first, then right half.
- A physical base-position label such as `Y` identifies where a key is located; it does not mean an `ADJ` binding emits `Y`.
- `transparent` (`&trans`) means the key falls through to the next active lower-priority layer.
- `mo N` activates layer `N` only while held.
- `kp KEY` sends a normal keycode or wrapped chord.
- `LG(KEY)` applies Left GUI, which is macOS Command; `LS(KEY)` applies Left Shift; `LC(KEY)` applies Left Control.
- Nested wrappers are chords: for example, `&kp LG(LS(N3))` emits Command+Shift+3.

## Layers and activation

| Layer | Number | Name in keymap | Purpose | Activation |
|---|---:|---|---|---|
| `DEF` | 0 | `default_layer` | macOS QWERTY with top-corner Esc/Backspace, left-pinky Caps/Hyper, and dedicated thumb controls | Active by default |
| `LWR` | 1 | `lower_layer` | Numbers, function keys, navigation, `TAB`, Option, mirrored thumbs | Hold right-middle thumb `LOWER` (`&mo 1`) |
| `RSE` | 2 | `raise_layer` | Symbols, paired punctuation, Ctrl-arrow chords, Option, mirrored thumbs | Hold left-middle thumb `RAISE` (`&mo 2`) |
| `ADJ` | 3 | `adjust_layer` | Bluetooth, macOS productivity chords, RGB underglow controls, bootloader, reset, mirrored thumbs | Hold right-middle `LOWER` and left-middle `RAISE` together |

The `ADJ` layer is configured with ZMK conditional layers:

```dts
if-layers = <LWR RSE>;
then-layer = <ADJ>;
```

## Thumb keys

### Default layer pinky and thumb keys

The dedicated Caps key is on the left home-row outer key, reachable by the left pinky. Karabiner-Elements turns that plain `Caps Lock` into Hyper when held and Escape when tapped only on a host with the external rule.

| Position | Left thumb cluster | Right thumb cluster |
|---|---|---|
| Outer | `LEFT OPTION` | `SPACE` |
| Middle | `RAISE` (`&mo 2`) | `LOWER` (`&mo 1`) |
| Inner | `LEFT GUI` / macOS Command | `ENTER` |

`LOWER` is a pure momentary layer key. It does not emit Enter when tapped; Enter is the separate right-inner thumb key. Backspace is not a thumb key: it is the top-right base key.

### Non-default layer thumbs

On `LWR`, `RSE`, and `ADJ`, the thumb rows intentionally mirror the base layer where possible: left-outer `LEFT OPTION`, left-middle `RAISE`, left-inner `LEFT GUI`/Command, right-outer `SPACE`, right-middle `LOWER`, and right-inner `ENTER`. This keeps `LEFT OPTION`, Command, and `ENTER` available off the base layer. It replaces the old Lower left-thumb `LEFT CTRL`/`LEFT SHIFT` special behavior, so `CTRL+number` shortcuts are no longer produced via the Lower left thumb.

## Layer 0: `DEF` / default macOS QWERTY

Source node: `default_layer`.

| Row | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `ESC` `Q` `W` `E` `R` `T` | `Y` `U` `I` `O` `P` `BACKSPACE` |
| Home | `CAPS LOCK` `A` `S` `D` `F` `G` | `H` `J` `K` `L` `;` `'` |
| Bottom | `LEFT SHIFT` `Z` `X` `C` `V` `B` | `N` `M` `,` `.` `/` `LEFT CTRL` |
| Thumbs | `LEFT OPTION` `RAISE` `LEFT GUI` | `SPACE` `LOWER` `ENTER` |

Raw bindings by position:

| Position | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `&kp ESC` `&kp Q` `&kp W` `&kp E` `&kp R` `&kp T` | `&kp Y` `&kp U` `&kp I` `&kp O` `&kp P` `&kp BSPC` |
| Home | `&kp CAPS` `&kp A` `&kp S` `&kp D` `&kp F` `&kp G` | `&kp H` `&kp J` `&kp K` `&kp L` `&kp SEMI` `&kp SQT` |
| Bottom | `&kp LSHFT` `&kp Z` `&kp X` `&kp C` `&kp V` `&kp B` | `&kp N` `&kp M` `&kp COMMA` `&kp DOT` `&kp FSLH` `&kp LCTRL` |
| Thumbs | `&kp LALT` `&mo 2` `&kp LGUI` | `&kp SPACE` `&mo 1` `&kp RET` |

Current displaced-key placement: `Caps Lock` is on the left home-row outer pinky key; `LEFT CTRL` is on the right bottom-row outer key; `ESC` and `BACKSPACE` are the top-left and top-right base keys; `TAB` is on Lower; `ENTER` is the right-inner thumb; and `MINUS` is only on Raise. The previous right-side `RIGHT SHIFT` base key is absent, with `LEFT SHIFT` retained on the left bottom-row outer key.

## Layer 1: `LWR` / numbers, function keys, navigation, Tab, Option

Source node: `lower_layer`. Activated by holding default-layer `LOWER` (`&mo 1`) on the right-middle thumb. The Lower thumb row mirrors the base thumb row, so `LEFT OPTION`, `LEFT GUI`/Command, and `ENTER` remain available while numbers, function keys, navigation, and Tab are active.

| Row | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `` ` `` `1` `2` `3` `4` `5` | `6` `7` `8` `9` `0` `DELETE` |
| Home | `TAB` `F1` `F2` `F3` `F4` `F5` | `LEFT` `DOWN` `UP` `RIGHT` `PAGE UP` `transparent` |
| Bottom | `LEFT OPTION` `F6` `F7` `F8` `F9` `F10` | `HOME` `PAGE DOWN` `PAGE UP` `END` `F11` `F12` |
| Thumbs | `LEFT OPTION` `RAISE` `LEFT GUI` | `SPACE` `LOWER` `ENTER` |

Raw bindings by position:

| Position | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `&kp GRAVE` `&kp N1` `&kp N2` `&kp N3` `&kp N4` `&kp N5` | `&kp N6` `&kp N7` `&kp N8` `&kp N9` `&kp N0` `&kp DEL` |
| Home | `&kp TAB` `&kp F1` `&kp F2` `&kp F3` `&kp F4` `&kp F5` | `&kp LEFT` `&kp DOWN` `&kp UP` `&kp RIGHT` `&kp PG_UP` `&trans` |
| Bottom | `&kp LALT` `&kp F6` `&kp F7` `&kp F8` `&kp F9` `&kp F10` | `&kp HOME` `&kp PG_DN` `&kp PG_UP` `&kp END` `&kp F11` `&kp F12` |
| Thumbs | `&kp LALT` `&mo 2` `&kp LGUI` | `&kp SPACE` `&mo 1` `&kp RET` |

## Layer 2: `RSE` / symbols, paired punctuation, and Ctrl-arrow chords

Source node: `raise_layer`. Activated while holding default-layer `RAISE` (`&mo 2`) on the left-middle thumb. Minus is the second left home-row position on this layer and does not exist on `DEF`. The Raise thumb row mirrors the base thumb row.

| Row | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `~` `!` `@` `#` `$` `%` | `^` `&` `*` `(` `)` `?` |
| Home | `ESC` `-` `=` `[` `]` `\\` | `CTRL+LEFT` `CTRL+DOWN` `CTRL+UP` `CTRL+RIGHT` `:` `"` |
| Bottom | `LEFT OPTION` `_` `+` `{` `}` `|` | `HOME` `PAGE DOWN` `PAGE UP` `END` `<` `>` |
| Thumbs | `LEFT OPTION` `RAISE` `LEFT GUI` | `SPACE` `LOWER` `ENTER` |

Raw bindings by position:

| Position | Left 6 keys | Right 6 keys |
|---|---|---|
| Top | `&kp TILDE` `&kp EXCL` `&kp AT` `&kp HASH` `&kp DLLR` `&kp PRCNT` | `&kp CARET` `&kp AMPS` `&kp STAR` `&kp LPAR` `&kp RPAR` `&kp QUESTION` |
| Home | `&kp ESC` `&kp MINUS` `&kp EQUAL` `&kp LBKT` `&kp RBKT` `&kp BSLH` | `&kp LC(LEFT)` `&kp LC(DOWN)` `&kp LC(UP)` `&kp LC(RIGHT)` `&kp COLON` `&kp DQT` |
| Bottom | `&kp LALT` `&kp UNDER` `&kp PLUS` `&kp LBRC` `&kp RBRC` `&kp PIPE` | `&kp HOME` `&kp PG_DN` `&kp PG_UP` `&kp END` `&kp LT` `&kp GT` |
| Thumbs | `&kp LALT` `&mo 2` `&kp LGUI` | `&kp SPACE` `&mo 1` `&kp RET` |

## Layer 3: `ADJ` / Bluetooth, macOS productivity chords, and system

Source node: `adjust_layer`. Activated only while the right-middle `LOWER` and left-middle `RAISE` thumbs are both held. The conditional layer then overrides the finger positions shown below, while the thumb row mirrors the base thumb row.

Actions are labeled by the key at the same **physical position on `DEF`**. A label such as `Y position` identifies where to press while `ADJ` is active; the binding there emits the chord in the action text rather than the letter `Y`.

| Row | Left 6 physical positions | Right 6 physical positions |
|---|---|---|
| Top | `ESC: transparent` `Q: BT profile 1` `W: BT profile 2` `E: BT profile 3` `R: BT profile 4` `T: BT profile 5` | `Y: full screenshot` `U: selected-area screenshot/snipping` `I: Screenshot app` `O: Spotlight` `P: previous-app switch` `top-right BACKSPACE: lock screen` |
| Home | `CAPS: BT clear` `A: select all` `S: save` `D: transparent` `F: find` `G: transparent` | `H: RGB effect` `J: RGB toggle` `K: RGB on` `L: RGB off` `;: RGB hue increase` `': RGB saturation increase` |
| Bottom | `SHIFT: transparent` `Z: undo` `X: cut` `C: copy` `V: paste` `B: redo` | `N: transparent` `M: transparent` `,: transparent` `.: transparent` `/: BOOTLOADER` `CTRL: SYSTEM RESET` |
| Thumbs | `LEFT OPTION` `RAISE` `LEFT GUI` | `SPACE` `LOWER` `ENTER` |

Exact raw bindings by position:

| Position | Left 6 bindings | Right 6 bindings |
|---|---|---|
| Top | `&trans` `&bt BT_SEL 0` `&bt BT_SEL 1` `&bt BT_SEL 2` `&bt BT_SEL 3` `&bt BT_SEL 4` | `&kp LG(LS(N3))` `&kp LG(LS(N4))` `&kp LG(LS(N5))` `&kp LG(SPACE)` `&kp LG(TAB)` `&kp LC(LG(Q))` |
| Home | `&bt BT_CLR` `&kp LG(A)` `&kp LG(S)` `&trans` `&kp LG(F)` `&trans` | `&rgb_ug RGB_EFF` `&rgb_ug RGB_TOG` `&rgb_ug RGB_ON` `&rgb_ug RGB_OFF` `&rgb_ug RGB_HUI` `&rgb_ug RGB_SAI` |
| Bottom | `&trans` `&kp LG(Z)` `&kp LG(X)` `&kp LG(C)` `&kp LG(V)` `&kp LG(LS(Z))` | `&trans` `&trans` `&trans` `&trans` `&bootloader` `&sys_reset` |
| Thumbs | `&kp LALT` `&mo 2` `&kp LGUI` | `&kp SPACE` `&mo 1` `&kp RET` |

### macOS chord reference

ZMK `LG` is macOS Command, `LS` is Shift, and `LC` is Control. These are firmware-generated key chords and require no Karabiner rule.

| Physical base position | Exact ZMK binding | Emitted chord | macOS action |
|---|---|---|---|
| `Y` | `&kp LG(LS(N3))` | Command+Shift+3 | Full screenshot |
| `U` | `&kp LG(LS(N4))` | Command+Shift+4 | Selected-area screenshot/snipping |
| `I` | `&kp LG(LS(N5))` | Command+Shift+5 | Screenshot app |
| `O` | `&kp LG(SPACE)` | Command+Space | Spotlight |
| `P` | `&kp LG(TAB)` | Command+Tab | Previous-app switch |
| Top-right `BACKSPACE` | `&kp LC(LG(Q))` | Control+Command+Q | Lock screen |
| `A` | `&kp LG(A)` | Command+A | Select all |
| `S` | `&kp LG(S)` | Command+S | Save |
| `F` | `&kp LG(F)` | Command+F | Find |
| `Z` | `&kp LG(Z)` | Command+Z | Undo |
| `X` | `&kp LG(X)` | Command+X | Cut |
| `C` | `&kp LG(C)` | Command+C | Copy |
| `V` | `&kp LG(V)` | Command+V | Paste |
| `B` | `&kp LG(LS(Z))` | Command+Shift+Z | Redo |

### RGB underglow controls

RGB underglow firmware support is enabled with `CONFIG_ZMK_RGB_UNDERGLOW=y` and uses ZMK's `&rgb_ug` behavior. These controls are intentionally placed on currently guarded `ADJ` right-home positions so `DEF`, `LWR`, and `RSE` behavior is unchanged.

| Physical base position on `ADJ` | Exact ZMK binding | Action |
|---|---|---|
| `H` | `&rgb_ug RGB_EFF` | Cycle RGB underglow effect |
| `J` | `&rgb_ug RGB_TOG` | Toggle RGB underglow |
| `K` | `&rgb_ug RGB_ON` | Turn RGB underglow on |
| `L` | `&rgb_ug RGB_OFF` | Turn RGB underglow off |
| `;` | `&rgb_ug RGB_HUI` | Increase RGB underglow hue |
| `'` | `&rgb_ug RGB_SAI` | Increase RGB underglow saturation |

RGB underglow requires compatible LEDs and wiring on the physical keyboard. It can increase battery drain on wireless builds; turn it off from `ADJ` + `L` when battery life matters.

## Practical common-key coverage baseline

This NJ68 transition layout is checked for the commonly used keys needed for normal typing, shell/editor work, and the verified macOS workflow: all letters, digits, US punctuation pairs, top-left `Escape`, top-right `Backspace`, Lower `Tab`, `Delete`, mirrored non-default thumb access to `Enter` and `Space`, `Caps Lock`, standard left-side modifiers, arrows, `Home`, `End`, `Page Up`, `Page Down`, and `F1` through `F12`.

It intentionally does not chase full-size keyboard parity for unconfirmed niche keys such as `Print Screen`, `Scroll Lock`, `Pause`, `Insert`, numpad-only keys, or media controls. Screenshot actions use macOS firmware chords instead of a Print Screen keycode.

## Host dependencies and shortcut rationale

The 14 `ADJ` productivity chords above are implemented entirely in ZMK and do not depend on the host files below. The separate Caps/Hyper, skhd/yabai, and Neovim workflows intentionally depend on host configuration that was read, not modified:

| Evidence | Firmware choice | Resulting use |
|---|---|---|
| `/Users/ryanparker/.config/karabiner/karabiner.json`: `Caps Lock: Hyper when held, Escape when tapped` | Base left home-row pinky key sends `&kp CAPS` | Tap for Escape; hold with keys for `command+control+option+shift` Hyper chords on that host. |
| `/Users/ryanparker/.config/skhd/skhdrc`: `hyper - h/j/k/l` focus windows | Hold Caps/Hyper + base `H/J/K/L` | Focus yabai windows west/south/north/east. |
| `skhdrc`: `hyper - z/f/b/r` | Hold Caps/Hyper + base `Z/F/B/R` | Toggle zoom parent/fullscreen, balance space, rotate space. |
| `skhdrc`: `hyper - 1..5` and `hyper - left/right` | Hold Caps/Hyper + Lower numbers/arrows using the right-middle Lower thumb | Focus named spaces `chat`, `terminal`, `web`, `notes`, `default`, or previous/next space. |
| `skhdrc`: `hyper - m` / `hyper - s`, then modal `h/j/k/l` or `1..5` | Hold Caps/Hyper + `M`/`S`, then base directions or Lower numbers using the right-middle Lower thumb | Enter move/swap modes and trigger verified yabai warp/swap/space actions. |
| Neovim `lua/ryanparker/core/keymaps.lua`: leader is `<Space>` | Thumb `SPACE` remains a dedicated key | Preserves leader mappings. |
| Neovim `keymaps.lua`: `<C-h/j/k/l>` window navigation | Base `LEFT CTRL` plus `H/J/K/L` remains available | Produces confirmed Neovim navigation chords without firmware macros. |
| Neovim `keymaps.lua`: `<C-Up/Down/Left/Right>` window resizing | Raise right home-row sends `CTRL+LEFT/DOWN/UP/RIGHT` | Direct access to confirmed Neovim resize chords. |

## Notes on special keycodes

| Legend | Source binding | Meaning documented from keymap |
|---|---|---|
| `BT profile 1` through `BT profile 5` | `&bt BT_SEL 0` through `&bt BT_SEL 4` | Select one of five configured ZMK Bluetooth profiles |
| `BT clear` | `&bt BT_CLR` | Clear Bluetooth pairing information via ZMK Bluetooth behavior |
| `RGB effect` | `&rgb_ug RGB_EFF` | Cycle ZMK RGB underglow effect |
| `RGB toggle` | `&rgb_ug RGB_TOG` | Toggle ZMK RGB underglow |
| `RGB on` | `&rgb_ug RGB_ON` | Turn ZMK RGB underglow on |
| `RGB off` | `&rgb_ug RGB_OFF` | Turn ZMK RGB underglow off |
| `RGB hue increase` | `&rgb_ug RGB_HUI` | Increase ZMK RGB underglow hue |
| `RGB saturation increase` | `&rgb_ug RGB_SAI` | Increase ZMK RGB underglow saturation |
| `BOOTLOADER` | `&bootloader` | Invoke the ZMK bootloader behavior |
| `SYSTEM RESET` | `&sys_reset` | Invoke the ZMK system reset behavior |
