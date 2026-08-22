
#pragma once
#define ZMK_DISPLAY_WIDGET_LISTENER(listener, state_type, cb, state_func) static void listener##_init(void) { cb(state_func(0)); }
