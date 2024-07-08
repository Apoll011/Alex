class SkillIntentError(Exception):
     def __init__(self, skill_name: str, name: str) -> None:
          super().__init__(f"This is the wrong skill({skill_name}) for this intent({name})")

class SkillSlotNotFound(Exception):
     def __init__(self, slot_name: str) -> None:
          super().__init__("The slot: " + slot_name + " was not found")
