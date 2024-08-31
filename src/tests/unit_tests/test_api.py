import unittest
from core.api.client import ApiClient
from core.config import api

class TestApi(unittest.TestCase):
    def setUp(self) -> None:
        self.api =  ApiClient(api['host'], api['port'])

    def test_api_exist(self):
        
        self.assertEqual(self.api.active, True, "Error Server Not Active")

    def test_api_responce(self):
        data = self.api.call_route("users/search/name", {"query": "Tiago"})
        self.assertEqual(data.response, ["0000000001"], "Something went  wrong with inexisting errors."))
        # Assert the result
        
if __name__ == '__main__':
    unittest.main()
