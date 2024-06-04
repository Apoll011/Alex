import unittest
from src.core.system.error import Error

class TestError(unittest.TestCase):
    def test_error_exist(self):
        result = Error.get(404)
        # Assert the result
        self.assertEqual(result[1], 404, "Error 404 didn't exists")

    def test_error_dont_exist(self):
        result = Error.get(938)
        # Assert the result
        self.assertEqual(result[1], 304, "Something went  wrong with inexisting errors.")
if __name__ == '__main__':
    unittest.main()
