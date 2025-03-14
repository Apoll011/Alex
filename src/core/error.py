
class MissingMainSkillClass(Exception):
    def __init__(self, skill_name: str, skill) -> None:
        super().__init__(
            "The skill", skill, " is missing the main class ", skill_name.title()
        )

class SkillIntentError(Exception):
    def __init__(self, skill_name: str, name: str) -> None:
        super().__init__(
            f"This is the wrong skill({skill_name}) for this intent({name})"
        )

class SkillNotRegistered(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(
            f"This skill {name} was not registered. Register it in the initialization function by using self.register(\"{name}\")."
        )

class SkillSlotNotFound(Exception):
    slot_name: str

    def __init__(self, slot_name: str) -> None:
        self.slot_name = slot_name
        super().__init__("The slot: " + slot_name + " was not found")

class InterfaceNotRegistered(Exception):
    def __init__(self) -> None:
        super().__init__(
            "The Alex Interface is still not registered when it was requested."
        )

class ServerClosed(Exception):
    def __init__(self) -> None:
        super().__init__("The Alex Base Server Is Closed.")

class RegisterNotValid(BaseException):
    def __init__(self, name) -> None:
        super().__init__(f"Register {name} Not Valid")
