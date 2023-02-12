from .. import config
import neopixel
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
    for ch, input_channel in config.input_channels.items():
        if "set_tally" in input_channel:
            input_channel["set_tally"](0, 100, 255)
            config.update_leds()
            time.sleep(0.01)

    for i in range(0, 4):
        color = (0, 100, 255) if i % 2 == 0 else (0, 0, 0)
        for ch, input_channel in config.input_channels.items():
            if "set_tally" in input_channel:
                input_channel["set_tally"](*color)
        config.update_leds()
        time.sleep(0.1)

    for i in range(len(config.pixels)):
        pixel_index = (i * 256 // len(config.pixels))
        config.pixels[i] = wheel(pixel_index & 255)
    config.pixels.show()
