# Corne keyboard (ZMK)

ZMK firmware configuration for a 42-key Corne (nice!nano v2, split, Bluetooth + USB), tuned for macOS data engineering and DevOps work: shell, Python, SQL, YAML/JSON, Terraform, Docker, Kubernetes, Vim, tmux, and a yabai/skhd tiling window manager.

- Keymap: [`config/corne.keymap`](config/corne.keymap)
- Settings: [`config/corne.conf`](config/corne.conf)
- Design rationale: [`docs/keymap.md`](docs/keymap.md)
- Firmware is built by GitHub Actions (ZMK v0.3.0, pinned in `config/west.yml` and the workflow).

## Layout at a glance

Five layers. Every layer has 42 keys; `.` means "falls through to the layer below".

### Base (layer 0)

```text
 ESC      Q    W    E    R    T   |   Y    U    I    O    P    BSPC
 TAB/HYP  A    S    D    F    G   |   H    J    K    L    ;    '
 SHIFT    Z    X    C    V    B   |   N    M    ,    .    /    CTRL
                OPT  RAISE  CMD   |   SPACE  LOWER  RET/WM
```

### Lower (layer 1, hold LOWER): numbers, arrows, F-keys

```text
 ESC      1    2    3    4    5   |   6     7     8    9      0     BSPC
 TAB/HYP  CTRL OPT  CMD  SHFT TMUX|   LEFT  DOWN  UP   RIGHT  PGDN  PGUP
 F1       F2   F3   F4   F5   F6  |   F7    F8    F9   F10    F11   F12
                CTRL RAISE  CMD   |   SPACE LOWER  RET
```

### Raise (layer 2, hold RAISE): symbols

```text
 ESC      !    @    #    $    %   |   ^    &    *    :     |    BSPC
 TAB/HYP  CTRL OPT  CMD  SHFT =   |   [    (    )    {     }    ]
 \        -    "    _    +    `   |   <    >    HOME END   ?    ~
                CTRL RAISE  CMD   |   SPACE LOWER  RET
```

### Adjust (layer 3, hold LOWER + RAISE): system

```text
 ESC      BT1  BT2  BT3  BT4  BT5 |   CAP   CWORD CAPS  SPOT  APP   LOCK
 TAB/HYP  PREV PLAY NEXT MUTE VOL-|   MC    EXPO  DT<   DT>   AREA  FQUIT
 RESET    DISP- DISP+ USB  BLE VOL+|   BTCLR FULL  WIN   HIDE  MIN   BOOT
                CTRL RAISE  CMD   |   SPACE LOWER  RET
```

### WM (layer 4, hold RET/WM): window manager

Every key sends `Hyper+<key>` (Ctrl+Alt+Cmd+Shift).

```text
 TAB      .    .    E    R    T   |   1    2    3    4    5    .
 .        A    S    D    F    .   |   H    J    K    L    .    .
 .        Z    X    .    V    B   |   .    M    .    .    .    .
                .    .    .       |   RET  .    (held)
```

## How to use it

### Thumb keys

| Key | Tap | Hold |
|---|---|---|
| `OPT` / `CMD` | Option / Command | same |
| `RAISE` | n/a | Raise layer (symbols) |
| `LOWER` | n/a | Lower layer (numbers, arrows, F-keys) |
| `SPACE` | Space | n/a |
| `RET/WM` | Enter | WM layer |
| `LOWER + RAISE` held together | n/a | Adjust layer |

### `TAB/HYP` (left outer home key, on every layer)

- **Tap** for Tab. **Hold** for Hyper (Ctrl+Alt+Cmd+Shift).
- Hold it and press another key to send a hyper chord. skhd understands this as `hyper`.
- The WM layer sends the same chord, so `TAB/HYP` + `H/J/K/L` drives skhd too, without the thumb.
- Timing: `balanced` flavor, 200 ms tapping term, `require-prior-idle-ms = 100`, so Tab resolves instantly while typing.

### Esc and Control

- `Esc` is the top-left key on Base, Lower, Raise and Adjust.
- Right Control is the bottom-right key on Base. Left-hand Control, Option, Command and Shift are plain held keys on the Lower and Raise home rows.

### Lower layer

- Arrows sit on the physical `H J K L` keys (`LEFT DOWN UP RIGHT`), with `PGDN` / `PGUP` after them.
- `LOWER + Option + Left/Right`: move by word.
- `LOWER + Command + Left/Right`: line start / end.
- Add `LOWER + Shift` to extend a selection.
- `TMUX` sends the `Ctrl-A` prefix and releases Control, so the next arrow moves between panes.

### Raise layer

- Brackets are paired on the right home row: `[ ( ) { } ]`.
- `:` and `|` sit above the parentheses. `~` is bottom-right, `-` is under the left middle finger.
- `BSPC`, `TAB` (the `TAB/HYP` key), `HOME` and `END` are available without leaving the layer.

### Adjust layer

| Key | Action |
|---|---|
| `BT1`–`BT5` | Select Bluetooth profile 1–5 |
| `BTCLR` | Clear the current Bluetooth bond |
| `USB` / `BLE` | Choose USB or Bluetooth output |
| `BOOT` | Enter the bootloader (for flashing) |
| `RESET` | Reset the keyboard |
| `PREV` `PLAY` `NEXT` `MUTE` `VOL-` `VOL+` | Media keys |
| `DISP-` `DISP+` | Brightness down / up |
| `CAP` | Shift-Cmd-5 (screenshot / recording UI) |
| `CWORD` | Caps Word (auto-stops on word break) |
| `CAPS` | Caps Lock |
| `SPOT` / `APP` / `LOCK` | Spotlight / app switcher / lock screen |
| `MC` / `EXPO` | Mission Control / App Exposé (Ctrl-Up / Ctrl-Down) |
| `DT<` / `DT>` | Desktop left / right (Ctrl-Left / Ctrl-Right) |
| `AREA` / `FULL` | Shift-Cmd-4 / Shift-Cmd-3 screenshots |
| `FQUIT` | Force Quit (Cmd-Opt-Esc) |
| `WIN` / `HIDE` / `MIN` | Next window of app (Cmd-\`) / hide / minimize |

### WM layer (window manager)

Hold the right outer thumb (`RET/WM`) and tap a key. This drives `skhd/skhdrc` in the dotfiles repo, so yabai and skhd must be running.

| Do this | Press |
|---|---|
| Focus window left / down / up / right | `H` / `J` / `K` / `L` |
| Jump to Space 1–5 (chat, terminal, web, notes, default) | `1` … `5` |
| Focus most recent window | `TAB` |
| New Alacritty window | the Space position (`RET`) |
| Zoom / fullscreen | `Z` / `F` |
| Float window | `T` |
| Balance / rotate 90° | `B` / `R` |
| Toggle split / mirror | `X` / `V` |
| Stack layout / bsp layout | `A` / `D` |

Modes need two steps. Enter with the layer, **release it**, then tap bare keys:

1. **Move:** WM + `M`, release, then `H/J/K/L` (warp) or `1`–`5` (to a Space). Exits after one action.
2. **Swap:** WM + `S`, release, then `H/J/K/L`. Exits after one action.
3. **Resize:** WM + `E`, release, then tap `H/J/K/L` repeatedly. Press `Esc` to leave.

Notes:
- A quick tap on `RET/WM` still sends Enter, and it fires on release.
- Space focus and move-to-Space may need the yabai scripting addition on your macOS version.

## Bluetooth and power settings

Set in [`config/corne.conf`](config/corne.conf):

| Setting | Value | Why |
|---|---|---|
| `BT_PERIPHERAL_PREF_MIN_INT` / `MAX_INT` | 9 / 21 (11.25–26.25 ms) | Apple-compliant range, avoids the pinned 15 ms case that some devices scale to 30 ms |
| `BT_PERIPHERAL_PREF_LATENCY` | 30 | Power saving; does not delay key presses |
| `BT_PERIPHERAL_PREF_TIMEOUT` | 600 (6 s) | Valid under Apple's 2–6 s and newer 6–18 s guidance |
| `BT_CTLR_TX_PWR_PLUS_8` | on | +8 dBm radio for split and host range |
| `ZMK_BLE_EXPERIMENTAL_CONN` | on | Disables 2M PHY for compatibility |
| `ZMK_IDLE_TIMEOUT` / `ZMK_IDLE_SLEEP_TIMEOUT` | 60 s / 15 min | Idle then deep sleep |
| RGB underglow | off | Experiment to rule out RGB as a lag source |

The final connection interval is chosen by macOS. Capture the connection with PacketLogger (Xcode Additional Tools) to see what it actually granted.

## Pairing and output

1. Hold `LOWER + RAISE` for the Adjust layer.
2. Tap `BT1`–`BT5` to pick a profile, then pair from macOS Bluetooth settings.
3. `BTCLR` clears the current profile. `USB` / `BLE` pick the output.
4. `settings_reset` firmware wipes all bonds if pairing gets stuck.

## Build and flash

1. Push a branch that changes `config/**` (or run **Build ZMK firmware** manually in GitHub Actions).
2. Download the `firmware` artifact. It contains `corne_left`, `corne_right` and `settings_reset` `.uf2` files.
3. Put a half into bootloader mode (double-tap reset, or `BOOT` on the Adjust layer, bottom-right) and copy the matching `.uf2` onto the `NICENANO` drive.
4. Flash both halves. If the Mac does not reconnect, remove the keyboard in Bluetooth settings and pair again.

Builds are defined in [`build.yaml`](build.yaml): `corne_left` (with the `studio-rpc-usb-uart` snippet for ZMK Studio over USB, lock off) and `corne_right`, both with the `nice_oled` display shield, plus a standalone `settings_reset`.

## Repository layout

```text
build.yaml            build matrix (boards, shields, snippets)
config/corne.keymap   all layers, hold-taps, macros
config/corne.conf     shared settings (Bluetooth, power, RGB, display)
config/boards/shields/corne/   per-half settings and shield overlays
config/west.yml       pinned ZMK and zmk-nice-oled revisions
docs/keymap.md        layer descriptions and design rationale
```
