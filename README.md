# Corne v4 ZMK user config for Windows

Wireless-first 42-key Corne v4 configuration for nice!nano/nRF52840 using ZMK, `nice_nano/nrf52840/zmk`, `corne_left nice_oled`, and `corne_right nice_oled`, with safe wired USB support only on the left/central firmware.

The pinned upstream ZMK revision exposes the generic Corne shields rather than a separate `corne_v4` shield, so this config intentionally keeps `corne_left`/`corne_right` and documents Corne v4 as the target hardware.

## Included files

- `build.yaml` builds normal `corne_v4_left` and `corne_v4_right` artifacts, plus optional `corne_v4_left_studio` and `settings_reset` artifacts.
- `config/west.yml` pins ZMK and the LVGL9-compatible `chyuuu/zmk-nice-oled` fork.
- `config/corne.keymap` contains four 42-binding layers: `DEF`, `LWR`, `RSE`, and `ADJ`, including Windows utility, media, and output-selection controls on `ADJ`.
- `config/corne.conf` enables BLE, nice_oled, Windows-oriented BLE preferences, wireless power management, and no active RGB underglow settings.
- `zephyr/module.yml` exposes this repo as a Zephyr module/board root.
- `.github/workflows/build.yml` validates the repo and runs the ZMK user-config build.

## Thumb layout

ZMK Corne binding order is the 36 finger keys followed by the left thumbs outer-to-inner, then the right thumbs inner-to-outer. Every layer uses the same physical thumb row:

```text
Left thumbs, outer -> inner:  LALT  RAISE  SPACE
Right thumbs, inner -> outer: RWIN  LOWER  ENTER
```

`SPACE` is therefore on the inner-left thumb. `RWIN` is the Windows key on the inner-right thumb.

## RGB LEDs

RGB underglow/per-key LED support is disabled because the selected Corne v4 target has unknown per-half LED count and pinout.

- `config/corne.conf` has no active `CONFIG_ZMK_RGB_UNDERGLOW*` settings.
- `config/corne.keymap` does not bind `&rgb_ug` controls.
- `config/corne.keymap` does not add an `&led_strip` chain-length override.

Do not enable RGB or add a chain-length override until the exact Corne v4 LED hardware is confirmed.

## Windows utilities and media controls

`ADJ` is activated by holding `LOWER` + `RAISE` together.

Top-right Windows utility keys on `ADJ`:

```text
Y: Print Screen   U: Win+Shift+S   I: Win+V   O: Win+S   P: Win+Tab   Backspace: Win+L
```

Right home-row media keys on `ADJ`:

```text
H: Previous   J: Play/Pause   K: Next   L: Mute   ;: Volume Down   ': Volume Up
```

Bluetooth select/clear controls remain on the left side of `ADJ`.

## Wired and wireless output

The shared config keeps BLE enabled and keeps USB out of `config/corne.conf` so the right half remains a normal split peripheral. The `build.yaml` matrix adds wired USB and USB boot support only to the left/central artifacts.

- For wired use, plug USB into the left half. The right half still talks to the left half over split BLE.
- For wireless use, pair over BLE as usual; the left half remains the central side.
- Windows BLE compatibility preferences include `CONFIG_BT_CTLR_PHY_2M=n` and `CONFIG_BT_GATT_ENFORCE_SUBSCRIPTION=n`.
- ZMK's default output prefers USB when both USB and BLE are available.
- Output controls are on `ADJ`: hold `LOWER` + `RAISE`, then use physical `N/M/,` for `&out OUT_USB`, `&out OUT_BLE`, and `&out OUT_TOG`.

## OLED

The `nice_oled` shield is enabled on both halves. Windows modifier symbols are selected with `CONFIG_NICE_OLED_WIDGET_MODIFIERS_INDICATORS_FIXED_SYMBOL_WINDOWS=y`.

## Build targets

`build.yaml` uses ZMK's hardware-model-v2 board target `nice_nano/nrf52840/zmk`:

- `corne_left nice_oled` + `CONFIG_ZMK_USB` + `CONFIG_ZMK_USB_BOOT` -> `corne_v4_left`
- `corne_right nice_oled` -> `corne_v4_right`
- `corne_left nice_oled` + `studio-rpc-usb-uart` + `CONFIG_ZMK_STUDIO` + `CONFIG_ZMK_USB` + `CONFIG_ZMK_USB_BOOT` -> `corne_v4_left_studio`
- `settings_reset` -> `settings_reset`

USB and Studio are only for the left/central half. The right peripheral keeps the normal firmware and does not enable USB or ZMK Studio.

Local build commands, from a west workspace with this repository as the user config:

```sh
west build -s zmk/app -d build/corne_left -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_left nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD" -DCONFIG_ZMK_USB=y -DCONFIG_ZMK_USB_BOOT=y
west build -s zmk/app -d build/corne_right -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_right nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
west build -s zmk/app -d build/corne_left_studio -b nice_nano/nrf52840/zmk -S studio-rpc-usb-uart -- -DSHIELD="corne_left nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD" -DCONFIG_ZMK_STUDIO=y -DCONFIG_ZMK_USB=y -DCONFIG_ZMK_USB_BOOT=y
west build -s zmk/app -d build/settings_reset -b nice_nano/nrf52840/zmk -- -DSHIELD="settings_reset" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
```

## Flashing notes

1. Build or download both normal artifacts: `corne_v4_left` and `corne_v4_right`.
2. Put one nice!nano into bootloader mode.
3. Copy the matching `.uf2` to that half's mounted bootloader volume.
4. Repeat with the other half; do not swap left/right firmware.
5. If Bluetooth pairing is stale, use `ADJ` + `BT_CLR`, then pair again, or flash `settings_reset` once before reflashing the normal firmware.

Use `corne_v4_left_studio` only when you want ZMK Studio support on the left/central half; keep `corne_v4_right` on the right half.

When using a cable for typing, connect it to the left half. Connecting the right half over USB is only for flashing or charging; it remains the split peripheral in normal operation.

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
