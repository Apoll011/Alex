from typing import NamedTuple, Dict, Any
from enum import Enum

class Temperature(Enum):
    """Temperature enumeration"""
    celsius = 0
    fahrenheit = 0

class SlotValue(NamedTuple):
    """Base class for slot values"""
    kind: str
    value: Any

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

class SlotValueAmountOfMoney(SlotValue):
    """Slot value representing an amount of money"""
    value: int
    precision: str
    unit: str

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

class SlotValueNumber(SlotValue):
    """Slot value representing a number"""
    value: int

class SlotValueOrdinal(SlotValueNumber):
    """Slot value representing an ordinal number"""
    pass

class SlotValueTemperature(SlotValue):
    """Slot value representing a temperature"""
    value: float
    unit: Temperature

class SlotValueTimeInterval(SlotValue):
    """Slot value representing a time interval"""
    from_: str
    to: str

class SlotValuePercentage(SlotValue):
    """Slot value representing a percentage"""
    value: float

class SlotValueMusicAlbum(SlotValue):
    """Slot value representing a music album"""
    value: str

class SlotValueMusicArtist(SlotValue):
    """Slot value representing a music artist"""
    value: str

class SlotValueMusicTrack(SlotValue):
    """Slot value representing a music track"""
    value: str

class SlotValueCity(SlotValue):
    """Slot value representing a city"""
    value: str

class SlotValueCountry(SlotValue):
    """Slot value representing a country"""
    value: str

class SlotValueRegion(SlotValue):
    """Slot value representing a region"""
    value: str

class SlotRange(NamedTuple):
    """Range of values"""
    start: int
    end: int

class Slot(NamedTuple):
    """Slot representing a piece of information extracted from user input"""
    range: SlotRange
    raw_value: str
    value: SlotValue
    entity: str
    slot_name: str

class Entity(NamedTuple):
    """Entity representing a piece of information"""
    name: str
    value: str

class Intent(NamedTuple):
    """Intent representing the user's intention"""
    intent_name: str
    confidence: float

class IntentResponse(NamedTuple):
    """Response to a user's input, containing the input, intent, and slots"""
    input: str
    intent: Intent
    slots: list[Slot]

class IntentParserToObject:
    """Class for parsing intent data from a dictionary representation"""
    def __init__(self) -> None:
        """Initializes the parser"""
        pass

    def parse_slot(self, slot: Dict[str, Any]) -> Slot:
        """Parses a slot dictionary and returns a Slot instance"""
        range = SlotRange(start=slot["range"]["start"], end=slot["range"]["end"])
        raw_value = slot["rawValue"]
        entity = slot["entity"]
        slot_name = slot["slotName"]
        value = SlotValueFactory.create(**slot["value"])
        return Slot(range=range, raw_value=raw_value, value=value, entity=entity, slot_name=slot_name)

    def parse_intent(self, intent: Dict[str, Any]) -> Intent:
        """Parses an intent dictionary and returns an Intent instance"""
        intent_name = intent["intentName"]
        confidence = intent["probability"]
        return Intent(intent_name=intent_name, confidence=confidence)

    def parser(self, intentr: Dict[str, Any]) -> IntentResponse:
        """Parses the entire intent data dictionary and returns an IntentResponse instance"""
        input = intentr["input"]
        intent = self.parse_intent(intentr["intent"])
        slots = [self.parse_slot(slot) for slot in intentr["slots"]]
        return IntentResponse(input=input, intent=intent, slots=slots)
