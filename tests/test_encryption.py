import unittest
from src.core.system.security.encryption import cryptografy

class EncryptionTest(unittest.TestCase):
    def test_encrypt_match(self):
        seg = "Texto super seguro"
        crypted = cryptografy.encrypt(seg)
        decr = cryptografy.desencrypt(crypted)
        # Assert the result
        self.assertEqual(seg, decr, "Test case failed")

    def test_encrypt_dont_match(self):
        seg = "Texto super seguro"
        crypted = cryptografy.encrypt(seg)
        decr = cryptografy.desencrypt(crypted+"yeurhebkerhbgbh")
        # Assert the result
        self.assertNotEqual(seg, decr, "Test case failed")

if __name__ == '__main__':
    unittest.main()
