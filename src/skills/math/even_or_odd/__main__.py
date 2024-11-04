from core.intents.slots import SlotValueNumber
from core.skills import BaseSkill

class EvenOrOdd(BaseSkill):
    def init(self):
        self.register("math@even.or.odd")

    def is_prime(self):
        if self.number.value > self.setting("prime_search_limit"):
            return self.say("search.limit")

        for i in range(2, int(self.number.value // 2)):
            if self.number.value % i == 0:
                return self.say(f"prime.no", number=self.number.value)

        return self.say(f"prime.yes", number=self.number.value)

    def execute(self, intent):
        super().execute(intent)
        self.require("number", SlotValueNumber)
        self.optional("type")

        self.number: SlotValueNumber = self.get_obj("number")

        if self.slot_exists("type") and self.assert_equal("type", "prime"):
            r = self.is_prime()
        elif self.slot_exists("type") and self.assert_equal("type", "even"):
            r = self.make_responce("yes", "no")
        elif self.slot_exists("type") and self.assert_equal("type", "odd"):
            r = self.make_responce("no", "yes")
        else:
            r = self.make_responce()
        return r

    def make_responce(self, first="", second=""):
        last = "odd"
        f = second
        if self.number.is_even():
            last = "even"
            f = first
        return self.say(f"responce.{f}.{last}", number=self.number.value)
