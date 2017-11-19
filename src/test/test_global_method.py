import unittest
import sys
from unittest.mock import patch

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

    # @patch('src.main..validate_token', return_value=True)
    def test_Decode_ExpireeSignature(self):
        pass

    def test_Decode_InvalidToken(self):
        pass
        # some_id = '12345679'
        # token = gm.encode_token(some_id)
        #
        # self.assertEqual(gm.decode_token(token), some_id)

    def test_validate_token_OK(self):
        some_id = '12345679'
        token = gm.encode_token(some_id)

        self.assertTrue(gm.validate_token(token))

    def test_validate_token_NOK(self):
        self.assertTrue(gm.validate_token("5"))

    def test_validate_tokenId_OK(self):
        some_id = '12345679'
        token = gm.encode_token(some_id)

        self.assertTrue(gm.validate_token(token, some_id))

    def test_validate_tokenId_NOK(self):
        some_id = '12345679'
        token = gm.encode_token(some_id)

        self.assertFalse(gm.validate_token(token, "1"))


if __name__ == '__main__':
    unittest.main()
