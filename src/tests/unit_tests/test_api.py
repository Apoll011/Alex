import unittest
from core.api.client import ApiClient
from core.config import api

class TestApi(unittest.TestCase):
    def setUp(self) -> None:
        self.api =  ApiClient(api['host'], api['port'])

    def test_api_exist(self):
        
        self.assertEqual(self.api.active, True, "Error Server Not Active")

    def test_api_responce(self):
        data = self.api.call_route("users/search/name", {"name": "Tiago"})
        tiago_user = self.api.call_route("user/", {'id': "f86f0279-c4ec-4f5e-99e9-2fa44059c629"})
        self.assertEqual(data.response["users"][0], tiago_user.response["id"], "Something went  wrong with inexisting errors.")
        # Assert the result
        
if __name__ == '__main__':
    unittest.main()
