from typing import NamedTuple


class Entitie(NamedTuple):
    name: str
    """
    Entitie name
    """

    value: str
    """
    The provided value
    """

class Intent(NamedTuple):
    intent_name: str
    """
    This is the intent name (ex: system@wake)
    """

    confidence: float
    """
    How much certaint was the intent recogizer about this sentence
    """

    text: str
    """
    Altered text to make fonetic sense in alex log
    """

    raw_text: str
    """
    Real input that was submitted
    """

    entities: list[Entitie]
    """
    List of the recognized entities
    """

    recognized_seconds: float
    """
    Time taked to recognize the sentence
    """

class IntentParserToObject:
    def __init__(self) -> None:
        pass

    def parser(self, intent:dict):
        e = []
        for ee in intent['entities']:
            e.append(Entitie(ee['name'], ee['value']))

        i = Intent(intent['intent_name'], intent['confidence'], intent['text'], intent['raw_text'], e, intent['recognized_seconds'])
        return i
