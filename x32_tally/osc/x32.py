import logging
import socket
import sys
import threading
import time
import struct
import shlex

import coloredlogs
from pythonosc.osc_bundle import OscBundle
from pythonosc.osc_message import OscMessage
from pythonosc.osc_message_builder import OscMessageBuilder

def _is_number_tryexcept(s):
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

# X32 Class
# This class serves as a client for the console
class X32(threading.Thread):
    def __init__(self, address):
        super().__init__()
        # Define a logger
        self._log = logging.getLogger(self.__class__.__name__)
        # Store the address
        self._address = (address, 10023)
        # Create a socket to talk to the X32.
        # The X32 will respond on the same ethereal port that is used to send the message hence why there should be only one socket per client
        self._socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self._socket.setblocking(False)

        # Create variables to store the X32 infos
        self.x32_server_version = "Unknown"
        self.x32_server_name = "Unknown"
        self.x32_console_model = "Unknown"
        self.x32_console_version = "Unknown"

        # Set timers to 0
        self.last_resubscribe = 0
        self.last_resync = 0

        # Set a timer for the last
        self.last_incoming = 0

        # List of handlers for messages
        self.handlers = []
        self.connection_handlers = []

    def __repr__(self):
        return f"<X32 server_version=\"{self.x32_server_version}\" server_name=\"{self.x32_server_name}\" console_model=\"{self.x32_console_model}\" console_version=\"{self.x32_console_version}\">"

    # has_connection property, this check that the last message from the console is less than 30sec old
    @property
    def has_connection(self):
        return (time.time() - 15) < self.last_incoming

    def handle_message__info(self, message):
        self.x32_server_version = message.params[0]
        self.x32_server_name = message.params[1]
        self.x32_console_model = message.params[2]
        self.x32_console_version = message.params[3]
        for handler in self.connection_handlers:
             handler(self.has_connection)

    def handle_message__subscribed_faders(self, message):
        if len(message.params[0]) != (4 + 4 * 32 + 4 * 32):
            self._log.warning("Messaged recevied by the /subscribed/faders handler that doesn't have the right size ({len(message.params[0])} != 260)")
            return
        data = struct.unpack(f"<i32i32f", message.params[0])[1:]  # Ignore first byte which is the length
        # Fake messages to maintain compatibility
        for i, value in enumerate(data[:32]):
            msg = OscMessageBuilder(f"/ch/{i+1:02}/mix/on")
            msg.add_arg(value)
            self.handle_message(msg.build())
        for i, value in enumerate(data[32:]):
            msg = OscMessageBuilder(f"/ch/{i+1:02}/mix/fader")
            msg.add_arg(value)
            self.handle_message(msg.build())

    def handle_message__node(self, message):
        data = shlex.split(message.params[0][:-1])
        msg = OscMessageBuilder(data[0])
        for param in data[1:]:
            msg.add_arg((int(float(param)) if float(param).is_integer() else float(param)) if _is_number_tryexcept(param) else param)
        self.handle_message(msg.build())


    # Internal OSC message handler
    def handle_message(self, message):
        # Log it
        self._log.debug(f"[RX] {message.address} {message.params}")
        # Reset the last incoming timer
        self.last_incoming = time.time()

        # Manually subscribed
        if message.address == "/subscribed/faders":
            self.handle_message__subscribed_faders(message)
            return  # Subscribed aliases are internal message no need to forward it

        # Node messages need to be unpacked and repackaged
        if message.address == "/node":
            self.handle_message__node(message)
            return  # Can't forward node responses

        # If the address is "/info" retrieve the server version/name and the console model/version and trigger the connection handlers
        if message.address == "/info":
            self.handle_message__info(message)

        # The message to every other handler
        for handler in self.handlers:
            handler(message)

    # Wrapper function use to send data to the console.
    # The function tries to send the message but does not raise an error if it fails (it just logs it).
    # This can happen if the network card is not up yet
    def _send(self, data: bytes):
        try:
            self._socket.sendto(data, self._address)
        except OSError as e:
            self._log.warning(f"Tried to send data but got: {e}")
        except Exception as e:
            self._log.error(f"Tried to send data but got: {e}")


    def _x32_format_subscribe(self, alias, addresses, start_i, end_i, interval=20):
        message = OscMessageBuilder("/formatsubscribe")
        message.add_arg(alias)
        for address in addresses:
            message.add_arg(address)
        message.add_arg(start_i)
        message.add_arg(end_i)
        message.add_arg(interval)
        self._send(message.build().dgram)

    def _x32_renew(self, alias):
        message = OscMessageBuilder("/renew")
        message.add_arg(alias)
        self._send(message.build().dgram)

    def _x32_xremote(self):
        message = OscMessageBuilder("/xremote")
        self._send(message.build().dgram)

    def _x32_info(self):
        message = OscMessageBuilder("/info")
        self._send(message.build().dgram)

    def _x32_showdump(self):
        message = OscMessageBuilder("/showdump")
        self._send(message.build().dgram)


    def _query_channel(self, channel):
        self._send(OscMessageBuilder(f"/ch/{channel:02}/mix/on").build().dgram)
        self._send(OscMessageBuilder(f"/ch/{channel:02}/mix/fader").build().dgram)
        self._send(OscMessageBuilder(f"/ch/{channel:02}/config/icon").build().dgram)
        self._send(OscMessageBuilder(f"/ch/{channel:02}/config/name").build().dgram)
        self._send(OscMessageBuilder(f"/ch/{channel:02}/config/color").build().dgram)

    def _query_show(self):
        self._x32_showdump()
        self._send(OscMessageBuilder(f"/-prefs/show_control").build().dgram)
        self._send(OscMessageBuilder(f"/‐show/prepos/current").build().dgram)
        self._send(OscMessageBuilder(f"/-show/showfile/show/name").build().dgram)


    # Resync function. This function is executed every 60sec to make sure the internal status is up-to-date with the console
    def _re_sync(self):
        self._log.info("[TX] Forced queried infos and subscribed")
        self.last_resync = time.time()

        for i in range(1, 33):
            self._query_channel(i)

        self._x32_format_subscribe(
            alias="/subscribed/faders",
            addresses=["/ch/**/mix/on", "/ch/**/mix/fader"],
            start_i=1, end_i=32,
            interval=20
        )

        self._query_show()

    # Resubscribe function. This function is executed every 5sec to subscribe to updates from the console
    def _re_subscribe(self):
        self.last_resubscribe = time.time()
        self._log.info("[TX] Renewed subscriptions")
        self._x32_xremote()
        self._x32_info()
        self._x32_renew("/subscribed/faders")

    # Main function of the thread
    def run(self) -> None:
        # Temp variable to avoid sending the same value over and over
        last_connection_status = None
        # Main loop
        while True:
            time.sleep(0.001)

            # Resync timer
            if self.last_resync + 60 < time.time():
                self._re_sync()
            # Resubscribe timer
            if self.last_resubscribe + 5 < time.time():
                self._re_subscribe()

            # Connection status check
            if last_connection_status != self.has_connection:
                last_connection_status = self.has_connection
                # Notify handlers
                for handler in self.connection_handlers:
                    handler(self.has_connection)
                # Force a resync if we just connected
                if self.has_connection:
                    self._re_sync()

            try:
                # A while loop here will ensure that if there is still data incoming it will be read before processing re-syncs
                # recvfrom will throw an error if there isn't anything thus exiting the loop
                while True:
                    # Receive data from the socket
                    data, peer = self._socket.recvfrom(1024)

                    # If data is present, and it's an OSC message, send it to the internal handler
                    if data and OscMessage.dgram_is_message(data):
                        self.handle_message(OscMessage(data))
                    # The message might also be a "/node" message from the console. These message don't start with / and thus don't comply with the OCS standard.
                    # Manually correct the address and send it to the internal handler
                    elif data.startswith(b"node"):
                        data = data.replace(b"node\x00\x00\x00\x00", b"/node\x00\x00\x00")
                        self.handle_message(OscMessage(data))
                    # If data is present, and it's an OSC bundle, unpack it and send all message to the internal handler
                    elif data and OscBundle.dgram_is_bundle(data):
                        for message in OscBundle(data):
                            self.handle_message(message)
                    else:
                        self._log.error(f"Received invalid data: {data}")
            except BlockingIOError:
                # Ignore BlockingIO errors
                pass
