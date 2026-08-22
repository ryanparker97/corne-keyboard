#pragma once
#include <stdint.h>
typedef uint8_t zmk_keymap_layer_index_t; typedef uint8_t zmk_keymap_layer_id_t;
static inline zmk_keymap_layer_index_t zmk_keymap_highest_layer_active(void){return 0;}
static inline zmk_keymap_layer_id_t zmk_keymap_layer_index_to_id(zmk_keymap_layer_index_t i){return i;}
static inline const char *zmk_keymap_layer_name(zmk_keymap_layer_id_t i){return "DEF";}
