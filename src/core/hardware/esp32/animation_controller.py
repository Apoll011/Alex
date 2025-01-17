from typing import Dict, Optional

from core.hardware.esp32.animation_config import AnimationConfig
from core.hardware.esp32.color import Color
from core.hardware.esp32.structures import AnimationType, PredefinedColor

class AnimationController:
    def __init__(self, sender=None):
        self.sender = sender

        self.saved_animations: Dict[str, tuple[AnimationType, int, AnimationConfig]] = {}
    def clear(self):
        """Clear all LEDs"""
        self.sender("CLEAR")

    def set_led(self, index: int, color: Color | PredefinedColor):
        """Set a single LED to a specific color"""
        if isinstance(color, Color):
            msg = f"LED:{index},{color.r},{color.g},{color.b}"
        else:
            msg = f"LED:{index},{color.value}"
        self.sender(msg)

    def play_animation(self,
                       animation_type: AnimationType,
                       duration: int,
                       config: Optional[AnimationConfig] = None):
        """Play an animation with optional configuration"""
        config_str = config.to_config_string() if config else ""
        msg = f"ANIMATION:{animation_type.value},{duration},{config_str}"
        self.sender(msg)

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
