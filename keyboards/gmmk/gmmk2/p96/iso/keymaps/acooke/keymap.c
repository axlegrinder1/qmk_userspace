/* Copyright 2021 Glorious, LLC <salman@pcgamingrace.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include QMK_KEYBOARD_H

// Each layer gets a name for readability, which is then used in the keymap matrix below.
// The underscores don't mean anything - you can have a layer called STUFF or any other name.
#define _BL 0
#define _FL 1

// Lighting presets on Fn+1/2/3. Each keeps the current brightness and is saved.
enum custom_keycodes {
    LT_RED = QK_USER,
    LT_WHITE,
    LT_RAINBOW,
};

// Effect used by the rainbow preset
#define RAINBOW_EFFECT RGB_MATRIX_CYCLE_LEFT_RIGHT

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
  /* Keymap _BL: Base Layer (Default Layer)
   */
[_BL] = LAYOUT(
  KC_ESC,   KC_F1,    KC_F2,    KC_F3,    KC_F4,    KC_F5,    KC_F6,    KC_F7,    KC_F8,    KC_F9,    KC_F10,   KC_F11,   KC_F12,   KC_PSCR,  KC_DEL,   KC_INS,   KC_PGUP,  KC_PGDN,
  KC_GRV,   KC_1,     KC_2,     KC_3,     KC_4,     KC_5,     KC_6,     KC_7,     KC_8,     KC_9,     KC_0,     KC_MINS,  KC_EQL,   KC_BSPC,  KC_NUM,   KC_PSLS,  KC_PAST,  KC_PMNS,
  KC_TAB,   KC_Q,     KC_W,     KC_E,     KC_R,     KC_T,     KC_Y,     KC_U,     KC_I,     KC_O,     KC_P,     KC_LBRC,  KC_RBRC,  KC_ENT,   KC_P7,    KC_P8,    KC_P9,    KC_PPLS,
  KC_CAPS,  KC_A,     KC_S,     KC_D,     KC_F,     KC_G,     KC_H,     KC_J,     KC_K,     KC_L,     KC_SCLN,  KC_QUOT,  KC_NUHS,            KC_P4,    KC_P5,    KC_P6,
  KC_LSFT,  KC_NUBS,  KC_Z,     KC_X,     KC_C,     KC_V,     KC_B,     KC_N,     KC_M,     KC_COMM,  KC_DOT,   KC_SLSH,  KC_RSFT,  KC_UP,    KC_P1,    KC_P2,    KC_P3,    KC_PENT,
  KC_LCTL,  KC_LGUI,  KC_LALT,                      KC_SPC,                                 KC_RALT,  MO(_FL),  KC_RCTL,  KC_LEFT,  KC_DOWN,  KC_RGHT,  KC_P0,    KC_PDOT),

  /* Keymap _FL: Function Layer
   */
[_FL] = LAYOUT(
  RM_TOGG,  KC_MYCM,  KC_WHOM,  KC_CALC,  KC_MSEL,  KC_MPRV,  KC_MPLY,  KC_MNXT,  KC_MSTP,  KC_MUTE,  KC_VOLD,  KC_VOLU,  _______,   _______,  _______,  _______,  _______,  QK_BOOT,
  _______,  LT_RED,   LT_WHITE, LT_RAINBOW, _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,   _______,  _______,  _______,  _______,  _______,
  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,   _______,  _______,  _______,  _______,  _______,
  _______,  _______,  RM_HUEU,  RM_HUED,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,             _______,  _______,  _______,
  _______,  _______,  RM_SATU,  RM_SATD,  RM_SPDD,  RM_SPDU,  _______,  NK_TOGG,  _______,  _______,  _______,  _______,  _______,   RM_VALU,  _______,  _______,  _______,  _______,
  _______,  GU_TOGG,  _______,                      _______,                                _______,  _______,  _______,  RM_PREV,   RM_VALD,  RM_NEXT,  _______,  _______),
[2] = LAYOUT(
  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,   _______,  _______,  _______,  _______,  _______,
  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,   _______,  _______,  _______,  _______,  _______,
  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,   _______,  _______,  _______,  _______,  _______,
  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,             _______,  _______,  _______,
  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,  _______,   _______,  _______,  _______,  _______,  _______,
	_______,  _______,  _______,                      _______,                                _______,  _______,  _______, _______,   _______,  _______,  _______,  _______)
};

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    if (!record->event.pressed) return true;
    switch (keycode) {
        case LT_RED:
            rgb_matrix_enable();
            rgb_matrix_mode(RGB_MATRIX_SOLID_COLOR);
            rgb_matrix_sethsv(0, 255, rgb_matrix_get_val());
            return false;
        case LT_WHITE:
            rgb_matrix_enable();
            rgb_matrix_mode(RGB_MATRIX_SOLID_COLOR);
            rgb_matrix_sethsv(0, 0, rgb_matrix_get_val());
            return false;
        case LT_RAINBOW:
            rgb_matrix_enable();
            rgb_matrix_mode(RAINBOW_EFFECT);
            // Cycle effects use saturation, so undo the white preset's zero saturation
            rgb_matrix_sethsv(rgb_matrix_get_hue(), 255, rgb_matrix_get_val());
            return false;
    }
    return true;
}

// Overlay brightness never drops below this, so it stays readable when the effect is dimmed.
#define OVERLAY_MIN_VAL 96

// Colour for a key while a layer above the base is held. Keys that do nothing go dark,
// toggles show their state: green = on / working, red = off / blocked.
// Lighting keys are handled by the caller, which leaves the running effect on them.
static rgb_t overlay_color(uint16_t keycode, bool is_layer_key, uint8_t val) {
    hsv_t hsv;
    if (keycode == LT_RED) {
        hsv = (hsv_t){HSV_RED};
    } else if (keycode == LT_WHITE) {
        hsv = (hsv_t){HSV_WHITE};
    } else if (keycode == LT_RAINBOW) {
        hsv = (hsv_t){timer_read() / 8, 255, 255};
    } else if (IS_CONSUMER_KEYCODE(keycode) || IS_SYSTEM_KEYCODE(keycode)) {
        hsv = (hsv_t){HSV_CYAN};
    } else {
        switch (keycode) {
            case NK_TOGG:
                hsv = keymap_config.nkro ? (hsv_t){HSV_GREEN} : (hsv_t){HSV_RED};
                break;
            case GU_TOGG:
                // Blink red while the Windows key is locked
                if (keymap_config.no_gui && (timer_read() / 500) % 2) return (rgb_t){0, 0, 0};
                hsv = keymap_config.no_gui ? (hsv_t){HSV_RED} : (hsv_t){HSV_GREEN};
                break;
            case QK_BOOT:
                hsv = (hsv_t){HSV_MAGENTA};
                break;
            case KC_NO:
            case KC_TRNS:
                // The held Fn key falls through to the base layer; light it so it is easy to find
                if (!is_layer_key) return (rgb_t){0, 0, 0};
                hsv = (hsv_t){HSV_WHITE};
                break;
            default:
                hsv = (hsv_t){HSV_WHITE};
                break;
        }
    }
    hsv.v = val;
    return hsv_to_rgb(hsv);
}

bool rgb_matrix_indicators_advanced_user(uint8_t led_min, uint8_t led_max) {
    uint8_t layer = get_highest_layer(layer_state);
    // Nothing is drawn over the effect unless a layer above the base is held
    if (layer == _BL) return false;

    uint8_t val = MAX(rgb_matrix_get_val(), OVERLAY_MIN_VAL);
    for (uint8_t row = 0; row < MATRIX_ROWS; row++) {
        for (uint8_t col = 0; col < MATRIX_COLS; col++) {
            uint8_t index = g_led_config.matrix_co[row][col];
            if (index == NO_LED || index < led_min || index >= led_max) continue;

            keypos_t pos     = {.row = row, .col = col};
            uint16_t keycode = keymap_key_to_keycode(layer, pos);
            if (IS_RGB_MATRIX_KEYCODE(keycode)) {
                // Leave the running effect on lighting keys so changes show while Fn is held
                continue;
            }
            rgb_t rgb = overlay_color(keycode, IS_QK_MOMENTARY(keymap_key_to_keycode(_BL, pos)), val);
            rgb_matrix_set_color(index, rgb.r, rgb.g, rgb.b);
        }
    }
    return false;
}
