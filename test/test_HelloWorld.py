import unittest

import sys
sys.path.append('../src')
import HelloWorld as hw

class TestHelloWorld(unittest.TestCase):

    def test_ReturnIsCorrect(self):
        message = hw.helloWorld()
        self.assertEqual(message, "Hello world!")

    def test_Split(self):
        message = hw.helloWorld()
        self.assertEqual(message[0], "H")
        
if __name__ == '__main__':
	unittest.main()
