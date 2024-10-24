from typing import Dict, NamedTuple

from .slots import *

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
    slots: dict[str, Slot]
    json:Dict[str, Any]

class IntentParserToObject:
    """Class for parsing intent data from a dictionary representation"""
    def __init__(self):
        """Initializes the parser"""
        pass

    @staticmethod
    def parse_slot(slot: Dict[str, Any]) -> Slot:
        """Parses a slot dictionary and returns a Slot instance"""
        intent_range = SlotRange(start=slot["range"]["start"], end=slot["range"]["end"])
        raw_value = slot["rawValue"]
        entity = slot["entity"].replace("snips/", "")
        slot_name = slot["slotName"]
        value = SlotValueFactory.create(**slot["value"])
        return Slot(range=intent_range, raw_value=raw_value, value=value, entity=entity, slot_name=slot_name)

    @staticmethod
    def parse_intent(intent: Dict[str, Any]) -> Intent:
        """Parses an intent dictionary and returns an Intent instance"""
        intent_name = intent["intentName"]
        confidence = intent["probability"]
        return Intent(intent_name=intent_name, confidence=confidence)

    def parser(self, intent_obj: Dict[str, Any]) -> IntentResponse:
        """Parses the entire intent data dictionary and returns an IntentResponse instance"""
        intent_input = intent_obj["input"]
        intent = self.parse_intent(intent_obj["intent"])

        intent_slots = {}

        for slot in intent_obj["slots"]:
            s = self.parse_slot(slot)
            intent_slots[s.slot_name] = s
        return IntentResponse(input=intent_input, intent=intent, slots=intent_slots, json=intent_obj)

    @staticmethod
    def draw_intent(intent_response: IntentResponse) -> None:
        """
        Draw the intent response graphically in the terminal, using indentation and colors.
        """
        COLORS = {
            "input": "\033[94m",  # blue
            "intent": "\033[92m",  # green
            "slot": "\033[93m",  # yellow
            "entity": "\033[95m",  # magenta
            "value": "\033[96m",  # cyan
            "percentage": "\33[91m" #red
        }

        RESET_COLOR = "\033[0m"

        print(f"{COLORS['input']}{intent_response.input}{RESET_COLOR}")
        print(f"  Intent: {COLORS['intent']}{intent_response.intent.intent_name} ({COLORS['percentage']}{intent_response.intent.confidence:.2f}{COLORS['intent']}){RESET_COLOR}")
        for sl in intent_response.slots:
            slot = intent_response.slots[sl]
            print(f"  {COLORS['slot']}Slot:{RESET_COLOR}")
            print(f"    Entity: {COLORS['entity']}{slot.entity}{RESET_COLOR}")
            print(f"    Slot Name: {COLORS['slot']}{slot.slot_name}{RESET_COLOR}")
            print(f"    Raw Value: {COLORS['value']}{slot.raw_value}{RESET_COLOR}")
            print(f"    Value Kind: {COLORS['value']}{slot.value.kind}")
            if not isinstance(slot.value, SlotValueDuration):
                print(f"    {RESET_COLOR}Value: {COLORS['value']}{slot.value.value}")
            if isinstance(slot.value, SlotValueInstantTime):
                print(f"    {RESET_COLOR}Grain: {COLORS['value']}{slot.value.grain}")
                print(f"    {RESET_COLOR}Precision: {COLORS['value']}{slot.value.precision}")
            elif isinstance(slot.value, SlotValueAmountOfMoney):
                print(f"    {RESET_COLOR}Precision: {COLORS['value']}{slot.value.precision}")
                print(f"    {RESET_COLOR}Unit: {COLORS['value']}{slot.value.unit}")
            elif isinstance(slot.value, SlotValueDuration):
                print(f"    {RESET_COLOR}Years: {COLORS['value']}{slot.value.years}")
                print(f"    {RESET_COLOR}Quarters: {COLORS['value']}{slot.value.quarters}")
                print(f"    {RESET_COLOR}Months: {COLORS['value']}{slot.value.months}")
                print(f"    {RESET_COLOR}Weeks: {COLORS['value']}{slot.value.weeks}")
                print(f"    {RESET_COLOR}Days: {COLORS['value']}{slot.value.days}")
                print(f"    {RESET_COLOR}Hours: {COLORS['value']}{slot.value.hours}")
                print(f"    {RESET_COLOR}Minutes: {COLORS['value']}{slot.value.minutes}")
                print(f"    {RESET_COLOR}Seconds: {COLORS['value']}{slot.value.seconds}")
                print(f"    {RESET_COLOR}Precision: {COLORS['value']}{slot.value.precision}")
            elif isinstance(slot.value, SlotValueTemperature):
                print(f"    {RESET_COLOR}Unit: {COLORS['value']}{slot.value.unit.name}")
            elif isinstance(slot.value, SlotValueTimeInterval):
                print(f"    {RESET_COLOR}From: {COLORS['value']}{slot.value.from_}")
                print(f"    {RESET_COLOR}To: {COLORS['value']}{slot.value.to}")
            print(f"{RESET_COLOR}")
