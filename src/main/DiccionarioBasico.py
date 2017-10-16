import logging

def getValueFromDict(dict, key):
	try:
		return dict[key]
	except KeyError:
		logging.error("El diccionario no tiene ninguna clave %s" % key)
	return None
