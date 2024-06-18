from core.system.intents import IntentParserToObject


intent = IntentParserToObject().parser({
  "input": "I need a flight leaving tomorow to Berlin",
  "intent": {
    "intentName": "searchFlight",
    "probability": 1.0
  },
  "slots": [
    {
      "range": {
        "start": 24,
        "end": 31
      },
      "rawValue": "tomorow",
      "value": {
        "kind": "InstantTime",
        "value": "2024-06-19 00:00:00 -01:00",
        "grain": "Day",
        "precision": "Exact"
      },
      "entity": "snips/datetime",
      "slotName": "date"
    },
    {
      "range": {
        "start": 35,
        "end": 41
      },
      "rawValue": "Berlin",
      "value": {
        "kind": "Custom",
        "value": "Berlin"
      },
      "entity": "city",
      "slotName": "destination"
    }
  ]
})

IntentParserToObject.draw_intent(intent)
