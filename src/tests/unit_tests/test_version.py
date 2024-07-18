import unittest
from core.version import *

class Version(unittest.TestCase):
    def test_version(self):
        self.version = VersionManager.get()
        self.assertIsInstance(self.version, dict, "Test case failed")

    def test_check_higher_version(self):
        self.assertFalse(check_version("50.50.50"), "Version match error")
    
    def test_check_lower_version(self):
        self.assertTrue(check_version("1.1.0"), "Version match error")

if __name__ == '__main__':
    unittest.main()
