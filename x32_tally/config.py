import logging
import board

x32_address = "192.168.150.100"

mqtt = {
    "host": "127.0.0.1",
    "port": 1883
}

log_levels = {
    "stand_detector": logging.INFO,
    "osc": logging.INFO,
    "tally_lights": logging.INFO,
}

tally_colors = {
    "muted": (25, 0, 0),
    "muted_not_in_stand": (75, 0, 0),
    "active": (0, 25, 0),
    "active_in_stand": (0, 255, 0),
}

tally_neopixel_pin = board.D18

input_channels = {
    1:  {"tally_leds": [0,  1,   2,  3,  4,  5], "on_stand_button": board.D23},
    2:  {"tally_leds": [6,  7,   8,  9, 10, 11], "on_stand_button": board.D24},
    3:  {"tally_leds": [12, 13, 14, 15, 16, 17], "on_stand_button": board.D25},
    4:  {"tally_leds": [18, 19, 20, 21, 22, 23], "on_stand_button": board.D8},
    5:  {"tally_leds": [24, 25, 26, 27, 28, 29], "on_stand_button": board.D7},
    6:  {"tally_leds": [30, 31, 32, 33, 34, 35], "on_stand_button": board.D1},
    7:  {"tally_leds": [36, 37, 38, 39, 40, 41], "on_stand_button": board.D12},
    8:  {"tally_leds": [42, 43, 44, 45, 46, 47], "on_stand_button": board.D16},
    9:  {"tally_leds": [48, 49, 50, 51, 52, 53], "on_stand_button": board.D20},
    10: {"tally_leds": [54, 55, 56, 57, 58, 59], "on_stand_button": board.D21},
    11: {"tally_leds": [60, 61, 62, 63, 64, 65], "on_stand_button": board.D26},
    12: {"tally_leds": [66, 67, 68, 69, 70, 71], "on_stand_button": board.D19},
    13: {"tally_leds": [72, 73, 74, 75, 76, 77], "on_stand_button": board.D13},
    14: {"tally_leds": [78, 79, 80, 81, 82, 83], "on_stand_button": board.D6},
    15: {"tally_leds": [84, 85, 86, 87, 88, 89], "on_stand_button": board.D5},
    16: {"tally_leds": [90, 91, 92, 93, 94, 95], "on_stand_button": board.D0},
    17: {},
    18: {},
    19: {},
    20: {},
    21: {},
    22: {},
    23: {},
    24: {},
    25: {},
    26: {},
    27: {},
    28: {},
    29: {},
    30: {},
    31: {},
    32: {},
}
