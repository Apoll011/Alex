from random import randint

from core.resources.application import Application

class AlexKey:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def create() -> None:
        value = str(randint(999**3, 999**4))
        Application.save("key", value, opening_type="w+")
    
    @staticmethod
    def get() -> int:
        return int(Application.get("key"))
