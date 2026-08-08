# Corne v4 ZMK Configuration

This repository is a ZMK user configuration for a Corne v4 split keyboard using nice!nano controllers. The build matrix uses ZMK main's hardware-model-v2 target `nice_nano/nrf52840/zmk`, whose upstream metadata defaults the nice!nano revision to `2.0.0`.

## What is included

- `config/corne.keymap` — macOS-oriented Corne QWERTY layout with four layers:
  - `DEF`: conventional 3x6+3 QWERTY base layer with left-pinky Caps/Hyper, opposite-hand Space and Command thumbs, Control, Shift, and Option access.
  - `LWR`: number, function, navigation, reachable `ESC`, and Option layer.
  - `RSE`: symbol, paired punctuation, Option, and Neovim-informed Ctrl-arrow resize chord layer.
  - `ADJ`: tri-layer reached by holding Lower + Raise, with Bluetooth profile controls, Mac modifiers, caps lock, bootloader, and reset.
- `config/corne.conf` — Corne runtime options for Bluetooth latency preferences, display, power management, disabled RGB/encoder, and current-ZMK-safe defaults.
- `build.yaml` — GitHub Actions build matrix for `nice_nano/nrf52840/zmk` + `corne_left` and `corne_right`.
- `config/west.yml` — ZMK manifest used by the GitHub Actions user-config build.

The shared `config/corne.conf` is applied to both split halves. It therefore avoids global USB or ZMK Studio enablement: the `corne_right` artifact is a peripheral and current ZMK rejects USB on non-central split halves. RGB is disabled with supported ZMK underglow configuration only; obsolete `WS2812_STRIP` overrides and user-forced deprecated KSCAN Kconfig settings are intentionally absent so warnings remain build failures instead of being suppressed.

## Layout notes

The keymap preserves the standard 3x6+3 Corne key positions. Command and Space are plain, dedicated opposite-hand thumb keys:

```text
Left:  LALT  RAISE  LGUI      Right: SPACE LOWER  ENTER
```

`Caps Lock` is a plain, dedicated left home-row outer key for pinky access. On the active host, Karabiner-Elements maps `Caps Lock` to Hyper (`command+control+option+shift`) when held and `Escape` when tapped, so the verified host rule remains the single Hyper implementation.

Displaced keys: Caps moved off the left thumb; `LEFT CTRL` moved to the right bottom-row outer key; the prior right-side `RIGHT SHIFT` base key was removed while left Shift remains.

Holding both `RAISE` and `LOWER` activates the `ADJ` layer through ZMK conditional layers. Bluetooth profile selection/clear, bootloader, and system reset stay on `ADJ`.

## macOS host dependencies

The macOS workflow depends on configuration outside this repository; those files were inspected but not changed:

- `/Users/ryanparker/.config/karabiner/karabiner.json` must keep the Caps Lock rule: Hyper when held, Escape when tapped.
- `/Users/ryanparker/.config/skhd/skhdrc` binds Hyper chords to yabai, including:
  - `Hyper+h/j/k/l` window focus.
  - `Hyper+z/f/b/r` zoom/balance/rotate.
  - `Hyper+1..5` named spaces and `Hyper+Left/Right` previous/next space.
  - `Hyper+m` and `Hyper+s` modal move/swap modes, followed by directions or space numbers.
- `/Users/ryanparker/.config/yabai/yabairc` configures BSP layout, gaps/padding, routing, and float rules used by those skhd commands.
- `/Users/ryanparker/Documents/personal/code/dotfiles/nvim` uses Space leader, `<C-h/j/k/l>` window navigation, and `<C-Up/Down/Left/Right>` window resizing.

Firmware choices are deliberately conservative: no application macro sprawl was added. Hyper is produced by holding the pinky Caps key with normal keys, Lower numbers, or Lower arrows; Neovim Ctrl-arrow resizing remains on Raise.

Common typing and editing coverage is intentionally limited to the practical compact-keyboard baseline in `KEYMAP.md`: letters, digits, US punctuation pairs, Escape, Tab, Backspace, Delete, Enter, Space, standard modifiers, arrows, Home/End, Page Up/Down, and F1-F12. Niche full-size keys such as Print Screen, Scroll Lock, Pause, Insert, numpad keys, and media keys are not mapped.

## Safety comparison and flashing guidance

Compared with the first repository version (`d9ba6f9`), the keymap, runtime configuration, shields, workflow shape, Bluetooth/power settings, and key ergonomics remain unchanged. The build matrix now uses ZMK main's hardware-model-v2 nice!nano target instead of the legacy board identifier so it continues to configure against current upstream ZMK.

This configuration is a reasonable **go** for building/flashing only when the physical keyboard is actually a Corne v4 split using nice!nano v2-compatible controllers and standard ZMK `corne_left`/`corne_right` shields. It builds separate `corne_v4_left` and `corne_v4_right` artifacts using `nice_nano/nrf52840/zmk`, which upstream ZMK currently defines with default revision `2.0.0`, and keeps bootloader/reset access on the guarded `ADJ` tri-layer. Do **not** flash it if the PCB revision, controller, diode matrix, display/power wiring, or handedness differs from those assumptions; first confirm the exact hardware and use matching ZMK board/shield targets. This repository cannot verify physical soldering, battery polarity, charging safety, display wiring, radio performance, or successful flashing.

## Building

The included workflow first validates this repository and then uses ZMK's reusable user-config workflow:

1. Push this repository to GitHub or open a pull request.
2. Wait for **Build ZMK firmware** to run the `Validate keymap and build metadata` job.
3. After validation succeeds, the `Build Corne firmware` job builds the configured left and right Corne artifacts.
4. Download the generated `corne_v4_left` and `corne_v4_right` firmware artifacts.

The workflow grants the default `GITHUB_TOKEN` read-only repository contents access and checks out the exact event SHA with `git` instead of adding a separate checkout action reference. The firmware job still calls `zmkfirmware/zmk/.github/workflows/build-user-config.yml@main` because ZMK's user-config workflow is consumed as an upstream reusable workflow. That `@main` reference is intentionally documented as a floating upstream ref; this repository does not pin or verify a specific ZMK workflow commit.

Local builds require a ZMK/west workspace. If one is available, build with commands equivalent to:

```sh
west build -s zmk/app -b nice_nano/nrf52840/zmk -- -DSHIELD=corne_left
west build -s zmk/app -b nice_nano/nrf52840/zmk -- -DSHIELD=corne_right
```

## Verification performed in this repository

Static checks can be run without a local ZMK checkout:

```sh
python3 scripts/check_keymap.py
python3 scripts/check_build_yaml.py
python3 scripts/check_config.py
```

These checks validate key binding counts for the four 42-key Corne layers, required plain Caps/Space/Command placement, macOS/Neovim/ZMK control bindings, the exact `nice_nano/nrf52840/zmk` Corne build matrix, matching README build commands, absence of legacy nice!nano board targets, and absence of unsupported Kconfig cleanup regressions (`WS2812_STRIP`, user-forced deprecated KSCAN settings, global USB/Studio, or warning suppression). Full firmware compilation still requires ZMK dependencies or the GitHub Actions workflow.
