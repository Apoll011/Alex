from typing import Any
from enum import Enum
from dataclasses import dataclass

class Temperature(Enum):
    """Temperature enumeration"""
    celsius = 0
    fahrenheit = 1

@dataclass
class SlotValue:
    """Base class for slot values"""
    kind: str
    value: str

    def __str__(self) -> str:
        return f"{self.kind}: {self.value}"

    def to_dict(self) -> dict:
        return {"kind": self.kind, "value": self.value}

class SlotValueFactory:
    """Factory class for creating SlotValue instances"""
    @staticmethod
    def create(kind: str, **kwargs: Any) -> SlotValue:
        """Creates a SlotValue instance based on the kind parameter and additional keyword arguments"""
        if kind == "InstantTime":
            return SlotValueInstantTime(kind=kind, **kwargs)
        elif kind == "AmountOfMoney":
            return SlotValueAmountOfMoney(kind=kind, **kwargs)
        elif kind == "Duration":
            return SlotValueDuration(kind=kind, **kwargs)
        elif kind == "Number":
            return SlotValueNumber(kind=kind, **kwargs)
        elif kind == "Ordinal":
            return SlotValueOrdinal(kind=kind, **kwargs)
        elif kind == "Temperature":
            return SlotValueTemperature(kind=kind, **kwargs)
        elif kind == "TimeInterval":
            return SlotValueTimeInterval(kind=kind, **kwargs)
        elif kind == "Percentage":
            return SlotValuePercentage(kind=kind, **kwargs)
        elif kind == "MusicAlbum":
            return SlotValueMusicAlbum(kind=kind, **kwargs)
        elif kind == "MusicArtist":
            return SlotValueMusicArtist(kind=kind, **kwargs)
        elif kind == "MusicTrack":
            return SlotValueMusicTrack(kind=kind, **kwargs)
        elif kind == "City":
            return SlotValueCity(kind=kind, **kwargs)
        elif kind == "Country":
            return SlotValueCountry(kind=kind, **kwargs)
        elif kind == "Region":
            return SlotValueRegion(kind=kind, **kwargs)
        elif kind == "Custom":
            return SlotValue(kind=kind, **kwargs)
        else:
            raise ValueError(f"Unknown kind of SlotValue: {kind}")

@dataclass
class SlotValueInstantTime(SlotValue):
    """Slot value representing an instant time"""
    grain: str
    precision: str

    def get_grain(self) -> str:
        return self.grain

    def get_precision(self) -> str:
        return self.precision

@dataclass
class SlotValueAmountOfMoney(SlotValue):
    """Slot value representing an amount of money"""
    value: int
    precision: str
    unit: str

    def get_value(self) -> int:
        return self.value

    def get_unit(self) -> str:
        return self.unit

@dataclass
class SlotValueDuration(SlotValue):
    """Slot value representing a duration"""
    years: int
    quarters: int
    months: int
    weeks: int
    days: int
    hours: int
    minutes: int
    seconds: int
    precision: str

    def get_total_seconds(self) -> int:
        return self.seconds + self.minutes * 60 + self.hours * 3600 + self.days * 86400 + self.weeks * 604800 + self.months * 2629800 + self.quarters * 7889400 + self.years * 31557600

    def get_precision(self) -> str:
        return self.precision

@dataclass
class SlotValueNumber(SlotValue):
    """Slot value representing a number"""
    value: int

    def get_value(self) -> int:
        return self.value

    def is_even(self) -> bool:
        return self.value % 2 == 0

@dataclass
class SlotValueOrdinal(SlotValue):
    """Slot value representing an ordinal number"""
    value: int

    def get_value(self) -> int:
        return self.value

    def is_first(self) -> bool:
        return self.value == 1

@dataclass
class SlotValueTemperature(SlotValue):
    """Slot value representing a temperature"""
    value: float
    unit: Temperature

    def get_value(self) -> float:
        return self.value

    def get_unit(self) -> Temperature:
        return self.unit

@dataclass
class SlotValueTimeInterval(SlotValue):
    """Slot value representing a time interval"""
    from_: str
    to: str

    def get_from(self) -> str:
        return self.from_

    def get_to(self) -> str:
        return self.to

@dataclass
class SlotValuePercentage(SlotValue):
    """Slot value representing a percentage"""
    value: float

    def get_value(self) -> float:
        return self.value

    def is_positive(self) -> bool:
        return self.value > 0

@dataclass
class SlotValueMusicAlbum(SlotValue):
    """Slot value representing a music album"""
    value: str

    def get_value(self) -> str:
        return self.value

@dataclass
class SlotValueMusicArtist(SlotValue):
    """Slot value representing a music artist"""
    value: str

    def get_value(self) -> str:
        return self.value

@dataclass
class SlotValueMusicTrack(SlotValue):
    """Slot value representing a music track"""
    value: str

    def get_value(self) -> str:
        return self.value

@dataclass
class SlotValueCity(SlotValue):
    """Slot value representing a city"""
    value: str

    def get_value(self) -> str:
        return self.value

@dataclass
class SlotValueCountry(SlotValue):
    """Slot value representing a country"""
    value: str

    def get_value(self) -> str:
        return self.value

@dataclass
class SlotValueRegion(SlotValue):
    """Slot value representing a region"""
    value: str

    def get_value(self) -> str:
        return self.value
