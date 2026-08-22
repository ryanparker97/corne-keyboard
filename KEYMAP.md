# Corne v3.1 keymap

This document mirrors `config/corne.keymap` for a wireless/wired 42-key Corne v3.1 using nice!nano and nice_oled.

## Layers

- `DEF` (0): QWERTY, Escape, Backspace, modifiers, thumbs.
- `LWR` (1): numbers, F-keys, navigation, Tab, Delete.
- `RSE` (2): symbols and Ctrl-arrow editor resize chords.
- `ADJ` (3): Bluetooth profiles, output selection, RGB controls, bootloader/reset, macOS utility chords.

`ADJ` is a conditional layer when `LWR` and `RSE` are both active.

## Thumb row

ZMK Corne binding order is 36 finger keys, then left thumbs outer-to-inner, then right thumbs inner-to-outer. All layers use:

```text
Left thumbs, outer -> inner:  LALT  RAISE  CMD
Right thumbs, inner -> outer: SPACE  LOWER  ENTER
Raw bindings: &kp LALT  &mo RSE  &kp LGUI    &kp SPACE  &mo LWR  &kp RET
```

macOS Command is on the inner-left thumb as `LGUI`. Space is on the inner-right thumb.

## DEF

```text
ESC   Q  W  E  R  T        Y  U  I  O  P  BSPC
CAPS  A  S  D  F  G        H  J  K  L  ;  '
LSFT  Z  X  C  V  B        N  M  ,  .  /  LCTRL
              LALT RSE CMD    SPACE LWR RET
```

## LWR

```text
`    1   2   3   4   5       6     7      8      9     0    DEL
TAB  F1  F2  F3  F4  F5      LEFT  DOWN   UP     RGHT  PGDN trans
trns F6  F7  F8  F9  F10     HOME  PGDN   PGUP   END   F11  F12
              LALT RSE CMD    SPACE LWR RET
```

## RSE

```text
~     !   @   #   $   %       ^       &      *      (      )    ?
ESC   -   =   [   ]   \\      C-LEFT  C-DOWN C-UP   C-RGHT :    "
trns  _   +   {   }   |       HOME    PGDN   PGUP   END    <    >
              LALT RSE CMD    SPACE LWR RET
```

## ADJ

```text
trns  BT1   BT2   BT3   BT4   BT5      SCRN   AREA   CAP    SPOT   APP    LOCK
BTCLR trns  trns  trns  trns  trns     RGBEF  RGBT   RGBON  RGBOF  RGBHU  RGBSA
trns  trns  trns  trns  trns  trns     USB    BLE    TOG    trns   BOOT   RESET
              LALT RSE CMD    SPACE LWR RET
```

RGB controls are guarded on `ADJ`; Bluetooth select/clear controls are preserved there as well. Output controls use ZMK `&out OUT_USB`, `&out OUT_BLE`, and `&out OUT_TOG` on the right side of the bottom row while preserving bootloader and reset.

For wired use, plug USB into the left/central half. The right half still communicates to the left over split BLE. When both USB and BLE are available, ZMK prefers USB by default; use the `ADJ` output controls to choose BLE, USB, or toggle between them.

## LED chain length

The pinned/upstream ZMK Corne `nice_nano` overlay defines the `led_strip` node. This keymap only overrides `&led_strip { chain-length = <27>; };` for a fully LED-populated Corne v3.1: 42 per-key SK6812 plus 12 underglow WS2812, or 27 LEDs per half. Change this to `<6>` if only the underglow LEDs are soldered.
