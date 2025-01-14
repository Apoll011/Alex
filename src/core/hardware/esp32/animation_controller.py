import threading
from typing import Dict, Optional

import websocket

from core.hardware.esp32.animation_config import AnimationConfig
from core.hardware.esp32.color import Color
from core.hardware.esp32.structures import AnimationType, PredefinedColor
from core.log import LOG

class AnimationController:
    def __init__(self, host: str, port: int = 81):
        self.uri = f"ws://{host}:{port}"
        self.websocket: Optional[websocket.WebSocketApp] = None
        self.saved_animations: Dict[str, tuple[AnimationType, int, AnimationConfig]] = {}
        self.thread: Optional[threading.Thread] = None
        self.connected = False

    def on_open(self, ws):
        LOG.info("WebSocket connection opened")
        self.connected = True

    def on_close(self, ws, close_status_code, close_msg):
        LOG.info("WebSocket connection closed")
        self.connected = False

    def on_error(self, ws, error):
        LOG.error(f"WebSocket error: {error}")

    def connect(self):
        """Connect to the WebSocket server"""
        self.websocket = websocket.WebSocketApp(
            self.uri,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
        )
        self.thread = threading.Thread(target=self.websocket.run_forever, daemon=True)
        self.thread.start()

    def disconnect(self):
        """Disconnect from the WebSocket server"""
        if self.websocket and self.connected:
            self.websocket.close()
            self.thread.join()

    def clear(self):
        """Clear all LEDs"""
        if self.websocket and self.connected:
            self.websocket.send("CLEAR")

    def set_led(self, index: int, color: Color | PredefinedColor):
        """Set a single LED to a specific color"""
        if self.websocket and self.connected:
            if isinstance(color, Color):
                msg = f"LED:{index},{color.r},{color.g},{color.b}"
            else:
                msg = f"LED:{index},{color.value}"
            self.websocket.send(msg)

    def play_animation(self,
                       animation_type: AnimationType,
                       duration: int,
                       config: Optional[AnimationConfig] = None):
        """Play an animation with optional configuration"""
        if self.websocket and self.connected:
            config_str = config.to_config_string() if config else ""
            msg = f"ANIMATION:{animation_type.value},{duration},{config_str}"
            self.websocket.send(msg)

    def save_animation(self,
                       name: str,
                       animation_type: AnimationType,
                       duration: int,
                       config: AnimationConfig):
        """Save an animation configuration for later use"""
        self.saved_animations[name] = (animation_type, duration, config)

    def play_saved_animation(self, name: str):
        """Play a previously saved animation"""
        if name in self.saved_animations:
            animation_type, duration, config = self.saved_animations[name]
            self.play_animation(animation_type, duration, config)
        else:
            raise ValueError(f"No saved animation named '{name}'")
