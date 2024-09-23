import http.client as httplib
from unittest import TestCase

from core.internet import InternetUser

class TestInternetUser(TestCase):
    def test_internet_on(self):
        connection = httplib.HTTPConnection("google.com", timeout=3)
        try:
            connection.request("HEAD", "/")
            connection.close()  # connection closed
            connected = True
        except Exception:
            connected = False

        self.assertEqual(InternetUser.internet_on(), connected)
