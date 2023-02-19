import logging
import socket
import threading
import time

from pythonosc.osc_bundle import OscBundle
from pythonosc.osc_message import OscMessage
from pythonosc.osc_message_builder import OscMessageBuilder


class X32(threading.Thread):
    def __init__(self, address):
        super().__init__()
        self._log = logging.getLogger(self.__class__.__name__)
        self._address = (address, 10023)
        self._socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self._socket.setblocking(False)

        self.x32_server_version = None
        self.x32_server_name = None
        self.x32_console_model = None
        self.x32_console_version = None

        self.last_resubscribe = 0
        self.last_resync = 0

        self.last_incoming = 0

        self.context = {}

        self.handlers = []
        self.connection_handlers = []

    def __repr__(self):
        return f"<X32 server_version=\"{self.x32_server_version}\" server_name=\"{self.x32_server_name}\" console_model=\"{self.x32_console_model}\" console_version=\"{self.x32_console_version}\">"

    @property
    def has_connection(self):
        return (time.time() - 30) < self.last_incoming

    def handle_message(self, message):
        self._log.debug(f"[RX] {message.address} {message.params}")

        self.last_incoming = time.time()

        self.context[message.address] = message
        if message.address == "/info":
            self.x32_server_version = message.params[0]
            self.x32_server_name = message.params[1]
            self.x32_console_model = message.params[2]
            self.x32_console_version = message.params[3]
            for handler in self.connection_handlers:
                handler(self.has_connection)

        for handler in self.handlers:
            handler(message)

    def _send(self, data: bytes):
        try:
            self._socket.sendto(data, self._address)
        except OSError as e:
            self._log.warning(f"Tried to send data but got: {e}")
        except Exception as e:
            self._log.error(f"Tried to send data but got: {e}")

    def _re_sync(self):
        self.last_resync = time.time()
        for i in range(1, 33):
            self._send(OscMessageBuilder(f"/ch/{i:02}/mix/on").build().dgram)
            self._send(OscMessageBuilder(f"/ch/{i:02}/mix/fader").build().dgram)
            self._send(OscMessageBuilder(f"/ch/{i:02}/config/icon").build().dgram)
            self._send(OscMessageBuilder(f"/ch/{i:02}/config/name").build().dgram)
            self._send(OscMessageBuilder(f"/ch/{i:02}/config/color").build().dgram)

    def _re_subscribe(self):
        self.last_resubscribe = time.time()
        self._log.info("[TX] Resubscribed")
        self._send(OscMessageBuilder("/xremote").build().dgram)
        self._send(OscMessageBuilder("/info").build().dgram)


    def run(self) -> None:
        last_connection_status = None
        while True:
            time.sleep(0.001)

            if self.last_resync + 60 < time.time():
                self._re_sync()

            if self.last_resubscribe + 5 < time.time():
                self._re_subscribe()

            if last_connection_status != self.has_connection:
                last_connection_status = self.has_connection
                for handler in self.connection_handlers:
                    handler(self.has_connection)
                if self.has_connection:
                    self._re_sync()

            try:
                data, peer = self._socket.recvfrom(1024)

                if data and OscMessage.dgram_is_message(data):
                    self.handle_message(OscMessage(data))

                if data and OscBundle.dgram_is_bundle(data):
                    for message in OscBundle(data):
                        self.handle_message(message)
            except BlockingIOError:
                pass
