# Keymap design notes

42-key Corne, QWERTY, macOS. Settings, pairing and flashing are in [README.md](../README.md).

## Design

- Plain QWERTY. Letters are ordinary keys.
- One hold-tap: Tab/Hyper on the left home-row outer key (balanced flavor, 200 ms tapping term, 150 ms quick-tap, `require-prior-idle-ms = 100`).
- No home-row mods, combos, tap dance or macros. The layer home-row modifiers are plain held keys.

## Thumbs

`OPT SYM CMD | SPACE NAV ENTER`. Holding both middle thumbs gives System through a ZMK conditional layer, in either order.

## Layers

`.` means no key and `_` means falls through to the layer below.

### Base

```text
 ESC      Q    W    E    R    T   |   Y    U    I    O    P    BSPC
 TAB/HYP  A    S    D    F    G   |   H    J    K    L    ;    '
 SHIFT    Z    X    C    V    B   |   N    M    ,    .    /    CTRL
                OPT  SYM  CMD     |   SPACE  NAV  ENTER
```

### Nav/Num (hold the right middle thumb)

```text
 ESC      1    2    3    4    5   |   6     7     8    9      0    BSPC
 TAB/HYP  CTRL OPT  CMD  SHIFT .   |   LEFT  DOWN  UP   RIGHT  HOME END
 SHIFT    .    .    .    .    .   |   .     .     .    .      .    CTRL
                OPT  _    CMD     |   SPACE _     ENTER
```

### Symbols (hold the left middle thumb)

```text
 ESC      !    @    #    $    %   |   ^    &    *    (    )    BSPC
 TAB/HYP  CTRL OPT  CMD  SHIFT .   |   -    =    [    ]    \    `
 SHIFT    .    .    .    .    .   |   _    +    {    }    |    ~
                OPT  _    CMD     |   SPACE _    ENTER
```

### System (hold both middle thumbs)

```text
 BOOT     .    .    .    .    .   |   BT1  BT2  BT3  BT4  BT5  .
 RGBTOG   HUE+ SAT+ BRI+ .    .   |   .    .    .    .    USB  BLE
 RGBMOD   HUE- SAT- BRI- .    BTCLR |  .    .    .    .    .    .
                OPT  _    CMD     |   SPACE _   ENTER
```

## Why it is laid out this way

- Esc is top-left, where it is expected.
- Tab/Hyper sits on the left home-row outer key so skhd's `hyper` is one held key; Tab stays a tap.
- Ctrl is bottom-right, so Ctrl chords are a right-pinky chord with the left hand free for the letter.
- Ctrl, Opt, Cmd, Shift sit on A S D F of Nav/Num and Symbols, so modifier + symbol or arrow chords do not need two adjacent left thumbs.
- Home and End sit next to the arrows. They reach zsh line start/end inside tmux, where `^A` is the prefix.
- System is only active while both thumbs are held, so a roll can no longer leave System latched after one thumb is released. Keys pressed while both thumbs are held still hit System.
- BTCLR is on the B slot, away from every symbol and arrow.
- RGB is off, so the System RGB keys fall through to Symbols: `RGBTOG` = Tab/Hyper, `HUE+` `SAT+` `BRI+` = Ctrl / Opt / Cmd, `RGBMOD` = Shift, and `HUE-` `SAT-` `BRI-` do nothing.

## Not on this layout

There is no Delete, Page Up, Page Down, F1-F12 or media key, and no window-manager layer.

## References

- [Miryoku reference](https://github.com/manna-harbour/miryoku/tree/master/docs/reference)
- [Designing a Symbol Layer](https://getreuer.info/posts/keyboards/symbol-layer/index.html)
- [ZMK v0.3 keymaps](https://v0-3-branch.zmk.dev/docs/keymaps)
- [Apple keyboard shortcuts](https://support.apple.com/en-us/102650)
