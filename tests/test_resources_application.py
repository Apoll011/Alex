import unittest
from src.core.system.resources.application import Application

class ApplicationResources(unittest.TestCase):
    def test_getPath(self):
        app = Application
        self.assertEqual(app.load("dna"), "/Users/Pegasus/Library/Mobile Documents/com~apple~CloudDocs/Pegasus/Projects/Alex/Alex/src/resources/application/application.dna", "The path is wrong.")

    def test_get(self):
        app = Application
        self.assertEqual(app.get("test"), "e4g5egrdveyy35eyjenjjno[k]", "They are not Equal. Gets Not Working.")
        self.assertEqual(app.get("bgr"), "")
    
     
if __name__ == '__main__':
    unittest.main()
