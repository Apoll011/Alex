import json
import time

from core.hardware.esp32.structures import Button
from core.interface import BaseInterface
from core.log import LOG

class ButtonHandler:
    def __init__(self):
        self.callbacks = {}
        self.global_callback = None
        self.last_pressed = {}
        self.debounce_time = 0.2

    def on_button_pressed(self, message):
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

    def register_callback(self, button, callback):
        """Register a callback function for a specific button"""
        if isinstance(button, Button):
            self.callbacks[button] = callback
        else:
            print(f"Invalid button type: {button}")

    def register_global_callback(self, callback):
        """Register a callback function for all buttons"""
        self.global_callback = callback