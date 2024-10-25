import datetime
import http.client as httplib
from unittest import TestCase

from core.utils import get_time_of_day, internet_on, is_morning, resource_path

class TestUtils(TestCase):
    def setUp(self):
        self.time = None
        h = datetime.datetime.now().hour
        if h > 18 or h < 7:
            self.time = 3
        elif h >= 12:
            self.time = 2
        elif h >= 7:
            self.time = 1

    def test_get_time_of_day(self):

        self.assertEqual(get_time_of_day(), self.time, "TIme different")

    def test_is_morning(self):

        if self.time == 1:
            self.assertTrue(is_morning(), "Its morning")
        else:
            self.assertFalse(is_morning(), "Its not morning")

    def test_internet_on(self):
        connection = httplib.HTTPConnection("google.com", timeout=1)
        try:
            connection.request("HEAD", "/")
            connection.close()  # connection closed
            connected = True
        except Exception:
            connected = False

        self.assertEqual(internet_on(), connected)

    def test_resource_path(self):
        self.assertEqual(resource_path("core/"), "/home/pegasus/development/Alex/src/tests/src/core/")
