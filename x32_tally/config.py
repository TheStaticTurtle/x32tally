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

x32_address = "192.168.150.196"

mqtt = {
    "server": "127.0.0.1",
    "port": 1883
}

input_channels = {
    1: {"set_tally": ws1812b_set_fn(0, 6), "is_on_stand": gpio_read_fn(board.D23)},
    2: {"set_tally": ws1812b_set_fn(1, 6), "is_on_stand": gpio_read_fn(board.D23)},
    3: {"set_tally": ws1812b_set_fn(2, 6), "is_on_stand": gpio_read_fn(board.D23)},
    4: {"set_tally": ws1812b_set_fn(3, 6), "is_on_stand": gpio_read_fn(board.D23)},
    5: {"set_tally": ws1812b_set_fn(4, 6), "is_on_stand": gpio_read_fn(board.D23)},
    6: {"set_tally": ws1812b_set_fn(5, 6), "is_on_stand": gpio_read_fn(board.D23)},
    7: {"set_tally": ws1812b_set_fn(6, 6), "is_on_stand": gpio_read_fn(board.D23)},
    8: {"set_tally": ws1812b_set_fn(7, 6), "is_on_stand": gpio_read_fn(board.D23)},
    9: {"set_tally": ws1812b_set_fn(8, 6), "is_on_stand": gpio_read_fn(board.D23)},
    10: {"set_tally": ws1812b_set_fn(9, 6), "is_on_stand": gpio_read_fn(board.D23)},
    11: {"set_tally": ws1812b_set_fn(10, 6), "is_on_stand": gpio_read_fn(board.D23)},
    12: {"set_tally": ws1812b_set_fn(11, 6), "is_on_stand": gpio_read_fn(board.D23)},
    13: {"set_tally": ws1812b_set_fn(12, 6), "is_on_stand": gpio_read_fn(board.D23)},
    14: {"set_tally": ws1812b_set_fn(13, 6), "is_on_stand": gpio_read_fn(board.D23)},
    15: {"set_tally": ws1812b_set_fn(14, 6), "is_on_stand": gpio_read_fn(board.D23)},
    16: {"set_tally": ws1812b_set_fn(15, 6), "is_on_stand": gpio_read_fn(board.D23)},
    17: {"set_tally": ws1812b_set_fn(16, 6)},
    18: {"set_tally": ws1812b_set_fn(17, 6)},
    19: {"set_tally": ws1812b_set_fn(18, 6)},
    20: {"set_tally": ws1812b_set_fn(19, 6)},
    21: {"set_tally": ws1812b_set_fn(20, 6)},
    22: {"set_tally": ws1812b_set_fn(21, 6)},
    23: {"set_tally": ws1812b_set_fn(22, 6)},
    24: {"set_tally": ws1812b_set_fn(23, 6)},
    25: {"set_tally": ws1812b_set_fn(24, 6)},
    26: {"set_tally": ws1812b_set_fn(25, 6)},
    27: {"set_tally": ws1812b_set_fn(26, 6)},
    28: {"set_tally": ws1812b_set_fn(27, 6)},
    29: {"set_tally": ws1812b_set_fn(28, 6)},
    30: {"set_tally": ws1812b_set_fn(29, 6)},
    31: {"set_tally": ws1812b_set_fn(30, 6)},
    32: {"set_tally": ws1812b_set_fn(31, 6)},
}
