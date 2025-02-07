from core.intents.slots import SlotValueNumber
from core.skills import BaseSkill

class Simple(BaseSkill):
    def init(self):
        self.register("math@simple")

    def execute(self, intent):
        super().execute(intent)
        self.require("mathoperation")
        self.require("first_number", SlotValueNumber)
        self.require("second_number", SlotValueNumber)

        operation_function = self.convert()

        r = None

        fNumber: SlotValueNumber = self.get_obj("first_number")
        sNumber: SlotValueNumber = self.get_obj("second_number")
        r = operation_function(fNumber, sNumber)
        self.context_save("last_result", r)

        return self.say("result", result=r)

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