import json
import logging
import coloredlogs
import sys

from pythonosc.osc_message import OscMessage
import paho.mqtt.client as mqtt
from x32_tally.osc.x32 import X32
from .. import config

coloredlogs.install(stream=sys.stdout, level=config.log_levels["osc"])


client = mqtt.Client()
client.enable_logger(logging.getLogger("MQTT"))
client.connect(config.mqtt["host"], config.mqtt["port"], 60)
client.loop_start()


def forward_to_mqtt(message: OscMessage):
    client.publish(f"X32{message.address}", json.dumps(message.params), retain=True)


def publish_connection_status(is_connected):
    client.publish(f"X32_STATUS/connected", json.dumps({"status": is_connected}), retain=True)


x32 = X32(config.x32_address)
x32.handlers.append(forward_to_mqtt)
x32.connection_handlers.append(publish_connection_status)
x32.start()


x32.join()
client.loop_stop()