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

message_history = {}
def on_message(clt, userdata, msg):
    global message_history
    try:
        message_history[msg.topic] = json.loads(msg.payload)
    except json.decoder.JSONDecodeError:
        message_history[msg.topic] = msg.payload

client.on_message = on_message


for ch, input_channel in config.input_channels.items():
    if not input_channel["enabled"]:
        continue
    client.subscribe(f"modules/osc/ch/{ch:02d}/mix/on")
    client.subscribe(f"modules/osc/ch/{ch:02d}/mix/fader")
    client.subscribe(f"modules/stand_buttons/{ch:02d}/is_on_stand")

client.subscribe(f"modules/osc/status")


def try_get(obj, topic, default=None):
    if topic in obj:
        return obj[topic]
    return default



leds = io.LedController()

input_channels_with_leds = {
    ch: input_channel
    for ch, input_channel in config.input_channels.items()
    if "tally_leds" in input_channel
}

animation_counter = 0
animation_speed = 1


def do_disconnected_animation():
    global animation_counter
    global animation_speed

    animation_counter += animation_speed
    if animation_counter == len(input_channels_with_leds) - 1 or animation_counter == 0:
        animation_speed *= -1

    for input_channel in input_channels_with_leds.values():
        leds.set(leds=input_channel["tally_leds"], r=0, g=20, b=40)

    leds.set(leds=list(input_channels_with_leds.values())[animation_counter]["tally_leds"], r=0, g=75, b=200)
    if animation_counter > 0:
        leds.set(leds=list(input_channels_with_leds.values())[animation_counter - 1]["tally_leds"], r=0, g=50, b=150)
    if animation_counter < len(input_channels_with_leds) - 2:
        leds.set(leds=list(input_channels_with_leds.values())[animation_counter + 1]["tally_leds"], r=0, g=50, b=150)


def do_tally_lights():
    for ch, input_channel in input_channels_with_leds.items():
        color = [0, 0, 0]

        x32_on = try_get(message_history, f"modules/osc/ch/{ch:02d}/mix/on")
        x32_fader = try_get(message_history, f"modules/osc/ch/{ch:02d}/mix/fader")
        module_is_on_stand = try_get(message_history, f"modules/stand_buttons/{ch:02d}/is_on_stand")

        if input_channel["enabled"]:
            if x32_on is not None and x32_fader is not None:
                is_active = x32_on[0] and x32_fader[0] > 0.08

                color = config.tally_colors["active"] if is_active else config.tally_colors["muted"]

                if module_is_on_stand is not None:
                    if bool(module_is_on_stand) == is_active:
                        if int(time.time() * 5) % 2 == 0:
                            color = config.tally_colors["active_in_stand"] if is_active else config.tally_colors["muted_not_in_stand"]

        leds.set(leds=input_channel["tally_leds"], r=color[0], g=color[1], b=color[2])


while True:
    osc_status = try_get(message_history, f"modules/osc/status")

    if osc_status is None or not osc_status["connected"]:
        do_disconnected_animation()
    else:
        do_tally_lights()

    leds.update()
    time.sleep(0.05)
