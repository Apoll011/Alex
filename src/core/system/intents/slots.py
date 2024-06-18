from typing import NamedTuple, Dict, Any
from enum import Enum


class Temperature(Enum):
    """Temperature enumeration"""
    celsius = 0
    fahrenheit = 0

class SlotValue(NamedTuple):
    """Base class for slot values"""
    kind: str
    value: str

class SlotValueFactory:
    """Factory class for creating SlotValue instances"""
    @staticmethod
    def create(kind: str, **kwargs: Any):
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
            return SlotValueTimeInterval(kind=kind, from_ = kwargs["from"], to = kwargs["to"])
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

class SlotValueInstantTime(NamedTuple):
    """Slot value representing an instant time"""
    kind: str
    value: str
    grain: str
    precision: str

class SlotValueAmountOfMoney(NamedTuple):
    """Slot value representing an amount of money"""
    kind: str
    value: int
    precision: str
    unit: str

class SlotValueDuration(NamedTuple):
    """Slot value representing a duration"""
    kind: str
    years: int
    quarters: int
    months: int
    weeks: int
    days: int
    hours: int
    minutes: int
    seconds: int
    precision: str

class SlotValueNumber(NamedTuple):
    """Slot value representing a number"""
    kind: str
    value: int

class SlotValueOrdinal(NamedTuple):
    """Slot value representing an ordinal number"""
    kind: str
    value: int

class SlotValueTemperature(NamedTuple):
    """Slot value representing a temperature"""
    kind: str
    value: float
    unit: Temperature

class SlotValueTimeInterval(NamedTuple):
    """Slot value representing a time interval"""
    kind: str
    from_: str
    to: str

class SlotValuePercentage(NamedTuple):
    """Slot value representing a percentage"""
    kind: str
    value: float

class SlotValueMusicAlbum(NamedTuple):
    """Slot value representing a music album"""
    kind: str
    value: str

class SlotValueMusicArtist(SlotValue):
    """Slot value representing a music artist"""
    value: str

class SlotValueMusicTrack(NamedTuple):
    """Slot value representing a music track"""
    kind: str
    value: str

class SlotValueCity(NamedTuple):
    """Slot value representing a city"""
    kind: str
    value: str

class SlotValueCountry(NamedTuple):
    """Slot value representing a country"""
    kind: str
    value: str

class SlotValueRegion(NamedTuple):
    """Slot value representing a region"""
    kind: str
    value: str
