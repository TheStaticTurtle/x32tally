import json
import logging
import time

import paho.mqtt.client as mqtt
from .. import config
from .. import io

import coloredlogs
import sys

coloredlogs.install(stream=sys.stdout, level=config.log_levels["tally_lights"])

# Tally light module
# This module activate the LEDs on the microphone holders. It requires the channel to be enabled and have pins defined.
# A channel is defined active if it is not muted and the fader is at least 8% up
# By default:
#   If the channel is active                      → Green LEDs
#   If the channel is NOT active                  → Red LEDs
#   If the channel is active and in the stand     → Flashing green LEDs
#   If the channel is NOT active and in the stand → Flashing red LEDs

# Get the MQTT client
client = io.get_mqtt_client("module_tally_lights")
client.loop_start()

# Define a dict to store message history, this is necessary because OSC message from the console comes asynchronously, and they are need all at the time.
message_history = {}

# Define a method responsible for receiving MQTT messages and storing them in the history
def on_message(clt, userdata, msg):
    global message_history
    try:
        message_history[msg.topic] = json.loads(msg.payload)
    except json.decoder.JSONDecodeError:
        message_history[msg.topic] = msg.payload

# Assign said function to the MQTT client
client.on_message = on_message

# Subscribe to MQTT topic for the mute, fader, and is_on_stand values
for ch, input_channel in config.input_channels.items():
    if not input_channel["enabled"]:
        continue
    client.subscribe(f"modules/osc/ch/{ch:02d}/mix/on")
    client.subscribe(f"modules/osc/ch/{ch:02d}/mix/fader")
    client.subscribe(f"modules/stand_buttons/{ch:02d}/is_on_stand")

# Also subscribe the global OSC status (used to check if the OSC module is connected to the console)
client.subscribe(f"modules/osc/status")

# Define a "try to get" function. This function tries to get a value from a dict and if not found return None instead of an exception
def try_get(obj, topic, default=None):
    if topic in obj:
        return obj[topic]
    return default

# Instantiate the LED controller
leds = io.LedController()

# Filter input channels from the config to only iterate over channels that have leds
input_channels_with_leds = {
    ch: input_channel
    for ch, input_channel in config.input_channels.items()
    if "tally_leds" in input_channel
}

# Define variables for animations
animation_counter = 0
animation_speed = 1


# Disconnected animation. This animation bounces a bright cyan light from side to side
def do_disconnected_animation():
    global animation_counter
    global animation_speed

    # Increase the counter
    animation_counter += animation_speed
    # If the counter has reached the end (or beginning), reverse it.
    if animation_counter == len(input_channels_with_leds) - 1 or animation_counter == 0:
        animation_speed *= -1

    # Set every holder to dark cyan.
    for input_channel in input_channels_with_leds.values():
        leds.set(leds=input_channel["tally_leds"], r=0, g=20, b=40)

    # Set the holder at position "counter" to bright cyan.
    leds.set(leds=list(input_channels_with_leds.values())[animation_counter]["tally_leds"], r=0, g=75, b=200)
    # If possible, set the adjacent holders to cyan
    if animation_counter > 0:
        leds.set(leds=list(input_channels_with_leds.values())[animation_counter - 1]["tally_leds"], r=0, g=50, b=150)
    if animation_counter < len(input_channels_with_leds) - 2:
        leds.set(leds=list(input_channels_with_leds.values())[animation_counter + 1]["tally_leds"], r=0, g=50, b=150)


# Tally light "animation". This function manages the LEDs according to the rules at the start of the file
def do_tally_lights():
    # Loop over every channel that have LEDs
    for ch, input_channel in input_channels_with_leds.items():
        # Set the default color to black
        color = [0, 0, 0]

        # Get the mute, fader and is_on_stand values from the history
        x32_on = try_get(message_history, f"modules/osc/ch/{ch:02d}/mix/on")
        x32_fader = try_get(message_history, f"modules/osc/ch/{ch:02d}/mix/fader")
        module_is_on_stand = try_get(message_history, f"modules/stand_buttons/{ch:02d}/is_on_stand")

        # If the channel is enabled
        if input_channel["enabled"]:
            # If the value stored in the history for the mute and fader values are not None
            if x32_on is not None and x32_fader is not None:
                # Calculate if the channel is active
                is_active = x32_on[0] and x32_fader[0] > 0.08

                # Set the channel color
                color = config.tally_colors["active"] if is_active else config.tally_colors["muted"]

                # if the value stored in the history for the is_on_stand is not None
                if module_is_on_stand is not None:
                    # If the channel is active and in the stand or not active and not in the stand
                    if bool(module_is_on_stand) == is_active:
                        # Math tricks to make it blink slower
                        if int(time.time() * 5) % 2 == 0:
                            # Set the bright color to the channel
                            color = config.tally_colors["active_in_stand"] if is_active else config.tally_colors["muted_not_in_stand"]
        # Set the leds
        leds.set(leds=input_channel["tally_leds"], r=color[0], g=color[1], b=color[2])


while True:
    # Get the OSC module status
    osc_status = try_get(message_history, f"modules/osc/status")

    # Test if the OSC module is connected and execute the proper function
    if osc_status is None or not osc_status["connected"]:
        do_disconnected_animation()
    else:
        do_tally_lights()

    # Update the leds
    leds.update()
    time.sleep(0.05)
