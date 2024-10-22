from datetime import datetime

from core.notifier import AlexEvent
from core.quotes import PyQuotes
from core.skills import BaseSkill
from core.translate import TranslationSystem
from core.utils import internet_on, is_morning

class Hi(BaseSkill):
    def init(self):
        self.register("saudation@hi")
        self.can_go_again = False

    def execute(self, intent):
        super().execute(intent)
        self.optional("timeOfDay")

        self.master_name = self.alex_context.load("master").name

        if self.slot_exists("timeOfDay"):
            if is_morning():
                self.register_event(AlexEvent.ALEX_GOOD_MORNING)
                self.morning_routine()
            else:
                self.say("greet.hi.based.on.time.of.day", time=self.slots["timeOfDay"])
        else:
            self.say("greet.hi", user=self.master_name)

    def morning_routine(self):
        if self.alex_context.load("master").is_birthday():
            self.say("happy.birth", user=self.master_name)
        self.say_morning_intro()

    def say_morning_intro(self):
        now = datetime.now()
        month_translation = TranslationSystem(self.alex().language, "months").get_translation(str(now.month))
        if internet_on():
            self.say(
                "morning.online",
                user_name=self.master_name,
                current_time=self.api(
                    "/lang/format/nice_time", lang=self.language, speech=True
                ).response,
                day=now.day,
                month=month_translation,
                brief_weather_description="Sunny",
                temperature="13",
                inspiring_quote=PyQuotes().get_clean_quote()
            )
        else:
            self.say(
                "morning.offline",
                user_name=self.master_name,
                current_time=self.api(
                    "/lang/format/nice_time", lang=self.language, speech=True
                ).response,
                day=now.day,
                month=month_translation
            )
