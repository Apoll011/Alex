from datetime import datetime

from core.user import User

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

        self.master: User = self.context_load("master")

        if self.slot_exists("timeOfDay"):
            if is_morning():
                self.register_event(AlexEvent.ALEX_GOOD_MORNING)
                self.morning_routine()
            else:
                self.say("greet.hi.based.on.time.of.day", time=self.get("timeOfDay"))
        else:
            self.say("greet.hi", user=self.master.first_name())

    def morning_routine(self):
        self.birthday_related()
        self.say_morning_intro()

    def say_morning_intro(self):
        now = datetime.now()
        month_translation = TranslationSystem(self.get_language(), "months").get_translation(str(now.month))
        if internet_on():
            self.say(
                "morning.online",
                user_name=self.master.first_name(),
                current_time=self.api(
                    "/lang/format/nice_time", lang=self.get_language(), speech=True
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
                user_name=self.master.first_name(),
                current_time=self.api(
                    "/lang/format/nice_time", lang=self.get_language(), speech=True
                ).response,
                day=now.day,
                month=month_translation
            )

    def birthday_related(self):
        if self.master.is_birthday():
            self.say("happy.birth", user=self.master.name)
        elif self.is_birthday_coming():
            self.say("birthday.in.less.than", days=self.master.distance_to_birthday().days)
        elif self.master.distance_to_birthday().days == 2:
            self.say("birthday.tomorrow", years=self.master.data.body.age + 1)

    def is_birthday_coming(self):
        """
        Returns True if user makes birthday in the range defined in config between 2 and 31 days depending on the selected by the user
        :return: Boolean
        """
        return self.config("birthday_warning") >= self.master.distance_to_birthday().days > 2 and \
            self.config("birthday_warning") > 2
