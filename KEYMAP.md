# Corne v4 Windows NJ68 transition keymap

This document mirrors `config/corne.keymap` for a 42-key Corne v4 using nice!nano and nice_oled. The pinned upstream ZMK revision uses generic `corne_left`/`corne_right` shields for this target.

## NJ68 transition model

The layout keeps familiar compact-board habits while moving missing keys to layers:

| Habit | Corne placement |
|---|---|
| Top-left Escape | Base top-left `ESC` |
| Top-right Backspace | Base top-right `BACKSPACE` |
| Tab | `LOWER` + left home-row outer key |
| Enter | Right outer thumb `ENTER` |
| Number row | Hold `LOWER`, then top row `1`-`0` |
| Ctrl+number | Hold `LOWER` plus the Lower left outer thumb `LCTRL` |
| Arrows | Hold `LOWER`, then right home-row `LEFT/DOWN/UP/RIGHT` |
| Home/End/Page keys | Hold `LOWER` or `RAISE`, then the right bottom positions |
| Symbols | Hold `RAISE` |
| Utilities | Hold `LOWER` + `RAISE` for `ADJ` |

## Layers

- `DEF` (0): Windows QWERTY with corner Escape/Backspace and dedicated thumb controls.
- `LWR` (1): numbers, F-keys, navigation, Tab, Delete, and a held left-thumb Ctrl.
- `RSE` (2): symbols, paired punctuation, and Ctrl-arrow editor chords.
- `ADJ` (3): Bluetooth profiles, Windows utility chords, Ctrl editing chords, media controls, output selection, bootloader, and reset.

`ADJ` is a conditional layer when `LWR` and `RSE` are both active.

## Thumb row

ZMK Corne binding order is 36 finger keys, then left thumbs outer-to-inner, then right thumbs inner-to-outer.

Default-layer thumbs:

```text
Left thumbs, outer -> inner:  LALT  RAISE  LWIN
Right thumbs, inner -> outer: SPACE  LOWER  ENTER
Raw bindings: &kp LALT  &mo RSE  &kp LWIN    &kp SPACE  &mo LWR  &kp RET
```

On `LWR`, the left outer thumb is `LCTRL` and the remaining thumbs are transparent for the NJ68 Ctrl+number transition. On `RSE` and `ADJ`, all thumbs are transparent.

## DEF

```text
ESC   Q  W  E  R  T        Y  U  I  O  P  BSPC
CAPS  A  S  D  F  G        H  J  K  L  ;  '
LSFT  Z  X  C  V  B        N  M  ,  .  /  LCTRL
              LALT RSE LWIN    SPACE LWR RET
```

## LWR

```text
`     1   2   3   4   5       6     7      8      9     0    DEL
TAB   F1  F2  F3  F4  F5      LEFT  DOWN   UP     RGHT  PGUP trans
LALT  F6  F7  F8  F9  F10     HOME  PGDN   PGUP   END   F11  F12
              LCTRL trans trans    trans trans trans
```

## RSE

```text
~     !   @   #   $   %       ^       &      *      (      )    ?
ESC   -   =   [   ]   \\      C-LEFT  C-DOWN C-UP   C-RGHT :    "
LALT  _   +   {   }   |       HOME    PGDN   PGUP   END    <    >
              trans trans trans    trans trans trans
```

## ADJ

```text
trns  BT1   BT2   BT3   BT4   BT5      PSCRN  WIN+S+S  WIN+V  WIN+S  WIN+TAB  WIN+L
BTCLR C+A   C+S   trns  C+F   trns     PREV   PLAY     NEXT   MUTE   VOLD     VOLU
trns  C+Z   C+X   C+C   C+V   C+Y      USB    BLE      TOG    trns   BOOT     RESET
              trans trans trans    trans trans trans
```

Windows utility chords on the top-right are Print Screen, Win+Shift+S, Win+V, Win+S, Win+Tab, and Win+L. Media controls on the right home row are previous, play/pause, next, mute, volume down, and volume up.

Bluetooth select/clear controls are preserved on `ADJ`. Output controls use ZMK `&out OUT_USB`, `&out OUT_BLE`, and `&out OUT_TOG` on the right side of the bottom row while preserving bootloader and reset.

For wired use, plug USB into the left/central half. The right half still communicates to the left over split BLE. When both USB and BLE are available, ZMK prefers USB by default; use the `ADJ` output controls to choose BLE, USB, or toggle between them.

## RGB and LED chain length

RGB underglow/per-key LEDs are disabled because the Corne v4 LED count and pinout are unknown. The keymap has no `&rgb_ug` bindings and no `&led_strip` chain-length override.
