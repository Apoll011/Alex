import unittest

from core.security.encryption import cryptography

class EncryptionTest(unittest.TestCase):
    def test_encrypt_match(self):
        seg = "Texto super seguro"
        crypted = cryptography.encrypt(seg)
        decr = cryptography.desencrypt(crypted)
        # Assert the result
        self.assertEqual(seg, decr, "Test case failed")

    def test_encrypt_dont_match(self):
        seg = "Texto super seguro"
        crypted = cryptography.encrypt(seg)
        decr = cryptography.desencrypt(crypted + "yeurhebkerhbgbh")
        # Assert the result
        self.assertNotEqual(seg, decr, "Test case failed")

if __name__ == '__main__':
    unittest.main()
