def is_float(s):
	try:
		float(s)
		return True
	except ValueError:
		return False
	except TypeError:
		return False


print(is_float(None))