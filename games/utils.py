class Singleton(type):
	_instance = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls.__instance:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances


def get_value(_list, key_name, _key, value_name):
	for e in _list:
		if e[key_name] == _key:
			return e['value']
	return None
	