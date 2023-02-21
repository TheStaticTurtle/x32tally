import json
import logging
import board

# Main config file
# this file is imported in every module

# Address of the X32/M32 console
x32_address = "192.168.150.100"

# Address of the MQTT server. if mosquito is installed locally use 127.0.0.1:1883
mqtt = {
    "host": "127.0.0.1",
    "port": 1883
}

# Log level used by each module
log_levels = {
    "stand_buttons": logging.INFO,
    "osc": logging.INFO,
    "tally_lights": logging.INFO,
}

# Colors for the tally lights
tally_colors = {
    "muted": (30, 0, 0),
    "muted_not_in_stand_on": (10, 2, 0),
    "muted_not_in_stand_off": (10, 2, 0),
    "active": (0, 25, 0),
    "active_in_stand_on": (0, 255, 0),
    "active_in_stand_off": (0, 25, 0),
}

# Pin used for the neopixel output
tally_neopixel_pin = board.D18

# List of input channels from 1 to 32.
#   enabled: Enabled or not the channel it will completely disable the channel
#   tally_leds: List of the leds for this channel
#   on_stand_button: Pin of the stand buttons
input_channels = {
    1:  {"enabled": True,  "tally_leds": [0,  1,   2,  3,  4,  5], "on_stand_button": board.D23},
    2:  {"enabled": True,  "tally_leds": [6,  7,   8,  9, 10, 11], "on_stand_button": board.D24},
    3:  {"enabled": True,  "tally_leds": [12, 13, 14, 15, 16, 17], "on_stand_button": board.D25},
    4:  {"enabled": True,  "tally_leds": [18, 19, 20, 21, 22, 23], "on_stand_button": board.D8},
    5:  {"enabled": True,  "tally_leds": [24, 25, 26, 27, 28, 29], "on_stand_button": board.D7},
    6:  {"enabled": True,  "tally_leds": [30, 31, 32, 33, 34, 35], "on_stand_button": board.D1},
    7:  {"enabled": True,  "tally_leds": [36, 37, 38, 39, 40, 41], "on_stand_button": board.D12},
    8:  {"enabled": True,  "tally_leds": [42, 43, 44, 45, 46, 47], "on_stand_button": board.D16},
    9:  {"enabled": True,  "tally_leds": [48, 49, 50, 51, 52, 53], "on_stand_button": board.D20},
    10: {"enabled": True,  "tally_leds": [54, 55, 56, 57, 58, 59], "on_stand_button": board.D21},
    11: {"enabled": True,  "tally_leds": [60, 61, 62, 63, 64, 65], "on_stand_button": board.D26},
    12: {"enabled": True,  "tally_leds": [66, 67, 68, 69, 70, 71], "on_stand_button": board.D19},
    13: {"enabled": True,  "tally_leds": [72, 73, 74, 75, 76, 77], "on_stand_button": board.D13},
    14: {"enabled": True,  "tally_leds": [78, 79, 80, 81, 82, 83], "on_stand_button": board.D6},
    15: {"enabled": True,  "tally_leds": [84, 85, 86, 87, 88, 89], "on_stand_button": board.D5},
    16: {"enabled": False, "tally_leds": [90, 91, 92, 93, 94, 95], "on_stand_button": board.D0},
    17: {"enabled": False},
    18: {"enabled": False},
    19: {"enabled": False},
    20: {"enabled": False},
    21: {"enabled": False},
    22: {"enabled": False},
    23: {"enabled": False},
    24: {"enabled": False},
    25: {"enabled": False},
    26: {"enabled": False},
    27: {"enabled": False},
    28: {"enabled": False},
    29: {"enabled": False},
    30: {"enabled": False},
    31: {"enabled": False},
    32: {"enabled": False},
}