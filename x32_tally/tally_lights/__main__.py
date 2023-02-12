import json
import logging
import time

import paho.mqtt.client as mqtt
from .. import config

import coloredlogs
import sys

coloredlogs.install(stream=sys.stdout, level=config.log_levels["tally_lights"])

client = mqtt.Client()
client.enable_logger(logging.getLogger("MQTT"))
client.connect(config.mqtt["host"], config.mqtt["port"], 60)
client.loop_start()


for ch, input_channel in config.input_channels.items():
    client.subscribe(f"X32/ch/{ch:02d}/mix/on")
    client.subscribe(f"X32/ch/{ch:02d}/mix/fader")
    client.subscribe(f"ONSTAND_DETECTION/ch/{ch:02d}/is_on_stand")

message_history = {}


def on_message(client, userdata, msg):
    global message_history
    try:
        message_history[msg.topic] = json.loads(msg.payload)
    except json.decoder.JSONDecodeError as e:
        pass

def try_get(obj, topic):
    if topic in obj:
        return obj[topic]
    return None

client.on_message = on_message


while True:
    for ch, input_channel in config.input_channels.items():
        if "set_tally" not in input_channel:
            continue

        color = [0, 0, 0]
        on = try_get(message_history, f"X32/ch/{ch:02d}/mix/on")
        fader = try_get(message_history, f"X32/ch/{ch:02d}/mix/fader")
        is_on_stand = try_get(message_history, f"ONSTAND_DETECTION/ch/{ch:02d}/is_on_stand")

        if on is not None and fader is not None:
            is_active = on[0] and fader[0] > 0.08

            color = [0, 10, 0] if is_active else [10, 0, 0]

            if is_on_stand is not None:
                if bool(is_on_stand) == is_active:
                    if int(time.time()*5) % 2 == 0:
                        color = [0, 75, 0] if is_active else [75, 0, 0]

        input_channel["set_tally"](*color)
    config.update_leds()

    time.sleep(0.05)

