#include <stdio.h>

#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

#include <lvgl.h>

#include <zmk/display.h>
#include <zmk/display/status_screen.h>
#include <zmk/event_manager.h>

LOG_MODULE_DECLARE(zmk, CONFIG_ZMK_LOG_LEVEL);

static sys_slist_t widgets = SYS_SLIST_STATIC_INIT(&widgets);

struct corne_oled_status_screen {
    sys_snode_t node;
    lv_obj_t *layer_label;
    lv_obj_t *bt_label;
    lv_obj_t *name_label;
};

static struct corne_oled_status_screen status_widget;

static void set_label_text(lv_obj_t *label, const char *text) {
    if (label != NULL) {
        lv_label_set_text(label, text);
    }
}

static void set_name_status(struct corne_oled_status_screen *widget) {
    char text[32] = {};

    snprintf(text, sizeof(text), "Name: %s", CONFIG_BT_DEVICE_NAME);
    set_label_text(widget->name_label, text);
}

#if !IS_ENABLED(CONFIG_ZMK_SPLIT) || IS_ENABLED(CONFIG_ZMK_SPLIT_ROLE_CENTRAL)

#include <zmk/ble.h>
#include <zmk/events/ble_active_profile_changed.h>
#include <zmk/events/layer_state_changed.h>
#include <zmk/keymap.h>

struct corne_layer_state {
    zmk_keymap_layer_index_t index;
    const char *label;
};

struct corne_bt_state {
    int active_profile_index;
    bool active_profile_connected;
    bool active_profile_bonded;
};

static struct corne_layer_state layer_status_get_state(const zmk_event_t *_eh) {
    zmk_keymap_layer_index_t index = zmk_keymap_highest_layer_active();
    zmk_keymap_layer_id_t id = zmk_keymap_layer_index_to_id(index);

    return (struct corne_layer_state){.index = index, .label = zmk_keymap_layer_name(id)};
}

static void set_layer_status(struct corne_layer_state state) {
    char text[32] = {};
    const char *label = state.label;

    if (label == NULL || label[0] == '\0') {
        snprintf(text, sizeof(text), "Layer: %u", state.index);
    } else {
        snprintf(text, sizeof(text), "Layer: %s", label);
    }

    struct corne_oled_status_screen *widget;
    SYS_SLIST_FOR_EACH_CONTAINER(&widgets, widget, node) {
        set_label_text(widget->layer_label, text);
    }
}

ZMK_DISPLAY_WIDGET_LISTENER(corne_oled_layer_status, struct corne_layer_state, set_layer_status,
                            layer_status_get_state)
ZMK_SUBSCRIPTION(corne_oled_layer_status, zmk_layer_state_changed);

static struct corne_bt_state bt_status_get_state(const zmk_event_t *_eh) {
    return (struct corne_bt_state){
        .active_profile_index = zmk_ble_active_profile_index(),
        .active_profile_connected = zmk_ble_active_profile_is_connected(),
        .active_profile_bonded = !zmk_ble_active_profile_is_open(),
    };
}

static void set_bt_status(struct corne_bt_state state) {
    char text[32] = {};
    int profile = state.active_profile_index + 1;

    if (!state.active_profile_bonded) {
        snprintf(text, sizeof(text), "BT%d: pairing", profile);
    } else if (state.active_profile_connected) {
        snprintf(text, sizeof(text), "BT%d: connected", profile);
    } else {
        snprintf(text, sizeof(text), "BT%d: disconnected", profile);
    }

    struct corne_oled_status_screen *widget;
    SYS_SLIST_FOR_EACH_CONTAINER(&widgets, widget, node) { set_label_text(widget->bt_label, text); }
}

ZMK_DISPLAY_WIDGET_LISTENER(corne_oled_bt_status, struct corne_bt_state, set_bt_status,
                            bt_status_get_state)
ZMK_SUBSCRIPTION(corne_oled_bt_status, zmk_ble_active_profile_changed);

static void init_dynamic_status(void) {
    corne_oled_layer_status_init();
    corne_oled_bt_status_init();
}

#else

#include <zmk/events/split_peripheral_status_changed.h>
#include <zmk/split/bluetooth/peripheral.h>

struct corne_peripheral_bt_state {
    bool connected;
    bool bonded;
};

static struct corne_peripheral_bt_state peripheral_bt_status_get_state(const zmk_event_t *_eh) {
    return (struct corne_peripheral_bt_state){
        .connected = zmk_split_bt_peripheral_is_connected(),
        .bonded = zmk_split_bt_peripheral_is_bonded(),
    };
}

static void set_peripheral_bt_status(struct corne_peripheral_bt_state state) {
    const char *text = state.connected ? "Split BT: connected"
                       : state.bonded   ? "Split BT: waiting"
                                      : "Split BT: pairing";

    struct corne_oled_status_screen *widget;
    SYS_SLIST_FOR_EACH_CONTAINER(&widgets, widget, node) { set_label_text(widget->bt_label, text); }
}

ZMK_DISPLAY_WIDGET_LISTENER(corne_oled_peripheral_bt_status, struct corne_peripheral_bt_state,
                            set_peripheral_bt_status, peripheral_bt_status_get_state)
ZMK_SUBSCRIPTION(corne_oled_peripheral_bt_status, zmk_split_peripheral_status_changed);

static void init_dynamic_status(void) {
    set_label_text(status_widget.layer_label, "Layer: central only");
    corne_oled_peripheral_bt_status_init();
}

#endif

static lv_obj_t *create_status_label(lv_obj_t *parent) {
    lv_obj_t *label = lv_label_create(parent);
    lv_obj_set_style_text_font(label, lv_theme_get_font_small(parent), LV_PART_MAIN);
    return label;
}

lv_obj_t *zmk_display_status_screen(void) {
    lv_obj_t *screen = lv_obj_create(NULL);
    lv_obj_set_style_border_width(screen, 0, LV_PART_MAIN);
    lv_obj_set_style_pad_all(screen, 0, LV_PART_MAIN);

    status_widget.name_label = create_status_label(screen);
    lv_obj_align(status_widget.name_label, LV_ALIGN_TOP_LEFT, 0, 0);

    status_widget.bt_label = create_status_label(screen);
    lv_obj_align(status_widget.bt_label, LV_ALIGN_LEFT_MID, 0, 0);

    status_widget.layer_label = create_status_label(screen);
    lv_obj_align(status_widget.layer_label, LV_ALIGN_BOTTOM_LEFT, 0, 0);

    sys_slist_append(&widgets, &status_widget.node);

    set_name_status(&status_widget);
    init_dynamic_status();

    return screen;
}
