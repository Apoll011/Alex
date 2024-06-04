import unittest
from src.core.system.security.code import Key

class AlexKeyTest(unittest.TestCase):
    def test_key(self):
        key = Key.get()
        print(key)
        self.assertIsInstance(key, str, "Test case failed")

if __name__ == '__main__':
    unittest.main()
