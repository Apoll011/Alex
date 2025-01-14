import json
import threading
import time

import websocket

from core.hardware.esp32.structures import Button
from core.interface import BaseInterface
from core.log import LOG

class ButtonHandler:
    def __init__(self, esp32_ip="192.168.1.100", port=82):
        self.ws = None
        self.esp32_ip = esp32_ip
        self.port = port
        self.connected = False
        self.callbacks = {}
        self.global_callback = None
        self.last_pressed = {}
        self.debounce_time = 0.2

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            state = data.get('state')
            value = data.get('value')

            if state != "pressed" or value is None:
                return

            button = self._identify_button(value)
            if button and self._debounce(button):
                if button in self.callbacks:
                    self.callbacks[button](BaseInterface.get().alex, state)

                # Call the global callback if registered
                if self.global_callback:
                    self.global_callback(BaseInterface.get().alex, button, state)
        except json.JSONDecodeError:
            LOG.error(f"Failed to parse message: {message}")

    @staticmethod
    def _identify_button(value):
        threshold = 0.15
        for button in Button:
            if abs(button.value - value) <= threshold:
                return button
        return None

    def _debounce(self, button):
        current_time = time.time()
        last_time = self.last_pressed.get(button, 0)
        if current_time - last_time >= self.debounce_time:
            self.last_pressed[button] = current_time
            return True
        return False

    def on_error(self, ws, error):
        LOG.error(f"Error: {error}")
        self.connected = False

    def on_close(self, ws, close_status_code, close_msg):
        LOG.info("Connection closed")
        self.connected = False
        # Try to reconnect after a delay
        time.sleep(5)
        self.connect()

    def on_open(self, ws):
        LOG.info("Connection established")
        self.connected = True

    def connect(self):
        ws_url = f"ws://{self.esp32_ip}:{self.port}"
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )

        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def register_callback(self, button, callback):
        """Register a callback function for a specific button"""
        if isinstance(button, Button):
            self.callbacks[button] = callback
        else:
            print(f"Invalid button type: {button}")

    def register_global_callback(self, callback):
        """Register a callback function for all buttons"""
        self.global_callback = callback

    def close(self):
        if self.ws:
            self.ws.close()
