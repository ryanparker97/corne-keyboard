#!/usr/bin/env bash
set -euo pipefail

print_url_lines() {
  local label="$1" url="$2" start="$3" end="$4"
  python3 - "$label" "$url" "$start" "$end" <<'PY'
import sys, urllib.request
label,url,start,end=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
print(f"===== {label} {url} lines {start}-{end} =====")
text=urllib.request.urlopen(url, timeout=30).read().decode('utf-8', 'replace').splitlines()
for i in range(start, min(end, len(text))+1):
    print(f"{i:04d}: {text[i-1]}")
print()
PY
}

LVGL_REV=f1db87ee98f1810328a8419572fa42a3b5f352ae
NICE_REV=46f824abb2bd41f1287c5c68abd14122af6042a3

print_url_lines "lvgl_v9_lv_image_header" "https://raw.githubusercontent.com/zmkfirmware/lvgl/${LVGL_REV}/src/draw/lv_image_dsc.h" 24 130
print_url_lines "lvgl_v9_image_color_format_enum" "https://raw.githubusercontent.com/zmkfirmware/lvgl/${LVGL_REV}/src/misc/lv_color.h" 220 310
print_url_lines "lvgl_v9_image_api_aliases" "https://raw.githubusercontent.com/zmkfirmware/lvgl/${LVGL_REV}/src/lvgl.h" 1 140
print_url_lines "zmk_nice_oled_modifiers_struct_examples" "https://raw.githubusercontent.com/mctechnology17/zmk-nice-oled/${NICE_REV}/boards/shields/nice_oled/assets/modifiers_sym.c" 20 70
print_url_lines "zmk_nice_oled_images_struct_examples" "https://raw.githubusercontent.com/mctechnology17/zmk-nice-oled/${NICE_REV}/boards/shields/nice_oled/assets/images.c" 1 120
print_url_lines "zmk_nice_oled_assets_include_declarations" "https://raw.githubusercontent.com/mctechnology17/zmk-nice-oled/${NICE_REV}/boards/shields/nice_oled/assets/images.h" 1 120
