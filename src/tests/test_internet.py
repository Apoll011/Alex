import http.client as httplib
from unittest import TestCase

from core.utils import internet_on

class TestInternetUser(TestCase):
    def test_internet_on(self):
        connection = httplib.HTTPConnection("google.com", timeout=1)
        try:
            connection.request("HEAD", "/")
            connection.close()  # connection closed
            connected = True
        except Exception:
            connected = False

        self.assertEqual(internet_on(), connected)
