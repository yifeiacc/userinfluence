class EdgeWeightedGraph(object):
	"""docstring for ClassName"""
	def __init__(self, v):
		self.V = v
		self.E = 0
		self.adj = []
		for _v in range(0, v):
			self.adj.append(set())

	def num_V(self): 
		return self.V
	def num_E(self):
		return self.E
	def addEdge(self, e):
		v1 = e.either()
		v2 = e.other(v1)
		self.adj[v1].add(e)
		self.adj[v2].add(e)
		self.E = self.E + 1
	def show(self):
		for v in range(0,self.V):
			for e in self.adj[v]:
				e.show()
			print("________________")