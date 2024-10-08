from core.intents.slots import SlotValueNumber
from core.skills import BaseSkill

class Simple(BaseSkill):
    def init(self):
        self.register("math@simple")

    def execute(self, intent):
        super().execute(intent)
        self.require("mathoperation")
        self.optional("first_number", SlotValueNumber)
        self.optional("second_number", SlotValueNumber)
        self.optional("number", SlotValueNumber)

        self.mathOp = self.slots["mathoperation"]

        operation_function = self.convert()

        r = None

        if self.is_single_number():
            number: SlotValueNumber = self.get_single_number()  # type: ignore
            last_result = self.alex_context.load("last_result")
            r = operation_function(last_result, number.value)

        elif self.slot_exists("first_number", "second_number"):
            fNumber: SlotValueNumber = self.slots["first_number"]  # type: ignore
            sNumber: SlotValueNumber = self.slots["second_number"]  # type: ignore
            r = operation_function(fNumber, sNumber)
            self.alex_context.save(r, "last_result")
        return self.responce_translated("result", {"result": r})

    def convert(self):
        if self.assert_equal("mathoperation", "plus"):
            return lambda x, y: x + y
        elif self.assert_equal("mathoperation", "times"):
            return lambda x, y: x * y
        elif self.assert_equal("mathoperation", "minus"):
            return lambda x, y: x - y
        elif self.assert_equal("mathoperation", "over"):
            return lambda x, y: x / y
        else:
            return lambda x, y: x.get_value() ^ y.get_value()

    def get_single_number(self):
        if self.is_single_number():
            if self.slot_exists("number"):
                return self.slots["number"]
            elif self.slot_exists("first_number") and not self.slot_exists("second_number"):
                return self.slots["first_number"]
            else:
                return self.slots["second_number"]

    def is_single_number(self):
        return self.slot_exists("number") or (
                self.slot_exists("first_number") and not self.slot_exists("second_number")) or (
                not self.slot_exists("first_number") and self.slot_exists("second_number"))
