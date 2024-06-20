import unittest
from src.core.system.api.call import ApiCall
from core.system.config import api

class TestApi(unittest.TestCase):
    def setUp(self) -> None:
        self.api =  ApiCall(api['host'], api['port'])

    def test_api_exist(self):
        
        self.assertEqual(self.api.active, True, "Error Server Not Active")

    def test_api_responce(self):
        p = self.api.call_route("users/search/name", {"query": "Tiago"})
        p.then(lambda data: self.assertEqual(data["result"], "0000000001", "Something went  wrong with inexisting errors."))
        # Assert the result
        
if __name__ == '__main__':
    unittest.main()
