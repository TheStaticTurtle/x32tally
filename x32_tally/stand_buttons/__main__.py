import json
import logging
import time
import coloredlogs
import sys
from .. import config
from .. import io
import paho.mqtt.client as mqtt

coloredlogs.install(stream=sys.stdout, level=config.log_levels["stand_buttons"])

# Stand button modules
# This module read inputs from the IO module to find out if a microphone is on the stand or not.
# It reports the status over MQTT


# Get the MQTT client
client = mqtt.Client()
client.enable_logger(logging.getLogger("MQTT"))
client.connect(config.mqtt["host"], config.mqtt["port"], 60)
client.loop_start()

# Instantiate the input controller
inputs = io.InputController()

# Store the history of input. This is used in order to avoid spacing the MQTT server for values that did not change
last_channel_values = {}
while True:
    time.sleep(0.05)
    # Loop over every channel
    for ch, input_channel in config.input_channels.items():
        # Get (if possible) the value of the buttons, Defaults to None if the channel does not have a button
        channel_value = None
        if "on_stand_button" in input_channel:
            channel_value = inputs.get(input_channel["on_stand_button"])

        # If the status has changed, publish the values over MQTT
        if ch not in last_channel_values or last_channel_values[ch] != channel_value:
            last_channel_values[ch] = channel_value
            client.publish(
                topic=f"modules/stand_buttons/{ch:02d}/status",
                payload=json.dumps({
                    "enabled": input_channel["enabled"],
                    "has_button": "on_stand_button" in input_channel,
                    "value": channel_value,
                    "last_update": time.time()
                }),
                retain=True
            )
