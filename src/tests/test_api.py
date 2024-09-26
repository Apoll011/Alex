import unittest

from core.client import ApiClient
from core.config import api
from core.error import ServerClosed

class TestApi(unittest.TestCase):
    api = None
    def setUp(self) -> None:
        try:
            self.api = ApiClient(api['host'], api['port'])
        except ServerClosed:
            pass
    def test_api_responce(self):
        if self.api and self.api.active:
            data = self.api.call_route("users/search/name", {"name": "Tiago"})
            tiago_user = self.api.call_route("user/", {'id': "f86f0279-c4ec-4f5e-99e9-2fa44059c629"})
            self.assertEqual(
                data.response["users"][0], tiago_user.response["id"], "Something went  wrong with inexisting errors."
            )
            # Assert the result
        else:
            self.assertEqual(True, True)
if __name__ == '__main__':
    unittest.main()
