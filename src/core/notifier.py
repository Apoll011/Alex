from enum import Enum
from typing import Any
from uuid import uuid4

class AlexEvent(Enum):
    ALEX_LOOP = "loop"
    ALEX_GOOD_MORNING = "good_morning"
    ALEX_WAKE = "wake"

    def __iter__(self):
        yield self

class Notify:
    events_callbacks: dict[str, dict[str, Any | list[Any]]] = {

    }
    events: dict[AlexEvent, list[str]] = {

    }

    def register(self, function, events: list[AlexEvent] | AlexEvent, *args, **kwargs):
        events_list = list(events)

        function_id = str(uuid4())
        self.events_callbacks[function_id] = {"function": function, "args": args, "kwargs": kwargs}

        for event in events_list:
            if event in self.events:
                self.events[event].append(function_id)
            else:
                self.events[event] = [function_id]

    def event(self, event: AlexEvent):
        if event in self.events:
            for function_ids in self.events[event]:
                function, args, kwargs = self.events_callbacks[function_ids].values()
                function(event.name, *args, **kwargs)
