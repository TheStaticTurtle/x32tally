import logging

import board
import neopixel
import digitalio


pixels = neopixel.NeoPixel(board.D18, 6 * 16, auto_write=False)

def update_leds():
    pixels.show()

def ws1812b_set_fn(start_i, count):
    leds = list(range(start_i * count, (start_i+1) * count))

    def write(r, g, b):
        for led in leds:
            pixels[led] = (r, g, b)
    return write


def gpio_read_fn(pin):
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT

    def read():
        return getattr(button, "value")
    return read


x32_address = "192.168.150.189"

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
    1: {"set_tally": ws1812b_set_fn(0, 6), "is_on_stand": gpio_read_fn(board.D23)},
    2: {"set_tally": ws1812b_set_fn(1, 6), "is_on_stand": gpio_read_fn(board.D24)},
    3: {"set_tally": ws1812b_set_fn(2, 6), "is_on_stand": gpio_read_fn(board.D25)},
    4: {"set_tally": ws1812b_set_fn(3, 6), "is_on_stand": gpio_read_fn(board.D8)},
    5: {"set_tally": ws1812b_set_fn(4, 6), "is_on_stand": gpio_read_fn(board.D7)},
    6: {"set_tally": ws1812b_set_fn(5, 6), "is_on_stand": gpio_read_fn(board.D1)},
    7: {"set_tally": ws1812b_set_fn(6, 6), "is_on_stand": gpio_read_fn(board.D12)},
    8: {"set_tally": ws1812b_set_fn(7, 6), "is_on_stand": gpio_read_fn(board.D16)},
    9: {"set_tally": ws1812b_set_fn(8, 6), "is_on_stand": gpio_read_fn(board.D20)},
    10: {"set_tally": ws1812b_set_fn(9, 6), "is_on_stand": gpio_read_fn(board.D21)},
    11: {"set_tally": ws1812b_set_fn(10, 6), "is_on_stand": gpio_read_fn(board.D26)},
    12: {"set_tally": ws1812b_set_fn(11, 6), "is_on_stand": gpio_read_fn(board.D19)},
    13: {"set_tally": ws1812b_set_fn(12, 6), "is_on_stand": gpio_read_fn(board.D13)},
    14: {"set_tally": ws1812b_set_fn(13, 6), "is_on_stand": gpio_read_fn(board.D6)},
    15: {"set_tally": ws1812b_set_fn(14, 6), "is_on_stand": gpio_read_fn(board.D5)},
    16: {"set_tally": ws1812b_set_fn(15, 6), "is_on_stand": gpio_read_fn(board.D0)},
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
