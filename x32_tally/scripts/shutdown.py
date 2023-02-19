from .. import config
from .. import io
import time

# Shutdown script this script creates a LED controller and does some blinkie lights animations

if __name__ == "__main__":
    leds = io.LedController()

    for ch, input_channel in config.input_channels.items():
        if "tally_leds" in input_channel:
            leds.set(leds=input_channel["tally_leds"], r=0, g=100, b=255)
            leds.update()
            time.sleep(0.01)

    for ch, input_channel in config.input_channels.items():
        if "tally_leds" in input_channel:
            leds.set(leds=input_channel["tally_leds"], r=0, g=0, b=0)
            leds.update()
            time.sleep(0.01)

    for ch, input_channel in list(config.input_channels.items())[::-1]:
        if "tally_leds" in input_channel:
            leds.set(leds=input_channel["tally_leds"], r=0, g=100, b=255)
            leds.update()
            time.sleep(0.01)

    for ch, input_channel in list(config.input_channels.items())[::-1]:
        if "tally_leds" in input_channel:
            leds.set(leds=input_channel["tally_leds"], r=0, g=0, b=0)
            leds.update()
            time.sleep(0.01)
