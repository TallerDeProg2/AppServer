#from unittest import TestCase
import unittest
from unittest.mock import patch

import sys
sys.path.append('../src')

from DiccionarioBasico import getValueFromDict
from DiccionarioBasico import logging


class TestDiccionarioBasico(unittest.TestCase):

	@patch('DiccionarioBasico.logging')
	def test_DiccionarioBasicoHasLogging(self, mock_logger):
		d = {}
		key = 1
		getValueFromDict(d, key)
		mock_logger.error.assert_called_with("El diccionario no tiene ninguna clave %s" % key)

if __name__ == '__main__':
	unittest.main()