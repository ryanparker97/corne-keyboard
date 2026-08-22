
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
