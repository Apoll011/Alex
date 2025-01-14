from typing import Optional, Union

from core.hardware.esp32.animation_config import GradientConfig, PulseConfig, StatusConfig
from core.hardware.esp32.color import Color
from core.hardware.esp32.structures import AnimationType, Pattern, PredefinedColor

class AnimationPresets:
    @staticmethod
    def warning_pulse(
            color: Optional[Union[Color, PredefinedColor]] = PredefinedColor.RED
    ) -> tuple[AnimationType, int, PulseConfig]:
        return (
            AnimationType.CONFIGURABLE_PULSE,
            2000,
            PulseConfig(speed=15, min_bright=50, max_bright=255, color=color),
        )

    @staticmethod
    def rainbow_wave(speed: int = 30) -> tuple[AnimationType, int, GradientConfig]:
        return (
            AnimationType.CONFIGURABLE_GRADIENT,
            5000,
            GradientConfig(
                speed=1,
                spread=2,
            ),
        )

    @staticmethod
    def status_ok() -> tuple[AnimationType, int, StatusConfig]:
        return (
            AnimationType.STATUS_INDICATOR,
            -1,  # Continuous
            StatusConfig(
                color=PredefinedColor.GREEN, pattern=Pattern.SOLID, blink=False
            ),
        )
