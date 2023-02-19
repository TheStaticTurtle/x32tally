import json
import logging
import coloredlogs
import sys

from pythonosc.osc_message import OscMessage
import paho.mqtt.client as mqtt
from x32_tally.osc.x32 import X32
from .. import config

coloredlogs.install(stream=sys.stdout, level=config.log_levels["osc"])

# OSC Module
# This module creates an instance of X32 and forward every message received to MQTT
# In addition it also sends ot the connection status that includes if the module is connected or not to the console and the console version/model

# Get the MQTT client
client = mqtt.Client()
client.enable_logger(logging.getLogger("MQTT"))
client.connect(config.mqtt["host"], config.mqtt["port"], 60)
client.loop_start()

# Get the X32 client
x32 = X32(config.x32_address)


# Define the function that forwards OSC message to the MQTT broker
def forward_to_mqtt(message: OscMessage):
    client.publish(
        topic=f"modules/osc{message.address}",
        payload=json.dumps(message.params),
        retain=True
    )


# Define the function that sends out the status of the module
def publish_connection_status(is_connected):
    client.publish(
        topic=f"modules/osc/status",
        payload=json.dumps({
            "connected": is_connected,
            "x32_server_version": x32.x32_server_version,
            "x32_server_name": x32.x32_server_name,
            "x32_console_model": x32.x32_console_model,
            "x32_console_version": x32.x32_console_version,
        }),
        retain=True
    )


# Set the handler for the X32 and start the client
x32.handlers.append(forward_to_mqtt)
x32.connection_handlers.append(publish_connection_status)
x32.start()

# Wait for the X32 client to end and stop the MQTT client
x32.join()
client.loop_stop()
