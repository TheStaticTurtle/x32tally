from .. import config
from .. import io
import time


def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return r, g, b


if __name__ == "__main__":
    leds = io.LedController()

    for ch, input_channel in config.input_channels.items():
        if "set_tally" in input_channel:
            leds.set(leds=input_channel["set_tally"], r=0, g=100, b=250)
            leds.update()
            time.sleep(0.01)

    for i in range(0, 4):
        color = (0, 100, 255) if i % 2 == 0 else (0, 0, 0)
        for ch, input_channel in config.input_channels.items():
            if "set_tally" in input_channel:
                leds.set(leds=input_channel["set_tally"], r=color[0], g=color[1], b=color[2])
        leds.update()
        time.sleep(0.1)

    for i in range(len(leds.pixels)):
        pixel_index = (i * 256 // len(leds.pixels))
        leds.pixels[i] = wheel(pixel_index & 255)
    leds.pixels.show()
