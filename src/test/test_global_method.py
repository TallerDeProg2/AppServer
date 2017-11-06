import unittest
import sys


sys.path.append('../src')
from src.main import global_method as gm


class TestGlobalMethods(unittest.TestCase):
    def test_Encode(self):
        some_id = '12345679'
        token = gm.encode_token(some_id)

        self.assertTrue(isinstance(token, str))

    def test_Encode_withoutId(self):
        self.assertEqual(gm.encode_token(''), None)

    def test_Decode(self):
        some_id = '12345679'
        token = gm.encode_token(some_id)

        self.assertEqual(gm.decode_token(token), some_id)


if __name__ == '__main__':
    unittest.main()
