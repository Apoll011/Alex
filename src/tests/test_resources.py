import unittest

from core.resources.application import Application
from core.resources.data_files import DataFile

class ApplicationResources(unittest.TestCase):
    def test_getPath(self):
        app = Application
        self.assertEqual(
            app.load("dna"), "/home/pegasus/development/Alex/resources/user/application/application.dna",
            "The path is wrong."
        )

    def test_application_exist(self):
        result = Application.exist("dna")

        # Assert the result
        self.assertTrue(result, "Test case failed")

    def test_application_dont_exist(self):
        result = result = Application.exist("tiago")

        # Assert the result
        self.assertFalse(result, "Test case failed")
    
    def test_application_get(self):
        result = Application.get("key")

        # Assert the result
        self.assertEqual(result, "732178387248", "Test case failed")

    def test_application_load(self):
        result = result = Application.load("plug")

        # Assert the result
        self.assertEqual(
            result, "/home/pegasus/development/Alex/resources/user/application/application.plug", "Test case failed"
        )

class DataFileTest(unittest.TestCase):
    def test_data_files_exist(self):
        result = DataFile.exist("test", "txt")

        # Assert the result
        self.assertTrue(result, "Test case failed")

    def test_data_files_dont_exist(self):
        result = result = DataFile.exist("tiago", "ber")

        # Assert the result
        self.assertFalse(result, "Test case failed")
    
    def test_data_files_get(self):
        result = DataFile.get("test", "txt")

        # Assert the result
        self.assertEqual(result, "Test", "Test case failed")

    def test_data_files_load(self):
        result = result = DataFile.load("test", "txt")

        # Assert the result
        self.assertEqual(result, "/home/pegasus/development/Alex/resources/user/data/txt/test.txt", "Test case failed")


if __name__ == '__main__':
    unittest.main()
