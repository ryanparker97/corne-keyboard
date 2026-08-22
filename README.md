# Corne v4 ZMK user config for Windows

Native-wireless 42-key Corne v4 configuration for nice!nano/nRF52840 using ZMK, `nice_nano/nrf52840/zmk`, `corne_left nice_oled`, and `corne_right nice_oled`. The current shared config keeps encoder support off, applies low-latency Bluetooth preferences, disables RGB underglow, enables display support, and keeps sleep/external-power settings.

The pinned upstream ZMK revision exposes the generic Corne shields rather than a separate `corne_v4` shield, so this config intentionally keeps `corne_left`/`corne_right` and documents Corne v4 as the target hardware.

## Included files

- `build.yaml` builds normal wireless `corne_v4_left` and `corne_v4_right` artifacts, plus `settings_reset`.
- `config/west.yml` pins ZMK and the LVGL9-compatible `chyuuu/zmk-nice-oled` fork.
- `config/corne.keymap` contains four 42-binding layers: `DEF`, `LWR`, `RSE`, and `ADJ`, following the Windows NJ68 transition model.
- `config/corne.conf` turns encoders off, sets low-latency Bluetooth/controller preferences, disables RGB underglow, enables display support, and configures sleep/external power.
- `zephyr/module.yml` marks this repository as a Zephyr module/board root; full display behavior still needs confirmation in a ZMK/west build.
- `.github/workflows/build.yml` validates the repo and runs the ZMK user-config build.

## NJ68 transition layout

This layout keeps compact-keyboard muscle memory on a Corne: base corner `ESC`/`BACKSPACE`, `TAB` on `LOWER`, numbers and navigation on `LOWER`, symbols on `RAISE`, and utilities on `ADJ`.

ZMK Corne binding order is the 36 finger keys followed by the left thumbs outer-to-inner, then the right thumbs inner-to-outer. The default layer uses:

```text
Left thumbs, outer -> inner:  LALT  RAISE  LWIN
Right thumbs, inner -> outer: SPACE  LOWER  ENTER
```

Raw default thumb bindings are `&kp LALT  &mo RSE  &kp LWIN    &kp SPACE  &mo LWR  &kp RET`.

On `LWR`, the left outer thumb becomes `LCTRL` and the remaining thumbs are transparent so `LOWER` + left outer thumb + number gives Ctrl+number. `RSE` and `ADJ` use transparent thumbs.

## RGB LEDs

RGB underglow/per-key LED support is disabled because the selected Corne v4 target has unknown per-half LED count and pinout.

- `config/corne.conf` has no active `CONFIG_ZMK_RGB_UNDERGLOW*` settings.
- `config/corne.keymap` does not bind `&rgb_ug` controls.
- `config/corne.keymap` does not add an `&led_strip` chain-length override.

Do not enable RGB or add a chain-length override until the exact Corne v4 LED hardware is confirmed.

## Windows utilities, editing, and media controls

`ADJ` is activated by holding `LOWER` + `RAISE` together.

Top-right Windows utility keys on `ADJ`:

```text
Y: Print Screen   U: Win+Shift+S   I: Win+V   O: Win+S   P: Win+Tab   Backspace: Win+L
```

Left-side editing chords on `ADJ`:

```text
A: Ctrl+A   S: Ctrl+S   F: Ctrl+F   Z: Ctrl+Z   X: Ctrl+X   C: Ctrl+C   V: Ctrl+V   B: Ctrl+Y
```

Right home-row media keys on `ADJ`:

```text
H: Previous   J: Play/Pause   K: Next   L: Mute   ;: Volume Down   ': Volume Up
```

Bluetooth select/clear controls remain on the left side of `ADJ`. Bootloader and reset remain on the lower-right side of `ADJ` for maintenance.

## Wireless and USB notes

The current shared config applies Bluetooth latency/controller preferences but does not override every nice!nano board default. In particular, USB HID endpoint behavior follows the compiled ZMK board defaults unless a future config change explicitly overrides it.

- Pair the left/central half with Windows using the Bluetooth profile controls on `ADJ`.
- Active Bluetooth preferences include `CONFIG_BT_CTLR_PHY_2M=y` and `CONFIG_BT_GATT_ENFORCE_SUBSCRIPTION=n`.
- No normal artifact enables ZMK Studio, a Studio snippet, or USB boot mode.
- A USB cable may still be used for power, charging, bootloader flashing, and any USB behavior provided by the compiled defaults.

## OLED

The `nice_oled` shield is included in the left and right build targets for SSD1306 display hardware, and `config/corne.conf` enables ZMK display support plus a dedicated display work queue. This repository does not currently force a custom OLED status screen or override the nice_oled widget set in shared config, so final display content should be confirmed with a full ZMK/west build.

## Build targets

`build.yaml` uses ZMK's hardware-model-v2 board target `nice_nano/nrf52840/zmk`:

- `corne_left nice_oled` -> `corne_v4_left`
- `corne_right nice_oled` -> `corne_v4_right`
- `settings_reset` -> `settings_reset`

Local build commands, from a west workspace with this repository as the user config:

```sh
west build -s zmk/app -d build/corne_left -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_left nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
west build -s zmk/app -d build/corne_right -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_right nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
west build -s zmk/app -d build/settings_reset -b nice_nano/nrf52840/zmk -- -DSHIELD="settings_reset" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
```

## Flashing notes

1. Build or download both normal artifacts: `corne_v4_left` and `corne_v4_right`.
2. Put one nice!nano into bootloader mode.
3. Copy the matching `.uf2` to that half's mounted bootloader volume over USB.
4. Repeat with the other half; do not swap left/right firmware.
5. If Bluetooth pairing is stale, use `ADJ` + `BT_CLR`, then pair again, or flash `settings_reset` once before reflashing the normal firmware.

Connecting either half over USB can be used for power, charging, bootloader flashing, and any USB behavior provided by the compiled defaults.

Only flash this on a Corne v4 42-key split with nice!nano-compatible controllers and matching 128x32 OLED wiring. Corne v4 physical matrix/OLED compatibility and LED wiring cannot be proven by these static checks or without a full firmware build and hardware confirmation.

## Dependency reproducibility status

`config/west.yml` and the reusable GitHub Actions workflow are pinned to ZMK `6e2ef41e022d555b10f116e395832913f71717b3`. The OLED module uses the LVGL9-compatible `chyuuu/zmk-nice-oled` fork pinned to `b2d5cd914b2180cb53766b0302c75818400d2f58` and supplied through the `nice_oled` shield. This fork revision updates the image descriptors for the pinned ZMK/LVGL 9 stack. These pins are chosen for reproducibility and alignment between local west workspaces and CI.

Local static validation passes with `python3 scripts/validate.py`. A full firmware compilation was not run in this environment because `west` is unavailable here; confirm the pinned build through GitHub Actions or a local ZMK/west workspace before flashing.

## Validation

Static checks:

```sh
python3 scripts/validate.py
git diff --check
```

Full firmware compilation still requires GitHub Actions or a local ZMK/west workspace; it was not run in this environment because `west` is unavailable here.
