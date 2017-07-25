class Edge(object):
	"""class of Edge"""
	def __init__(self, _v1, _v2, _weight):
		self.v1 = _v1
		self.v2 = _v2
		self.weight = _weight
	def weight(self):
		return self.weight

	def either(self):
		return self.v1

	def other(self, v):
		if v == self.v1: 
			return self.v2
		elif v == self.v2:
			return self.v1
	def show(self):
		print("(",self.v1,"," ,self.v2,")")