from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from core.hardware.esp32.color import Color
from core.hardware.esp32.structures import Direction, Pattern, PredefinedColor, Speed

class AnimationConfig:
    """Base class for animation configurations"""

    def to_config_string(self) -> str:
        """Convert config to string format expected by LED controller"""
        config_parts = []
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, Color):
                    config_parts.append(f"{key.upper()}:{str(value)}")
                elif isinstance(value, Enum):
                    config_parts.append(f"{key.upper()}:{value.value}")
                elif isinstance(value, bool):
                    config_parts.append(f"{key.upper()}:{"TRUE" if value else "FALSE"}")
                else:
                    config_parts.append(f"{key.upper()}:{value}")
        return ";".join(config_parts)

@dataclass
class PulseConfig(AnimationConfig):
    speed: Optional[int] = None
    min_bright: Optional[int] = None
    max_bright: Optional[int] = None
    color: Optional[Union[Color, PredefinedColor]] = None

@dataclass
class ChaseConfig(AnimationConfig):
    fade: Optional[int] = None
    tail: Optional[int] = None
    color: Optional[Union[Color, PredefinedColor]] = None
    reverse: Optional[bool] = None
    speed: Optional[int] = None

@dataclass
class SparkleConfig(AnimationConfig):
    fade: Optional[int] = None
    chance: Optional[int] = None
    color: Optional[Union[Color, PredefinedColor]] = None

@dataclass
class GradientConfig(AnimationConfig):
    speed: Optional[int] = None
    spread: Optional[int] = None
    start_hue: Optional[int] = None
    reverse: Optional[bool] = None

@dataclass
class WaveConfig(AnimationConfig):
    speed: Optional[int] = None
    waves: Optional[int] = None
    color: Optional[Union[Color, PredefinedColor]] = None

@dataclass
class StatusConfig(AnimationConfig):
    color: Optional[Union[Color, PredefinedColor]] = None
    pattern: Optional[Pattern] = None
    speed: Optional[int] = None
    blink: Optional[bool] = None
    bspeed: Optional[int] = None

@dataclass
class ProgressConfig(AnimationConfig):
    progress: Optional[int] = None  # 0-100
    active_color: Optional[Union[Color, PredefinedColor]] = None
    inactive_color: Optional[Union[Color, PredefinedColor]] = None
    reverse: Optional[bool] = None

@dataclass
class FireworkConfig(AnimationConfig):
    rocket_color: Optional[Union[Color, PredefinedColor]] = None
    burst_color: Optional[Union[Color, PredefinedColor]] = None
    trail_length: Optional[int] = None
    burst_size: Optional[int] = None
    fade_rate: Optional[int] = None
    speed: Optional[Speed] = None
    pattern: Optional[Pattern] = Pattern.SPARKLE

@dataclass
class MeteorConfig(AnimationConfig):
    meteor_color: Optional[Union[Color, PredefinedColor]] = None
    trail_color: Optional[Union[Color, PredefinedColor]] = None
    size: Optional[int] = None
    decay: Optional[int] = None
    speed: Optional[Speed] = None
    direction: Optional[Direction] = None
    pattern: Optional[Pattern] = Pattern.GRADIENT

@dataclass
class RippleConfig(AnimationConfig):
    ripple_color: Optional[Union[Color, PredefinedColor]] = None
    bg_color: Optional[Union[Color, PredefinedColor]] = None
    speed: Optional[Speed] = None
    fade_rate: Optional[int] = None
    max_waves: Optional[int] = None
    auto_trigger: Optional[bool] = None
    pattern: Optional[Pattern] = Pattern.GRADIENT

@dataclass
class PixelsConfig(AnimationConfig):
    color1: Optional[Union[Color, PredefinedColor]] = None
    color2: Optional[Union[Color, PredefinedColor]] = None
    density: Optional[int] = None
    change_rate: Optional[Speed] = None
    fade_rate: Optional[int] = None
    smooth: Optional[bool] = None
    pattern: Optional[Pattern] = Pattern.SPARKLE

@dataclass
class ScannerConfig(AnimationConfig):
    color: Optional[Union[Color, PredefinedColor]] = None
    size: Optional[int] = None
    fade_rate: Optional[int] = None
    speed: Optional[Speed] = None
    direction: Optional[Direction] = Direction.BOUNCE
    trail: Optional[bool] = None
    pattern: Optional[Pattern] = Pattern.SOLID

@dataclass
class StrobeConfig(AnimationConfig):
    on_color: Optional[Union[Color, PredefinedColor]] = None
    off_color: Optional[Union[Color, PredefinedColor]] = None
    on_time: Optional[int] = None
    off_time: Optional[int] = None
    pulses: Optional[int] = None
    gap_time: Optional[int] = None
    alternating: Optional[bool] = None
    speed: Optional[Speed] = None
    pattern: Optional[Pattern] = Pattern.SOLID

@dataclass
class AuroraConfig(AnimationConfig):
    hue1: Optional[int] = None
    hue2: Optional[int] = None
    saturation: Optional[int] = None
    speed: Optional[Speed] = None
    scale: Optional[int] = None
    intensity: Optional[int] = None
    blend: Optional[bool] = None
    pattern: Optional[Pattern] = Pattern.GRADIENT

@dataclass
class PlasmaConfig(AnimationConfig):
    speed: Optional[Speed] = None
    scale: Optional[int] = None
    hue_shift: Optional[int] = None
    saturation: Optional[int] = None
    multi_color: Optional[bool] = None
    color: Optional[Union[Color, PredefinedColor]] = None
    pattern: Optional[Pattern] = Pattern.RAINBOW
