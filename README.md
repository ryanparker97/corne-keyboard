# Corne v3.1 ZMK user config

Wireless-first 42-key Corne v3.1 configuration for nice!nano/nRF52840 using ZMK, `nice_nano/nrf52840/zmk`, `corne_left nice_oled`, and `corne_right nice_oled`, with safe wired USB support only on the left/central firmware.

## Included files

- `build.yaml` builds normal `corne_v3_1_left` and `corne_v3_1_right` artifacts, plus optional `corne_v3_1_left_studio` and `settings_reset` artifacts.
- `config/west.yml` pins ZMK and `mctechnology17/zmk-nice-oled`.
- `config/corne.keymap` contains four 42-binding layers: `DEF`, `LWR`, `RSE`, and `ADJ`, including output-selection controls on `ADJ`.
- `config/corne.conf` enables BLE, nice_oled, wireless power management, and conservative RGB without enabling USB globally.
- `zephyr/module.yml` exposes this repo as a Zephyr module/board root.
- `.github/workflows/build.yml` validates the repo and runs the ZMK user-config build.

## Thumb layout

ZMK Corne binding order is the 36 finger keys followed by the left thumbs outer-to-inner, then the right thumbs inner-to-outer. Every layer uses the same physical thumb row:

```text
Left thumbs, outer -> inner:  LALT  RAISE  SPACE
Right thumbs, inner -> outer: RGUI  LOWER  ENTER
```

`SPACE` is therefore on the inner-left thumb. `RGUI` is macOS Command on the inner-right thumb.

## RGB LEDs

RGB is enabled conservatively for wireless use:

- `CONFIG_ZMK_RGB_UNDERGLOW=y`
- off on start: `CONFIG_ZMK_RGB_UNDERGLOW_ON_START=n`
- low brightness: `CONFIG_ZMK_RGB_UNDERGLOW_BRT_START=15`, capped by `CONFIG_ZMK_RGB_UNDERGLOW_BRT_MAX=40`
- idle auto-off: `CONFIG_ZMK_RGB_UNDERGLOW_AUTO_OFF_IDLE=y`
- USB auto-off is intentionally not enabled in shared `config/corne.conf` because it depends on `USB_DEVICE_STACK` and may fail for the right split peripheral.

The pinned/upstream ZMK Corne `nice_nano` overlay defines the `led_strip` node. This keymap only overrides `&led_strip { chain-length = <27>; };` for a fully LED-populated Corne v3.1: 42 per-key SK6812 plus 12 underglow WS2812, or 27 LEDs per half. Change this to `<6>` if only the underglow LEDs are soldered.

RGB controls are on `ADJ`: hold `LOWER` + `RAISE`, then use physical `H/J/K/L/;/’` for effect, toggle, on, off, hue up, and saturation up.

## Wired and wireless output

The shared config keeps BLE enabled and keeps USB out of `config/corne.conf` so the right half remains a normal split peripheral. The `build.yaml` matrix adds wired USB and USB boot support only to the left/central artifacts.

- For wired use, plug USB into the left half. The right half still talks to the left half over split BLE.
- For wireless use, pair over BLE as usual; the left half remains the central side.
- ZMK's default output prefers USB when both USB and BLE are available.
- Output controls are on `ADJ`: hold `LOWER` + `RAISE`, then use physical `N/M/,` for `&out OUT_USB`, `&out OUT_BLE`, and `&out OUT_TOG`.

## Build targets

`build.yaml` uses ZMK's hardware-model-v2 board target `nice_nano/nrf52840/zmk`:

- `corne_left nice_oled` + `CONFIG_ZMK_USB` + `CONFIG_ZMK_USB_BOOT` -> `corne_v3_1_left`
- `corne_right nice_oled` -> `corne_v3_1_right`
- `corne_left nice_oled` + `studio-rpc-usb-uart` + `CONFIG_ZMK_STUDIO` + `CONFIG_ZMK_USB` + `CONFIG_ZMK_USB_BOOT` -> `corne_v3_1_left_studio`
- `settings_reset` -> `settings_reset`

USB and Studio are only for the left/central half. The right peripheral keeps
the normal firmware and does not enable USB or ZMK Studio.

Local build commands, from a west workspace with this repository as the user config:

```sh
west build -s zmk/app -d build/corne_left -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_left nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD" -DCONFIG_ZMK_USB=y -DCONFIG_ZMK_USB_BOOT=y
west build -s zmk/app -d build/corne_right -b nice_nano/nrf52840/zmk -- -DSHIELD="corne_right nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
west build -s zmk/app -d build/corne_left_studio -b nice_nano/nrf52840/zmk -S studio-rpc-usb-uart -- -DSHIELD="corne_left nice_oled" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD" -DCONFIG_ZMK_STUDIO=y -DCONFIG_ZMK_USB=y -DCONFIG_ZMK_USB_BOOT=y
west build -s zmk/app -d build/settings_reset -b nice_nano/nrf52840/zmk -- -DSHIELD="settings_reset" -DZMK_CONFIG="$PWD/config" -DZMK_EXTRA_MODULES="$PWD"
```

## Flashing notes

1. Build or download both normal artifacts: `corne_v3_1_left` and `corne_v3_1_right`.
2. Put one nice!nano into bootloader mode.
3. Copy the matching `.uf2` to that half's mounted bootloader volume.
4. Repeat with the other half; do not swap left/right firmware.
5. If Bluetooth pairing is stale, use `ADJ` + `BT_CLR`, then pair again, or flash `settings_reset` once before reflashing the normal firmware.

Use `corne_v3_1_left_studio` only when you want ZMK Studio support on the
left/central half; keep `corne_v3_1_right` on the right half.

When using a cable for typing, connect it to the left half. Connecting the right
half over USB is only for flashing or charging; it remains the split peripheral
in normal operation.

Only flash this on a standard Corne v3.1 42-key split with nice!nano-compatible controllers, matching OLED wiring, and matching LED population/chain length.

## Dependency reproducibility status

`config/west.yml` and the reusable GitHub Actions workflow are pinned to ZMK `6e2ef41e022d555b10f116e395832913f71717b3`. The OLED module `mctechnology17/zmk-nice-oled` is pinned to `46f824abb2bd41f1287c5c68abd14122af6042a3` and supplied through the `nice_oled` shield. These pins are chosen for reproducibility and alignment between local west workspaces and CI.

Local static validation passes with `python3 scripts/validate.py`. A full firmware compilation was not run in this environment because `west` is unavailable here; confirm the pinned build through GitHub Actions or a local ZMK/west workspace before flashing.

## Validation

Static checks:

```sh
python3 scripts/validate.py
```

Full firmware compilation still requires GitHub Actions or a local ZMK/west workspace; it was not run in this environment because `west` is unavailable here.
