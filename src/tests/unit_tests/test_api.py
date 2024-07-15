import unittest
from core.api.client import ApiClient
from core.config import api

class TestApi(unittest.TestCase):
    def setUp(self) -> None:
        self.api =  ApiClient(api['host'], api['port'])

    def test_api_exist(self):
        
        self.assertEqual(self.api.active, True, "Error Server Not Active")

    def test_api_responce(self):
        p = self.api.call_route_async("users/search/name", {"query": "Tiago"})
        p.then(lambda data: self.assertEqual(data["result"], "0000000001", "Something went  wrong with inexisting errors."))
        # Assert the result
        
if __name__ == '__main__':
    unittest.main()
