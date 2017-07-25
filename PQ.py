class MinPQ(object):
	def __init__(self, MaxN):
		self.pq = []
		self.N = 0
		for i in range(0, MaxN + 1):
			self.pq.append(None)

	def less(self, i, j):
		return self.pq[i].weight < self.pq[j].weight

	def exch(self, i, j):
		self.pq[i], self.pq[j] = self.pq[j], self.pq[i]

	def swim(self, k):
		while k > 1 and self.less(k, int(k/2)):
			self.exch(int(k/2),k)
			k = int(k/2)

	def sink(self, k):
		while 2*k <= self.N:
			j = 2*k
			if j < self.N and self.less(j+1,j):
				j = j+1
			if self.less(k,j):
				break
			self.exch(k, j)
			k = j

	def is_empty(self):
		return self.N == 0

	def size(self):
		return self.N

	def insert(self, e):
		self.N = self.N + 1
		self.pq[self.N] = e
		self.swim(self.N)

	def del_min(self):
		Min = self.pq[1]
		self.exch(1, self.N)
		self.N = self.N - 1
		self.pq[self.N + 1] = None
		self.sink(1)
		return Min


class IndexMinPQ(object):
	def __init__(self, MaxN):
		self.pq = []
		self.qp = []
		self.keys = []
		self.N = 0
		for i in range(0, MaxN + 1):
			self.keys.append(None)
			self.pq.append(None)
			self.qp.append(-1)

	def less(self, i, j):

		if self.keys[self.pq[i]] == None:
			print(i,j)
			print(self.pq[i],self.pq[j])
		return self.keys[self.pq[i]] < self.keys[self.pq[j]]

	def exch(self, i, j):
		self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
		self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j

	def swim(self, k):
		while k > 1 and self.less(k, int(k/2)):
			self.exch(int(k/2),k)
			k = int(k/2)

	def sink(self, k):
		while 2*k <= self.N:
			j = 2*k
			if j < self.N and self.less(j+1,j):
				j = j+1
			if self.less(k,j):
				break
			self.exch(k, j)
			k = j

	def is_empty(self):
		return self.N == 0

	def contains(self, v):
		return self.qp[v] != -1

	def size(self):
		return self.N

	def insert(self, i, key):
		self.N = self.N + 1
		self.qp[i] = self.N
		self.pq[self.N] = i
		self.keys[i] =key
		self.swim(self.N)
	def min_index(self):
		return pq[1]

	def min_key(self):
		return self.key[self.pq[1]]

	def del_min(self):
		Min = self.pq[1]
		self.exch(1, self.N)
		self.N = self.N - 1
		self.sink(1)
		self.qp[Min] = -1
		self.keys[Min] = None
		self.pq[self.N + 1] = -1
		return Min

	def key_of(self, i):
		return self.keys[i]

	def change_key(self, i, key):
		self.keys[i] = key
		self.swim(self.qp[i])
		self.sink(self.qp[i])

	def change(self, i, key):
		self.change_key(i,key)

	def delete(self, i):
		index = self.qp[i]
		self.exch(index,self.N)
		self.N = self.N - 1
		self.swim(index)
		self.sink(index)
		self.keys[i] = None;
		self.qp[i] = -1
