from core.intents.slots import SlotValueNumber
from core.skills import BaseSkill

class SimplePrevious(BaseSkill):
    def init(self):
        self.register("math@simple.previous")

    def execute(self, intent):
        super().execute(intent)
        self.require("mathoperation")
        self.require("number", SlotValueNumber)

        operation_function = self.convert()

        number: SlotValueNumber = self.get_obj("number")
        last_result = self.context_load("last_result")
        r = operation_function(last_result, number.value)

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
