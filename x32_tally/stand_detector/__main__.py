import logging
import time
import coloredlogs
import sys
from .. import config
from .. import io
import paho.mqtt.client as mqtt

coloredlogs.install(stream=sys.stdout, level=config.log_levels["stand_detector"])

client = mqtt.Client()
client.enable_logger(logging.getLogger("MQTT"))
client.connect(config.mqtt["host"], config.mqtt["port"], 60)
client.loop_start()

inputs = io.InputController()

status = {}
last_status = {}
while True:
    time.sleep(0.05)
    for ch, input_channel in config.input_channels.items():
        if "on_stand_button" not in input_channel:
            status[ch] = None
        else:
            status[ch] = 1 if inputs.get(input_channel["on_stand_button"]) else 0

        if ch not in last_status or status[ch] != last_status[ch]:
            last_status[ch] = status[ch]
            logging.info(f"Channel {ch} changed status to: {status[ch]}")
            client.publish(f"ONSTAND_DETECTION/ch/{ch:02d}/is_on_stand", last_status[ch], retain=True)
