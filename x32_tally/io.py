import neopixel
import digitalio
from . import config


class LedController:
    def __init__(self):
        highest_pixel_id = 0
        for ch_n, ch in config.input_channels.items():
            if "tally_leds" in ch:
                highest_pixel_id = max(highest_pixel_id, *ch["tally_leds"])
        self.pixels = neopixel.NeoPixel(config.tally_neopixel_pin, highest_pixel_id + 1, auto_write=False)

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
