from dataclasses import dataclass
from typing import Optional

from core.hardware.esp32.structures import PredefinedColor

@dataclass
class Color:
    """Represents an RGB color that can be converted to various formats"""

    r: int
    g: int
    b: int

    @classmethod
    def from_hex(cls, hex_color: str) -> "Color":
        """Create color from hex string (e.g. '#FF0000')"""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            r = int(hex_color[0] * 2, 16)
            g = int(hex_color[1] * 2, 16)
            b = int(hex_color[2] * 2, 16)
        else:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)

        return cls(r, g, b)

    @classmethod
    def from_predefined(cls, color: PredefinedColor) -> "Color":
        """Create color from predefined enum"""
        color_map = {
            PredefinedColor.RED: cls(255, 0, 0),
            PredefinedColor.GREEN: cls(0, 255, 0),
            PredefinedColor.BLUE: cls(0, 0, 255),
            PredefinedColor.WHITE: cls(255, 255, 255),
            PredefinedColor.YELLOW: cls(255, 255, 0),
            PredefinedColor.PURPLE: cls(128, 0, 128),
            PredefinedColor.ORANGE: cls(255, 165, 0),
        }
        return color_map[color] if color in color_map.keys() else color

    def to_hex(self) -> str:
        """Convert to hex string"""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def to_predefined(self) -> Optional[PredefinedColor]:
        """Try to match to predefined color, return None if no match"""
        for predefined in PredefinedColor:
            if self == Color.from_predefined(predefined):
                return predefined
        return None

    def __str__(self) -> str:
        """Convert to string format for config"""
        if predefined := self.to_predefined():
            return predefined.value
        return self.to_hex()
