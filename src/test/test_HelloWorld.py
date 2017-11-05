import unittest

import sys
sys.path.append('../src')
from src.main import HelloWorld as hw

class TestHelloWorld(unittest.TestCase):

    def test_ReturnIsCorrect(self):
        message = hw.helloWord()
        self.assertEqual(message, "Hello world!")

    def test_Split(self):
        message = hw.helloWord()
        self.assertEqual(message[0], "H")
        
if __name__ == '__main__':
	unittest.main()
