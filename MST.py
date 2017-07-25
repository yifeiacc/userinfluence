from PQ import MinPQ
class MST (object):
	"""docstring for MST """
	def __init__(self, G):
		self.pq = MinPQ(G.num_V())
		self.mst = []
		self.marked = []
		for i in range(0, G.num_V()):
			self.marked.append(False)
		self.visit(G, 0)
		while not self.pq.is_empty():
			e = self.pq.del_min()
			v1 = e.either()
			v2 = e.other(v1)
			if self.marked[v1] and self.marked[v2]:#check if the edge in the tree
				continue
			self.mst.append(e)
			if not self.marked[v1]:
				self.visit(G, v1)
			if not self.marked[v2]:
				self.visit(G, v2)
	def visit(self, G, v):
		self.marked[v] = True
		for e in G.adj[v]:
			if not self.marked[e.other(v)]:# check is corss edge
				self.pq.insert(e)