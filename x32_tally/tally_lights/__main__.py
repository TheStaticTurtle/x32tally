import json
import logging
import time

import paho.mqtt.client as mqtt
from .. import config
from .. import io

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

client.subscribe(f"X32_STATUS/connected")

message_history = {}


def on_message(clt, userdata, msg):
    global message_history
    try:
        message_history[msg.topic] = json.loads(msg.payload)
    except json.decoder.JSONDecodeError:
        message_history[msg.topic] = msg.payload


def try_get(obj, topic):
    if topic in obj:
        return obj[topic]
    return None


client.on_message = on_message


leds = io.LedController()

animation_counter = 0
animation_speed = 1

input_channels = {
    ch: input_channel
    for ch, input_channel in config.input_channels.items()
    if "tally_leds" in input_channel
}

while True:
    connection_status = try_get(message_history, f"X32_STATUS/connected")
    if connection_status is not None and connection_status["status"]:
        for ch, input_channel in input_channels.items():
            color = [0, 0, 0]
            on = try_get(message_history, f"X32/ch/{ch:02d}/mix/on")
            fader = try_get(message_history, f"X32/ch/{ch:02d}/mix/fader")
            is_on_stand = try_get(message_history, f"ONSTAND_DETECTION/ch/{ch:02d}/is_on_stand")

            if on is not None and fader is not None:
                is_active = on[0] and fader[0] > 0.08

                color = config.tally_colors["active"] if is_active else config.tally_colors["muted"]

                if is_on_stand is not None:
                    if bool(is_on_stand) == is_active:
                        if int(time.time()*5) % 2 == 0:
                            color = config.tally_colors["active_in_stand"] if is_active else config.tally_colors["muted_not_in_stand"]
            leds.set(leds=input_channel["tally_leds"], r=color[0], g=color[1], b=color[2])
    else:
        animation_counter += animation_speed
        if animation_counter == len(input_channels) - 1 or animation_counter == 0:
            animation_speed *= -1

        for ch, input_channel in input_channels.items():
            leds.set(leds=input_channel["tally_leds"], r=0, g=20, b=40)

        leds.set(leds=list(input_channels.values())[animation_counter]["tally_leds"], r=0, g=75, b=200)
        if animation_counter > 0:
            leds.set(leds=list(input_channels.values())[animation_counter-1]["tally_leds"], r=0, g=50, b=150)
        if animation_counter < len(input_channels) - 2:
            leds.set(leds=list(input_channels.values())[animation_counter+1]["tally_leds"], r=0, g=50, b=150)


    leds.update()

    time.sleep(0.05)
