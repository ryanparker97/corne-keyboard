# Corne v4 Windows keymap

This document mirrors `config/corne.keymap` for a wireless/wired 42-key Corne v4 using nice!nano and nice_oled. The pinned upstream ZMK revision uses generic `corne_left`/`corne_right` shields for this target.

## Layers

- `DEF` (0): QWERTY, Escape, Backspace, modifiers, thumbs.
- `LWR` (1): numbers, F-keys, navigation, Tab, Delete.
- `RSE` (2): symbols and Ctrl-arrow editor resize chords.
- `ADJ` (3): Bluetooth profiles, Windows utilities, media controls, output selection, bootloader/reset.

`ADJ` is a conditional layer when `LWR` and `RSE` are both active.

## Thumb row

ZMK Corne binding order is 36 finger keys, then left thumbs outer-to-inner, then right thumbs inner-to-outer. All layers use:

```text
Left thumbs, outer -> inner:  LALT  RAISE  SPACE
Right thumbs, inner -> outer: RWIN  LOWER  ENTER
Raw bindings: &kp LALT  &mo RSE  &kp SPACE    &kp RWIN  &mo LWR  &kp RET
```

Space is on the inner-left thumb. `RWIN` is the Windows key on the inner-right thumb.

## DEF

```text
ESC   Q  W  E  R  T        Y  U  I  O  P  BSPC
CAPS  A  S  D  F  G        H  J  K  L  ;  '
LSFT  Z  X  C  V  B        N  M  ,  .  /  LCTRL
              LALT RSE SPACE    RWIN LWR RET
```

## LWR

```text
`    1   2   3   4   5       6     7      8      9     0    DEL
TAB  F1  F2  F3  F4  F5      LEFT  DOWN   UP     RGHT  PGDN trans
trns F6  F7  F8  F9  F10     HOME  PGDN   PGUP   END   F11  F12
              LALT RSE SPACE    RWIN LWR RET
```

## RSE

```text
~     !   @   #   $   %       ^       &      *      (      )    ?
ESC   -   =   [   ]   \\      C-LEFT  C-DOWN C-UP   C-RGHT :    "
trns  _   +   {   }   |       HOME    PGDN   PGUP   END    <    >
              LALT RSE SPACE    RWIN LWR RET
```

## ADJ

```text
trns  BT1   BT2   BT3   BT4   BT5      PSCRN  WIN+S+S  WIN+V  WIN+S  WIN+TAB  WIN+L
BTCLR trns  trns  trns  trns  trns     PREV   PLAY     NEXT   MUTE   VOLD     VOLU
trns  trns  trns  trns  trns  trns     USB    BLE      TOG    trns   BOOT     RESET
              LALT RSE SPACE    RWIN LWR RET
```

Windows utility chords on the top-right are Print Screen, Win+Shift+S, Win+V, Win+S, Win+Tab, and Win+L. Media controls on the right home row are previous, play/pause, next, mute, volume down, and volume up.

Bluetooth select/clear controls are preserved on `ADJ`. Output controls use ZMK `&out OUT_USB`, `&out OUT_BLE`, and `&out OUT_TOG` on the right side of the bottom row while preserving bootloader and reset.

For wired use, plug USB into the left/central half. The right half still communicates to the left over split BLE. When both USB and BLE are available, ZMK prefers USB by default; use the `ADJ` output controls to choose BLE, USB, or toggle between them.

## RGB and LED chain length

RGB underglow/per-key LEDs are disabled because the Corne v4 LED count and pinout are unknown. The keymap has no `&rgb_ug` bindings and no `&led_strip` chain-length override.
