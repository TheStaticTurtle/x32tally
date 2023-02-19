import logging
import socket
import threading
import time

from pythonosc.osc_bundle import OscBundle
from pythonosc.osc_message import OscMessage
from pythonosc.osc_message_builder import OscMessageBuilder


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
        self.x32_server_version = None
        self.x32_server_name = None
        self.x32_console_model = None
        self.x32_console_version = None

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
        return (time.time() - 30) < self.last_incoming

    # Internal OSC message handler
    def handle_message(self, message):
        # Log it
        self._log.debug(f"[RX] {message.address} {message.params}")

        # Reset the last incoming timer
        self.last_incoming = time.time()

        # If the address is "/info" retrive the server version/name and the console model/version and trigger the connection handlers
        if message.address == "/info":
            self.x32_server_version = message.params[0]
            self.x32_server_name = message.params[1]
            self.x32_console_model = message.params[2]
            self.x32_console_version = message.params[3]
            for handler in self.connection_handlers:
                handler(self.has_connection)

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

    # Resync function. This function is executed every 60sec to make sure the internal status is up-to-date with the console
    def _re_sync(self):
        self.last_resync = time.time()
        for i in range(1, 33):
            self._send(OscMessageBuilder(f"/ch/{i:02}/mix/on").build().dgram)
            self._send(OscMessageBuilder(f"/ch/{i:02}/mix/fader").build().dgram)
            self._send(OscMessageBuilder(f"/ch/{i:02}/config/icon").build().dgram)
            self._send(OscMessageBuilder(f"/ch/{i:02}/config/name").build().dgram)
            self._send(OscMessageBuilder(f"/ch/{i:02}/config/color").build().dgram)

    # Resubscribe function. This function is executed every 5sec to subscribe to updates from the console
    def _re_subscribe(self):
        self.last_resubscribe = time.time()
        self._log.info("[TX] Resubscribed")
        self._send(OscMessageBuilder("/xremote").build().dgram)
        self._send(OscMessageBuilder("/info").build().dgram)

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
                # Receive data from the socket
                data, peer = self._socket.recvfrom(1024)

                # If data is present, and it's an OSC message, send it to the internal handler
                if data and OscMessage.dgram_is_message(data):
                    self.handle_message(OscMessage(data))

                # If data is present, and it's an OSC bundle, unpack it and send all message to the internal handler
                if data and OscBundle.dgram_is_bundle(data):
                    for message in OscBundle(data):
                        self.handle_message(message)
            except BlockingIOError:
                # Ignore BlockingIO errors
                pass
