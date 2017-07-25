from PQ import IndexMinPQ
class ShortestPath(object):
	"""docstring for shortestPath"""
	def __init__(self, G, s):
		self.edgeTo = []
		self.distTo = []
		self.pq = IndexMinPQ(G.V())
		for v in range(0, G.V()):
			self.distTo.append(float("inf"))
			self.edgeTo.append(None)
		self.distTo[s] = 0.0
		self.pq.insert(s, 0.0)
		assert(not self.pq.is_empty())
		while not self.pq.is_empty():
			self.relax(G, self.pq.del_min())
	def relax(self, G, v):
		for e in G.adj[v]:
			w = e.to()
			if self.distTo[w] > self.distTo[v] + e.weight():
				self.distTo[w] = self.distTo[v] + e.weight()
				self.edgeTo[w] = e
				if self.pq.contains(w):
					self.pq.change(w,self.distTo[w])
				else:
					self.pq.insert(w,self.distTo[w])
	def distTo(self, v):
		return self.distTo[v]
	def has_path_to(self, v):
		return self.distTo[v] < float("inf")


		
		