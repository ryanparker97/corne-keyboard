# nice!oled status screens

Both Corne halves build with the maintained `mctechnology17/zmk-nice-oled`
`nice_oled` shield on the existing 128x32 SSD1306 displays. The manifest pins
ZMK v0.3.0 and nice!oled v0.0.2 by commit because that is the module's
documented tested ZMK release.

`CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y` selects the module screen and the
built-in ZMK status screen is explicitly disabled. The module's defaults enable
a central status view (layer, WPM/Bongo Cat, HID and modifier indicators) and a
peripheral status view with battery/output information and the Cat animation.
RGB underglow, the 27-LED chain, the keymap, and the left-half Studio snippet
are unchanged. RAW HID is not enabled.

Build the left and right matrix entries in `build.yaml`; each includes
`nice_oled` after its Corne shield. Flash each resulting firmware to its
matching half.

## Migration

ZMK v0.3.0 uses the `nice_nano_v2` board name. The previous main-branch
`nice_nano//zmk` matrix name is not valid on this pinned release, so all three
matrix entries use `nice_nano_v2`.

## ZMK limits

This is a ZMK status screen, not a QMK screen port. QMK-only raw matrix/keycode
visualization and host lock-LED behavior are not provided. The module's ZMK HID
indicator can show supported lock state (including Caps Lock), but no QMK host
LED interface or raw key-event display is configured.
