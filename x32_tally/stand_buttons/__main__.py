import json
import logging
import time
import coloredlogs
import sys
from .. import config
from .. import io
import paho.mqtt.client as mqtt

coloredlogs.install(stream=sys.stdout, level=config.log_levels["stand_buttons"])

client = mqtt.Client()
client.enable_logger(logging.getLogger("MQTT"))
client.connect(config.mqtt["host"], config.mqtt["port"], 60)
client.loop_start()

inputs = io.InputController()

last_channel_values = {}
while True:
    time.sleep(0.05)
    for ch, input_channel in config.input_channels.items():
        channel_value = None
        if "on_stand_button" in input_channel:
            channel_value = inputs.get(input_channel["on_stand_button"])

        if ch not in last_channel_values or last_channel_values[ch] != channel_value:
            last_channel_values[ch] = channel_value
            client.publish(
                topic=f"modules/stand_buttons/{ch:02d}/status",
                payload=json.dumps({
                    "enabled": input_channel["enabled"] and "on_stand_button" in input_channel,
                    "value": channel_value,
                    "last_update": time.time()
                }),
                retain=True
            )
