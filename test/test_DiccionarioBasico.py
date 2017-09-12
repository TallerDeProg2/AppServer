from unittest import TestCase
from DiccionarioBasico import getValueFromDict
from DiccionarioBasico import logging
from unittest.mock import patch

class TestDiccionarioBasico(TestCase):

	@patch('logging')
	def test_DiccionarioBasicoHasLogging(self, mock_logger):
		d = {}
		key = 1
		getValueFromDict(d, key)
		mock_logger.error.assert_called_with("El diccionario no tiene ninguna clave %s" % key)

if __name__ == '__main__':
	unittest.main()