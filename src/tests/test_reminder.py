from unittest import TestCase

from black import datetime

from core.intents import SlotValue, SlotValueInstantTime
from core.models import ReminderObject

class TestReminderObject(TestCase):
    def setUp(self):
        self.date_time = datetime.now()
        self.time = SlotValueInstantTime("SlotValueInstantTime", self.date_time.strftime("%Y-%m-%d %H:%M:%S"), "", "")
        value = SlotValue("SlotVaLue", "Feed")
        self.reminder = ReminderObject(self.time, value)

    def test_get_hour_and_minute(self):
        if self.time.get_hour() == "00" and self.time.get_minute() == "00":
            t = "12:00"
        else:
            t = f"{self.time.get_hour()}:{self.time.get_minute()}"

        self.assertEqual(self.reminder.get_hour_and_minute(), t, "Time dont match")

    def test_seconds(self):
        self.assertLess(self.reminder.seconds(), 0, "The seconds is greater than zero")

    def test_get_action(self):
        self.assertEqual(self.reminder.get_action(), "Feed", "Thes strings dont match")
