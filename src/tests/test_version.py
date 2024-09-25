import unittest

from core.codebase_managemet.version import *

class Version(unittest.TestCase):
    def setUp(self):
        self.version = VersionManager

    def test_version(self):
        self.assertIsInstance(self.version.get(), dict, "Test case failed")

    def test_check_higher_version(self):
        self.assertFalse(self.version.check_version("50.50.50"), "Version match error")
        self.assertFalse(self.version.check_version("50.50.50-Production"), "Version match error")

    def test_check_lower_version(self):
        self.assertTrue(self.version.check_version("1.1.0"), "Version match error")
        self.assertTrue(self.version.check_version("4.9.0-Beta"), "Version match error")

if __name__ == "__main__":
    unittest.main()
