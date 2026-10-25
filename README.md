# Corne keyboard (ZMK)

ZMK firmware configuration for a 42-key Corne (nice!nano v2, split, Bluetooth + USB) running macOS, with a plain QWERTY base, Hyper on the Tab key and Bluetooth profile keys on the system layer.

- Keymap: [`config/corne.keymap`](config/corne.keymap)
- Settings: [`config/corne.conf`](config/corne.conf)
- Firmware is built by GitHub Actions (ZMK v0.3.0, pinned in `config/west.yml` and the workflow).

## Layout at a glance

Four layers. Every layer has 42 keys; `.` means "no key" and `_` means "falls through to the layer below".

### Base (layer 0)

```text
 TAB/HYP  Q    W    E    R    T   |   Y    U    I    O    P    BSPC
 CTRL     A    S    D    F    G   |   H    J    K    L    ;    '
 SHIFT    Z    X    C    V    B   |   N    M    ,    .    /    ESC
                OPT  NAV  CMD     |   SPACE  SYM  ENTER
```

### Nav/Num (layer 1, hold the left middle thumb): numbers and arrows

```text
 TAB/HYP  1    2    3    4    5   |   6     7     8    9      0    BSPC
 CTRL     .    .    .    .    .   |   LEFT  DOWN  UP   RIGHT  .    .
 SHIFT    .    .    .    .    .   |   .     .     .    .      .    .
                OPT  _    CMD     |   SPACE SYS   ENTER
```

### Symbols (layer 2, hold the right middle thumb)

```text
 TAB/HYP  !    @    #    $    %   |   ^    &    *    (    )    BSPC
 CTRL     .    .    .    .    .   |   -    =    [    ]    \    `
 SHIFT    .    .    .    .    .   |   _    +    {    }    |    ~
                OPT  SYS  CMD     |   SPACE _    ENTER
```

### System (layer 3): Bluetooth, RGB, bootloader

Reach it by holding one middle thumb (Nav/Num or Symbols) and then the other middle thumb.

```text
 BOOT     .    .    .    .    .   |   BT1  BT2  BT3  BT4  BT5  .
 RGBTOG   HUE+ SAT+ BRI+ .    .   |   BTCLR .   .    .    USB  BLE
 RGBMOD   HUE- SAT- BRI- .    .   |   .    .    .    .    .    .
                OPT  _    CMD     |   SPACE _   ENTER
```

## How to use it

### Thumb keys

| Key | Tap | Hold |
|---|---|---|
| `OPT` / `CMD` | Option / Command | same |
| `NAV` (left middle) | n/a | Nav/Num layer (numbers, arrows) |
| `SYM` (right middle) | n/a | Symbols layer |
| `SPACE` / `ENTER` | Space / Enter | n/a |
| Both middle thumbs | n/a | System layer (hold one, then the other) |

Option, Command, Space and Enter are the same on every layer.

### `TAB/HYP` (top-left key, on layers 0-2)

- **Tap** for Tab. **Hold** for Hyper (Ctrl+Alt+Cmd+Shift).
- Hold it and press another key to send a Hyper chord. skhd understands this as `hyper`, so `TAB/HYP` + a key triggers your Hyper bindings.
- Timing: `balanced` flavor, 200 ms tapping term, 150 ms quick-tap, `require-prior-idle-ms = 100`, so Tab resolves instantly while typing. A Hyper chord started within 100 ms of a non-modifier keypress comes out as Tab; pause briefly first.

### Control and Escape

- Control is the plain `CTRL` key on the left home row, so Ctrl chords (`Ctrl-a`, `Ctrl-d`, `Ctrl-c`) work from Base.
- Esc is the bottom-right key. Shift is the bottom-left key; there is no Right Shift.

### Nav/Num layer

- Numbers are on the top row (`1`-`5` left, `6`-`0` right).
- Arrows sit on the right home row (`LEFT DOWN UP RIGHT`, under `H J K L`).

### Symbols layer

- The left half is the shifted number row: `! @ # $ %`.
- The right half has `^ & * ( )` on top, `- = [ ] \ ``` on the home row, and `_ + { } | ~` below.
- `;`, `'`, `,`, `.` and `/` are on Base. `:`, `"`, `<`, `>` and `?` need Shift.

### System layer

| Key | Action |
|---|---|
| `BT1`-`BT5` | Select Bluetooth profile 1-5 |
| `BTCLR` | Clear the current Bluetooth bond |
| `USB` / `BLE` | Choose USB or Bluetooth output |
| `BOOT` | Enter the bootloader (for flashing) |
| `RGBTOG` `RGBMOD` `HUE±` `SAT±` `BRI±` | RGB underglow keys; they do nothing while RGB is off (see below) |

### Not on this layout

There is no Delete, Home, End, Page Up, Page Down, F1-F12 or media key, and no window-manager layer.

## Bluetooth and power settings

Set in [`config/corne.conf`](config/corne.conf):

| Setting | Value | Why |
|---|---|---|
| `BT_PERIPHERAL_PREF_MIN_INT` / `MAX_INT` | 12 / 24 (15-30 ms) | Fully Apple-compliant request; macOS grants 15 ms to HID devices. An 11.25 ms request can be rejected, which leaves the link at macOS's initial 30 ms |
| `BT_PERIPHERAL_PREF_LATENCY` | 30 | Power saving; does not delay key presses |
| `ZMK_SPLIT_BLE_PREF_INT` | 6 (7.5 ms) | Right-to-left half link; the host-link values above do not apply to it |
| `ZMK_DISPLAY_DEDICATED_THREAD_PRIORITY` | 10 | OLED rendering runs below the BLE send threads so a frame never holds up a key report |
| `BT_PERIPHERAL_PREF_TIMEOUT` | 600 (6 s) | Valid under Apple's 2-6 s and newer 6-18 s guidance |
| `BT_CTLR_TX_PWR_PLUS_8` | on | +8 dBm radio for split and host range |
| `ZMK_BLE_EXPERIMENTAL_CONN` | on | Disables 2M PHY for compatibility |
| `ZMK_IDLE_TIMEOUT` / `ZMK_IDLE_SLEEP_TIMEOUT` | 60 s / 15 min | Idle then deep sleep |
| RGB underglow | off | Experiment to rule out RGB as a lag source |

The final connection interval is chosen by macOS. Capture the connection with PacketLogger (Xcode Additional Tools) to see what it actually granted.

## Pairing and output

1. Hold one middle thumb, then the other, for the System layer.
2. Tap `BT1`-`BT5` to pick a profile, then pair from macOS Bluetooth settings.
3. `BTCLR` clears the current profile. `USB` / `BLE` pick the output.
4. `settings_reset` firmware wipes all bonds if pairing gets stuck.

## Build and flash

1. Push a branch that changes `config/**` (or run **Build ZMK firmware** manually in GitHub Actions).
2. Download the `firmware` artifact. It contains `corne_left`, `corne_right` and `settings_reset` `.uf2` files.
3. Put a half into bootloader mode (double-tap reset, or `BOOT` on the System layer, top-left) and copy the matching `.uf2` onto the `NICENANO` drive.
4. Flash both halves. If the Mac does not reconnect, remove the keyboard in Bluetooth settings and pair again.

Builds are defined in [`build.yaml`](build.yaml): `corne_left` (with the `studio-rpc-usb-uart` snippet for ZMK Studio over USB, lock off) and `corne_right`, both with the `nice_oled` display shield, plus a standalone `settings_reset`.

## Repository layout

```text
build.yaml            build matrix (boards, shields, snippets)
config/corne.keymap   all layers and the Tab/Hyper hold-tap
config/corne.conf     shared settings (Bluetooth, power, RGB, display)
config/boards/shields/corne/   per-half settings and shield overlays
config/west.yml       pinned ZMK and zmk-nice-oled revisions
```
