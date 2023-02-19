import json
import logging

import board
import neopixel
import digitalio
import paho.mqtt.client as mqtt

from . import config

# IO Wrappers
# This file contains wrappers for input and outputs.
# This allows you to easily customize input and output methods
# It also includes a function to create MQTT clients

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


def get_mqtt_client(client_id):
    client = mqtt.Client(
        client_id=client_id,
        reconnect_on_failure=True
    )
    client.enable_logger(logging.getLogger("MQTT"))
    client.connect(config.mqtt["host"], config.mqtt["port"], 60)
    return client


# Send the input_channels config to the MQTT server
def broadcast_config():
    import paho.mqtt.client as mqtt_client

    # Custom encoder for board pins
    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            return o.id if isinstance(o, board.D0.__class__) else o.__dict__

    __mqtt_client = mqtt_client.Client(client_id="config")
    __mqtt_client.connect(config.mqtt["host"], config.mqtt["port"], 60)
    __mqtt_client.publish(topic="config/input_channels", payload=JSONEncoder().encode(config.input_channels), retain=True)
broadcast_config()
