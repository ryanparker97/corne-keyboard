# Corne v4 ZMK Configuration

This layout is documented as an **NJ68-to-Corne transition layout**: it keeps familiar QWERTY typing, gives you dedicated top-left Escape and top-right Backspace keys, keeps Tab/number/navigation access on a predictable Lower layer, and places Space, Lower, and Enter on separate right-thumb keys so the smaller Corne feels less abrupt.

This repository is a ZMK user configuration for a Corne v4 split keyboard using nice!nano controllers. The build matrix uses ZMK main's hardware-model-v2 target `nice_nano/nrf52840/zmk`, whose upstream metadata defaults the nice!nano revision to `2.0.0`.

## What is included

- `config/corne.keymap` — macOS-oriented Corne QWERTY layout with four layers:
  - `DEF`: conventional 3x6+3 QWERTY base layer with easy top-left Esc, top-right Backspace, left-pinky Caps/Hyper, opposite-hand Space and Command thumbs, and separate Lower and Enter thumbs.
  - `LWR`: number, function, navigation, `TAB`, and Option layer.
  - `RSE`: symbol, paired punctuation (including Minus), Option, and Neovim-informed Ctrl-arrow resize chord layer.
  - `ADJ`: conditional Lower + Raise tri-layer with Bluetooth profile controls, built-in macOS productivity chords, bootloader, and reset.
- `config/corne.conf` — Corne runtime options for Bluetooth latency preferences, display, power management, disabled RGB/encoder, and current-ZMK-safe defaults.
- `build.yaml` — GitHub Actions build matrix for `nice_nano/nrf52840/zmk` + `corne_left` and `corne_right`.
- `config/west.yml` — ZMK manifest used by the GitHub Actions user-config build.

The shared `config/corne.conf` is applied to both split halves. It therefore avoids global USB or ZMK Studio enablement: the `corne_right` artifact is a peripheral and current ZMK rejects USB on non-central split halves. RGB is disabled with supported ZMK underglow configuration only; obsolete `WS2812_STRIP` overrides and user-forced deprecated KSCAN Kconfig settings are intentionally absent so warnings remain build failures instead of being suppressed.

## Layout notes

### NJ68 transition goals

Coming from an NJ68/68-key keyboard, the main goal is not to recreate every physical key. Instead, this layout keeps the habits that matter most during the transition:

- `ESC` stays easy at the top-left corner, and `BACKSPACE` is the top-right base key.
- QWERTY letters stay in normal positions.
- The right thumbs are three plain, separate controls: `SPACE`, momentary `LOWER`, and `ENTER`.
- Holding the right-middle `LOWER` thumb gives access to numbers, `TAB`, arrows, navigation, Delete, function keys, and a left-thumb `CTRL` for `CTRL+number` shortcuts.
- Symbols stay on `RAISE`, with paired punctuation grouped together; Minus is on Raise rather than the base layer.
- Caps remains a plain firmware key so the macOS Karabiner Hyper/Escape rule can keep working.

The keymap preserves the standard 3x6+3 Corne key positions. Command and Space are plain, dedicated opposite-hand thumb keys; Lower is a pure momentary layer key, and Enter is a separate key:

```text
Left:  LALT  RAISE  LGUI      Right: SPACE  LOWER  ENTER
Base corners: ESC (top-left)                    BACKSPACE (top-right)
```

`Caps Lock` is a plain, dedicated left home-row outer key for pinky access. On the active host, Karabiner-Elements maps `Caps Lock` to Hyper (`command+control+option+shift`) when held and `Escape` when tapped, so the verified host rule remains the single Hyper implementation.

Current displaced-key placement is explicit: Esc is on the top-left base key; Tab is on Lower; Caps is off the left thumb; `LEFT CTRL` is on the right bottom-row outer key; Backspace is on the top-row far-right base key; and Enter is the right-inner thumb.

Minus is available only on Raise. The prior right-side `RIGHT SHIFT` base key is absent while left Shift remains.

Holding the right-middle Lower thumb together with the left-middle Raise thumb activates `ADJ` through ZMK conditional layers. Bluetooth profile selection/clear, built-in macOS chords, bootloader, and system reset stay on `ADJ`.

### Built-in macOS productivity chords

The following `ADJ` actions are named by their **physical base-layer positions**, not by the keys emitted in the chord. ZMK `LG` is macOS Command, `LS` is Shift, and `LC` is Control.

| Physical base position on `ADJ` | Firmware chord | Action |
|---|---|---|
| `Y` | Command+Shift+3 | Full screenshot |
| `U` | Command+Shift+4 | Selected-area screenshot/snipping |
| `I` | Command+Shift+5 | Screenshot app |
| `O` | Command+Space | Spotlight |
| `P` | Command+Tab | Previous-app switch |
| Top-right `BACKSPACE` position | Control+Command+Q | Lock screen |
| `A` | Command+A | Select all |
| `S` | Command+S | Save |
| `F` | Command+F | Find |
| `Z` | Command+Z | Undo |
| `X` | Command+X | Cut |
| `C` | Command+C | Copy |
| `V` | Command+V | Paste |
| `B` | Command+Shift+Z | Redo |

These 14 chords are emitted directly by ZMK firmware and do not require Karabiner-Elements. See [`KEYMAP.md`](KEYMAP.md) for exact physical tables and raw bindings.

## macOS host dependencies

The Caps/Hyper, window-management, and editor workflows below depend on configuration outside this repository; they are distinct from the built-in `ADJ` productivity chords above. These host files were inspected but not changed:

- `/Users/ryanparker/.config/karabiner/karabiner.json` must keep the Caps Lock rule: Hyper when held, Escape when tapped.
- `/Users/ryanparker/.config/skhd/skhdrc` binds Hyper chords to yabai, including:
  - `Hyper+h/j/k/l` window focus.
  - `Hyper+z/f/b/r` zoom/balance/rotate.
  - `Hyper+1..5` named spaces and `Hyper+Left/Right` previous/next space.
  - `Hyper+m` and `Hyper+s` modal move/swap modes, followed by directions or space numbers.
- `/Users/ryanparker/.config/yabai/yabairc` configures BSP layout, gaps/padding, routing, and float rules used by those skhd commands.
- `/Users/ryanparker/Documents/personal/code/dotfiles/nvim` uses Space leader, `<C-h/j/k/l>` window navigation, and `<C-Up/Down/Left/Right>` window resizing.

Firmware choices remain conservative: the productivity actions are a small fixed set of direct macOS chords rather than application-specific macro sprawl. Hyper is produced only through the host's Caps rule, including when combined with Lower numbers/arrows by holding the right-middle Lower thumb; skhd/yabai consume those Hyper events. Neovim Ctrl-arrow resizing remains on Raise. None of those host-dependent behaviors should be conflated with the self-contained `ADJ` chords.

For the NJ68 transition, common typing and editing coverage is intentionally limited to the practical compact-keyboard baseline in `KEYMAP.md`: letters, digits, US punctuation pairs, easy top-left Escape, top-right Backspace, Lower Tab, Delete, Enter, Space, standard modifiers, arrows, Home/End, Page Up/Down, and F1-F12. Niche full-size keys such as Print Screen, Scroll Lock, Pause, Insert, numpad keys, and media keys are not mapped; screenshots are sent as macOS chords instead of a Print Screen keycode.

## Safety comparison and flashing guidance

Compared with the first repository version (`d9ba6f9`), the build/runtime safety assumptions, shields, workflow shape, and Bluetooth/power settings remain conservative. The current keymap intentionally changes transition ergonomics by placing Esc and Backspace at the top-left and top-right base corners, moving Tab to Lower, dedicating the right thumbs to Space, momentary Lower, and Enter, and keeping Minus on Raise. The build matrix now uses ZMK main's hardware-model-v2 nice!nano target instead of the legacy board identifier so it continues to configure against current upstream ZMK.

This configuration is a reasonable **go** for building/flashing only when the physical keyboard is actually a Corne v4 split using nice!nano v2-compatible controllers and standard ZMK `corne_left`/`corne_right` shields. It builds separate `corne_v4_left` and `corne_v4_right` artifacts using `nice_nano/nrf52840/zmk`, which upstream ZMK currently defines with default revision `2.0.0`, and keeps bootloader/reset access on the guarded `ADJ` tri-layer. Do **not** flash it if the PCB revision, controller, diode matrix, display/power wiring, or handedness differs from those assumptions; first confirm the exact hardware and use matching ZMK board/shield targets. This repository cannot verify physical soldering, battery polarity, charging safety, display wiring, radio performance, or successful flashing.

## Building

The included workflow first validates this repository and then uses ZMK's reusable user-config workflow:

1. Push this repository to GitHub or open a pull request.
2. Wait for **Build ZMK firmware** to run the `Validate keymap and build metadata` job.
3. After validation succeeds, the `Build Corne firmware` job builds the configured left and right Corne artifacts.
4. Download the generated `corne_v4_left` and `corne_v4_right` firmware artifacts.

The workflow grants the default `GITHUB_TOKEN` read-only repository contents access and checks out the exact event SHA with `git` instead of adding a separate checkout action reference. The firmware job still calls `zmkfirmware/zmk/.github/workflows/build-user-config.yml@main` because ZMK's user-config workflow is consumed as an upstream reusable workflow. That `@main` reference is intentionally documented as a floating upstream ref; this repository does not pin or verify a specific ZMK workflow commit.

### Dependency reproducibility status

No known-good ZMK commit or release tag has been verified in this repository yet. For that reason, `config/west.yml` and the reusable GitHub Actions workflow continue to track ZMK `main` instead of pretending to provide reproducible firmware inputs. To make builds reproducible later, first run and record a successful full firmware build for both `corne_left` and `corne_right`, then pin `config/west.yml` and the reusable workflow to that verified commit or tag. Until that evidence exists, do not replace `main` with an arbitrary commit.

Local builds require a ZMK/west workspace. If one is available, build with commands equivalent to:

```sh
west build -s zmk/app -b nice_nano/nrf52840/zmk -- -DSHIELD=corne_left
west build -s zmk/app -b nice_nano/nrf52840/zmk -- -DSHIELD=corne_right
```

## Flashing and post-flash checklist

Only flash artifacts that were built for the exact half being updated. The left and right halves are separate firmware images; flashing the wrong artifact can leave a half with incorrect handedness behavior.

Before flashing:

1. Confirm the PCB is a Corne v4 using nice!nano v2-compatible controllers and standard ZMK `corne_left`/`corne_right` shields.
2. Confirm which USB mass-storage volume corresponds to the left or right controller bootloader.
3. Back up any currently working firmware artifacts if rollback matters.
4. Disconnect batteries or follow the controller/keyboard vendor's safe flashing instructions if the hardware requires it.

After flashing each half:

1. Reboot both halves and test USB/BLE connection on the intended central side.
2. Verify top-left Escape, top-right Backspace, all six thumbs (especially separate right-middle Lower and right-inner Enter), Raise, and Lower+Raise `ADJ` activation before relying on the keyboard.
3. Verify all 14 `ADJ` productivity chords by their documented physical positions, especially that the guarded top-right position locks the screen; avoid unsaved work while testing editing shortcuts.
4. If Bluetooth pairing is stale, use `ADJ` + `BT clear`, then re-pair the host profile intentionally.
5. Confirm Caps behaves as Hyper/Escape only on hosts with the external Karabiner rule; on other hosts it remains plain Caps Lock. Confirm the `ADJ` firmware chords work independently of that rule.

This repository cannot validate physical hardware health, bootloader state, battery safety, or radio performance. No flashing was performed as part of repository validation.

## Host portability and Bluetooth rationale

The keymap is portable as a normal USB/BLE keyboard for ordinary keys. The 14 `ADJ` chords emit standard modifier/key events directly from firmware, although their documented actions follow macOS conventions. The Hyper workflow remains host dependent: without the Karabiner-Elements rule, the left pinky key sends plain `Caps Lock`; without skhd/yabai, Hyper shortcuts do nothing; without the Neovim mappings, the Ctrl-arrow chords are just normal Ctrl-arrow key events.

The BLE settings in `config/corne.conf` now target fast typing on macOS: the firmware avoids forced 2M PHY, advertises preferred connection parameters (`CONFIG_BT_PERIPHERAL_PREF_MIN_INT=9`, `CONFIG_BT_PERIPHERAL_PREF_MAX_INT=18`, and `CONFIG_BT_PERIPHERAL_PREF_LATENCY=0`), and increases the BLE keyboard report queue from ZMK's default `20` to `40` so quick bursts have more room before BLE notifications catch up. The connected host negotiates the final BLE interval and latency, so the `BT_PERIPHERAL_PREF` values are preferences rather than guarantees. Transmit power remains high for link margin, which can increase battery drain. Validate BLE changes with a real full firmware build and hardware test before documenting them as safe.

## Verification performed in this repository

Static checks can be run without a local ZMK checkout:

```sh
python3 scripts/validate.py

# Or run individual checks:
python3 scripts/check_keymap.py
python3 scripts/check_build_yaml.py
python3 scripts/check_config.py
python3 scripts/check_dependencies.py
```

These checks validate key binding counts for the four 42-key Corne layers; required plain Caps/Space/Command placement; exact base Backspace/Lower/Enter positions; exact `ADJ` macOS chord, Bluetooth, bootloader, and reset positions; Lower Ctrl+number and macOS/Neovim/ZMK control bindings; practical common-key coverage; the exact `nice_nano/nrf52840/zmk` Corne build matrix and matching README commands; absence of legacy nice!nano board targets; exact active supported Kconfig/BLE settings; no active forced BLE 2M PHY; and the documented dependency pinning status. They do not compile firmware, exercise a keyboard, or prove that macOS performs each documented action. Full firmware compilation still requires ZMK dependencies or the GitHub Actions workflow, and physical behavior requires hardware testing.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the lightweight GitHub Flow and required validation steps.
