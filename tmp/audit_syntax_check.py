#!/usr/bin/env python3
from pathlib import Path
import subprocess, shutil, os, textwrap
root = Path('tmp/audit_stubs')
if root.exists():
    shutil.rmtree(root)
for d in ['zephyr/kernel.h','zephyr/logging/log.h','zmk/display.h','zmk/display/status_screen.h','zmk/event_manager.h','zmk/ble.h','zmk/events/ble_active_profile_changed.h','zmk/events/layer_state_changed.h','zmk/keymap.h','zmk/events/split_peripheral_status_changed.h','zmk/split/bluetooth/peripheral.h']:
    (root / Path(d).parent).mkdir(parents=True, exist_ok=True)
(root/'zephyr/kernel.h').write_text(r'''
#pragma once
#include <stdbool.h>
#include <stdint.h>
#define K_FOREVER 0
#define SYS_SLIST_STATIC_INIT(x) {0}
typedef struct sys_snode { struct sys_snode *next; } sys_snode_t;
typedef struct { sys_snode_t *head; } sys_slist_t;
static inline void sys_slist_append(sys_slist_t *l, sys_snode_t *n) {}
#define SYS_SLIST_FOR_EACH_CONTAINER(list, var, member) for ((var)=0; (var)!=0; )
#define IS_ENABLED(x) x
''')
(root/'zephyr/logging/log.h').write_text('#pragma once\n#define LOG_MODULE_DECLARE(...)\n')
(root/'lvgl.h').write_text(r'''
#pragma once
typedef struct lv_obj_t lv_obj_t;
#define LV_PART_MAIN 0
#define LV_ALIGN_TOP_LEFT 0
#define LV_ALIGN_LEFT_MID 1
#define LV_ALIGN_BOTTOM_LEFT 2
static inline void lv_label_set_text(lv_obj_t *o, const char *t) {}
static inline lv_obj_t *lv_label_create(lv_obj_t *p) { return (lv_obj_t*)1; }
static inline void lv_obj_set_style_text_font(lv_obj_t *o, const void *f, int part) {}
static inline const void *lv_theme_get_font_small(lv_obj_t *o) { return 0; }
static inline lv_obj_t *lv_obj_create(lv_obj_t *p) { return (lv_obj_t*)1; }
static inline void lv_obj_set_style_border_width(lv_obj_t *o, int w, int part) {}
static inline void lv_obj_set_style_pad_all(lv_obj_t *o, int p, int part) {}
static inline void lv_obj_align(lv_obj_t *o, int align, int x, int y) {}
''')
(root/'zmk/display.h').write_text(r'''
#pragma once
#define ZMK_DISPLAY_WIDGET_LISTENER(listener, state_type, cb, state_func) static void listener##_init(void) { cb(state_func(0)); }
''')
(root/'zmk/display/status_screen.h').write_text('#pragma once\n#include <lvgl.h>\nlv_obj_t *zmk_display_status_screen(void);\n')
(root/'zmk/event_manager.h').write_text('#pragma once\ntypedef void zmk_event_t;\n#define ZMK_SUBSCRIPTION(a,b)\n')
(root/'zmk/ble.h').write_text('#pragma once\n#include <stdbool.h>\nstatic inline int zmk_ble_active_profile_index(void){return 0;}\nstatic inline bool zmk_ble_active_profile_is_connected(void){return false;}\nstatic inline bool zmk_ble_active_profile_is_open(void){return true;}\n')
for p in ['zmk/events/ble_active_profile_changed.h','zmk/events/layer_state_changed.h','zmk/events/split_peripheral_status_changed.h']:
    (root/p).write_text('#pragma once\n')
(root/'zmk/keymap.h').write_text('#pragma once\n#include <stdint.h>\ntypedef uint8_t zmk_keymap_layer_index_t; typedef uint8_t zmk_keymap_layer_id_t;\nstatic inline zmk_keymap_layer_index_t zmk_keymap_highest_layer_active(void){return 0;}\nstatic inline zmk_keymap_layer_id_t zmk_keymap_layer_index_to_id(zmk_keymap_layer_index_t i){return i;}\nstatic inline const char *zmk_keymap_layer_name(zmk_keymap_layer_id_t i){return "DEF";}\n')
(root/'zmk/split/bluetooth/peripheral.h').write_text('#pragma once\n#include <stdbool.h>\nstatic inline bool zmk_split_bt_peripheral_is_connected(void){return true;}\nstatic inline bool zmk_split_bt_peripheral_is_bonded(void){return true;}\n')
cmds = [
    ['gcc','-fsyntax-only','-std=c11','-I'+str(root),'-DCONFIG_ZMK_LOG_LEVEL=0','-DCONFIG_BT_DEVICE_NAME="Corne"','-DCONFIG_ZMK_SPLIT=1','-DCONFIG_ZMK_SPLIT_ROLE_CENTRAL=1','src/display/corne_oled_status_screen.c'],
    ['gcc','-fsyntax-only','-std=c11','-I'+str(root),'-DCONFIG_ZMK_LOG_LEVEL=0','-DCONFIG_BT_DEVICE_NAME="Corne"','-DCONFIG_ZMK_SPLIT=1','-DCONFIG_ZMK_SPLIT_ROLE_CENTRAL=0','src/display/corne_oled_status_screen.c'],
]
for cmd in cmds:
    print('RUN', ' '.join(cmd))
    subprocess.run(cmd, check=True)
print('stub syntax checks passed')
