from .. import config
import time

if __name__ == "__main__":
    for ch, input_channel in config.input_channels.items():
        if "set_tally" in input_channel:
            input_channel["set_tally"](0, 100, 255)
            config.update_leds()
            time.sleep(0.01)

    for ch, input_channel in config.input_channels.items():
        if "set_tally" in input_channel:
            input_channel["set_tally"](0, 0, 0)
            config.update_leds()
            time.sleep(0.01)

    for ch, input_channel in list(config.input_channels.items())[::-1]:
        if "set_tally" in input_channel:
            input_channel["set_tally"](0, 100, 255)
            config.update_leds()
            time.sleep(0.01)

    for ch, input_channel in list(config.input_channels.items())[::-1]:
        if "set_tally" in input_channel:
            input_channel["set_tally"](0, 0, 0)
            config.update_leds()
            time.sleep(0.01)
