import logging

import board
import neopixel
import digitalio


class LedController:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, 6 * 16, auto_write=False)

    def update(self):
        self.pixels.show()

    def set(self, leds, r, g, b):
        for led in leds:
            self.pixels[led] = (r, g, b)


class InputController:
    def __init__(self):
        self.buttons = {}

    def get(self, pin):
        if pin.id not in self.buttons:
            self.buttons[pin.id] = digitalio.DigitalInOut(pin)
            self.buttons[pin.id].direction = digitalio.Direction.INPUT
        return self.buttons[pin.id].value


x32_address = "192.168.150.189"

tally_colors = {
    "muted": (25, 0, 0),
    "muted_not_in_stand": (75, 0, 0),
    "active": (0, 25, 0),
    "active_in_stand": (0, 255, 0),
}

mqtt = {
    "host": "127.0.0.1",
    "port": 1883
}

log_levels = {
    "stand_detector": logging.INFO,
    "osc": logging.INFO,
    "tally_lights": logging.INFO,
}

input_channels = {
    1:  {"set_tally": [0, 1, 2, 3, 4, 5],       "is_on_stand": board.D23},
    2:  {"set_tally": [6, 7, 8, 9, 10, 11],     "is_on_stand": board.D24},
    3:  {"set_tally": [12, 13, 14, 15, 16, 17], "is_on_stand": board.D25},
    4:  {"set_tally": [18, 19, 20, 21, 22, 23], "is_on_stand": board.D8},
    5:  {"set_tally": [24, 25, 26, 27, 28, 29], "is_on_stand": board.D7},
    6:  {"set_tally": [30, 31, 32, 33, 34, 35], "is_on_stand": board.D1},
    7:  {"set_tally": [36, 37, 38, 39, 40, 41], "is_on_stand": board.D12},
    8:  {"set_tally": [42, 43, 44, 45, 46, 47], "is_on_stand": board.D16},
    9:  {"set_tally": [48, 49, 50, 51, 52, 53], "is_on_stand": board.D20},
    10: {"set_tally": [54, 55, 56, 57, 58, 59], "is_on_stand": board.D21},
    11: {"set_tally": [60, 61, 62, 63, 64, 65], "is_on_stand": board.D26},
    12: {"set_tally": [66, 67, 68, 69, 70, 71], "is_on_stand": board.D19},
    13: {"set_tally": [72, 73, 74, 75, 76, 77], "is_on_stand": board.D13},
    14: {"set_tally": [78, 79, 80, 81, 82, 83], "is_on_stand": board.D6},
    15: {"set_tally": [84, 85, 86, 87, 88, 89], "is_on_stand": board.D5},
    16: {"set_tally": [90, 91, 92, 93, 94, 95], "is_on_stand": board.D0},
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
