class DirectedEdge(object):
	"""docstring for DirectedEdge"""
	def __init__(self, v, w, weight):
		self._v = v
		self._w = w
		self._weight = weight

	def weight(self):
		return self._weight

	def fromv(self):
		return self._v

	def to(self):
		return self._w

	def show(self):
		print("(", self._v, ",", self._w, ")")

class EdgeWeightedDigraph(object):
	"""docstring for EdgeWeightedDigraph"""
	def __init__(self, num_v):
		self._V = num_v
		self._E = 0
		self.adj = []
		for _ in range(0, num_v):
			self.adj.append(set())

	def V(self):
		return self._V

	def in_matrice(self, m):
		v, w = m.shape
		for i in range(0,v):
			for j in range(0,i):
				if m[i,j]!= 0:
					e = DirectedEdge(j, i, m[i,j])
					self.addEdge(e)
	def E(self):
		return self._E

	def addEdge(self, e):
		self.adj[e.fromv()].add(e)
		self._E = self._E + 1
	def show(self):
		for v in range(0,self._V):
			for e in self.adj[v]:
				e.show()
			print("________________")
		
		
		