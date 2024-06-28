from typing import Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

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

class SlotValueInstantTime(SlotValue):
    """Slot value representing an instant time"""
    grain: str
    precision: str
    value: str

    def __init__(self, kind: str, value: str, grain: str, precision: str):
        super().__init__(kind, value)
        self.grain = grain
        self.precision = precision

    def to_datetime(self) -> datetime:
        """Converts the value to a datetime object"""
        if self.precision == "year":
            return datetime.strptime(self.value, "%Y")
        elif self.precision == "month":
            return datetime.strptime(self.value, "%Y-%m")
        elif self.precision == "day":
            return datetime.strptime(self.value, "%Y-%m-%d")
        elif self.precision == "hour":
            return datetime.strptime(self.value, "%Y-%m-%d %H")
        elif self.precision == "minute":
            return datetime.strptime(self.value, "%Y-%m-%d %H:%M")
        elif self.precision == "second":
            return datetime.strptime(self.value, "%Y-%m-%d %H:%M:%S")
        else:
            raise ValueError(f"Unknown precision: {self.precision}")

    def get_year(self) -> int | None:
        """Returns the year component of the value"""
        return int(self.value[:4])

    def get_month(self) -> int | None:
        """Returns the month component of the value"""
        if self.precision == "month":
            return int(self.value[5:7])
        else:
            return int(self.value[5:7]) if len(self.value) > 4 else None

    def get_day(self) -> int | None:
        """Returns the day component of the value"""
        if self.precision == "day":
            return int(self.value[8:10])
        else:
            return int(self.value[8:10]) if len(self.value) > 7 else None

    def get_hour(self) -> int | None:
        """Returns the hour component of the value"""
        if self.precision == "hour":
            return int(self.value[11:13])
        else:
            return int(self.value[11:13]) if len(self.value) > 10 else None

    def get_minute(self) -> int | None:
        """Returns the minute component of the value"""
        if self.precision == "minute":
            return int(self.value[14:16])
        else:
            return int(self.value[14:16]) if len(self.value) > 13 else None

    def get_second(self) -> int | None:
        """Returns the second component of the value"""
        if self.precision == "second":
            return int(self.value[17:19])
        else:
            return int(self.value[17:19]) if len(self.value) > 16 else None

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

    def to_float(self) -> float:
        """Converts the value to a float"""
        return float(self.value)

    def format(self) -> str:
        """Formats the value as a string with the unit"""
        return f"{self.to_float():.2f} {self.unit}"

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
        """Returns the total number of seconds in the duration"""
        return self.seconds + self.minutes * 60 + self.hours * 3600 + self.days * 86400 + self.weeks * 604800 + self.months * 2629800 + self.quarters * 7889400 + self.years * 31557600

    def get_precision(self) -> str:
        """Returns the precision of the duration"""
        return self.precision

    def to_string(self) -> str:
        """Converts the duration to a string representation"""
        parts = []
        if self.years > 0:
            parts.append(f"{self.years} years")
        if self.quarters > 0:
            parts.append(f"{self.quarters} quarters")
        if self.months > 0:
            parts.append(f"{self.months} months")
        if self.weeks > 0:
            parts.append(f"{self.weeks} weeks")
        if self.days > 0:
            parts.append(f"{self.days} days")
        if self.hours > 0:
            parts.append(f"{self.hours} hours")
        if self.minutes > 0:
            parts.append(f"{self.minutes} minutes")
        if self.seconds > 0:
            parts.append(f"{self.seconds} seconds")

        if len(parts) == 1:
            return parts[0]
        elif len(parts) == 2:
            return f"{parts[0]} and {parts[1]}"
        else:
            return ", ".join(parts[:-1]) + f", and {parts[-1]}"

@dataclass
class SlotValueNumber(SlotValue):
    """Slot value representing a number"""
    value: int

    def get_value(self) -> int:
        return self.value

    def is_even(self) -> bool:
        return self.value % 2 == 0

    def is_positive(self) -> bool:
        return self.value > 0

    def is_negative(self) -> bool:
        return self.value < 0

    def abs(self) -> int:
        return abs(self.value)

    def __add__(self, other):
        if isinstance(other, int):
            return SlotValueNumber(kind="Number", value=self.value + other)
        elif isinstance(other, SlotValueNumber):
            return SlotValueNumber(kind="Number", value=self.value + other.value)
        else:
            raise ValueError(f"Cannot add {self.value} and {other}")

    def __sub__(self, other):
        if isinstance(other, int):
            return SlotValueNumber(kind="Number", value=self.value - other)
        elif isinstance(other, SlotValueNumber):
            return SlotValueNumber(kind="Number", value=self.value - other.value)
        else:
            raise ValueError(f"Cannot subtract {other} from {self.value}")

    def __mul__(self, other):
        if isinstance(other, int):
            return SlotValueNumber(kind="Number", value=self.value * other)
        elif isinstance(other, SlotValueNumber):
            return SlotValueNumber(kind="Number", value=self.value * other.value)
        else:
            raise ValueError(f"Cannot multiply {self.value} and {other}")

    def __truediv__(self, other):
        if isinstance(other, int):
            return self.value / other
        elif isinstance(other, SlotValueNumber):
            return self.value / other.value
        else:
            raise ValueError(f"Cannot divide {self.value} by {other}")

    def __mod__(self, other):
        if isinstance(other, int):
            return self.value % other
        elif isinstance(other, SlotValueNumber):
            return self.value % other.value
        else:
            raise ValueError(f"Cannot find the modulus of {self.value} and {other}")

    def __pow__(self, other):
        if isinstance(other, int):
            return self.value ** other
        elif isinstance(other, SlotValueNumber):
            return self.value ** other.value
        else:
            raise ValueError(f"Cannot raise {self.value} to the power of {other}")

@dataclass
class SlotValueOrdinal(SlotValue):
    """Slot value representing an ordinal number"""
    value: int

    def get_value(self) -> int:
        return self.value

    def is_first(self) -> bool:
        return self.value == 1

    def is_last(self) -> bool:
        """Returns True if the ordinal is the last in its series, and False otherwise"""
        return self.value == len(self.get_series())

    def get_series(self) -> list[int]:
        """Returns a list of all ordinals in the series to which this ordinal belongs"""
        series = []
        for i in range(1, self.value + 2):
            series.append(i)
        return series

    def get_previous(self) -> int | None:
        """Returns the previous ordinal in the series, or None if this is the first ordinal"""
        if self.is_first():
            return None
        else:
            return self.value - 1

    def get_next(self) -> int | None:
        """Returns the next ordinal in the series, or None if this is the last ordinal"""
        if self.is_last():
            return None
        else:
            return self.value + 1

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
