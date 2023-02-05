import json
import logging
import coloredlogs
import sys

coloredlogs.install(stream=sys.stdout, level=logging.DEBUG)

from pythonosc.osc_message import OscMessage
import paho.mqtt.client as mqtt
from x32_tally.osc.x32 import X32

from ..config import mqtt, x32_address

client = mqtt.Client()
client.enable_logger(logging.getLogger("MQTT"))
client.connect(mqtt["host"], mqtt["port"], 60)
client.loop_start()


def forward_to_mqtt(message: OscMessage):
    client.publish(f"X32{message.address}", json.dumps(message.params), retain=True)


x32 = X32(x32_address)
x32.handlers.append(forward_to_mqtt)
x32.start()


x32.join()
client.loop_stop()