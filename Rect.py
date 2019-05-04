class Rect:
	def __init__(self, x1, y1, x2, y2):
		x1 = int(x1)
		y1 = int(y1)
		x2 = int(x2)
		y2 = int(y2)
		self.x1 = min(x1, x2)
		self.y1 = min(y1, y2)
		self.x2 = max(x1, x2)
		self.y2 = max(y1, y2)
		self.w = self.x2 - self.x1
		self.h = self.y2 - self.y1

	def shift(self, x, y):
		self.x1 += x
		self.y1 += y
		self.x2 += x
		self.y2 += y

	def area(self):
		return self.w * self.h

	def bound(self, x1, y1, x2, y2):
		self.x1 = max(self.x1, x1)
		self.y1 = max(self.y1, y1)
		self.x2 = max(self.x2, x2)
		self.y2 = max(self.y2, y2)

	def overlap(self, other):
		dx = min(self.x2, other.x2) - max(self.x1, other.x1)
		dy = min(self.y2, other.y2) - max(self.y1, other.y2)
		print('dy: ' + str(dy) + ', dx: ' + str(dx))
		if (dx >= 0) and (dy >= 0):
			return dx * dy
		return 0

	def intersects(self, other):
		if self.y2 < other.y1 or self.x2 < other.x1:
			return False
		if self.x1 > other.x2 or self.y1 > other.y2:
			return False
		return True

	def __str__(self):
		return str(self.x1) + ',' + str(self.y1) + ',' + str(self.x2) + ',' + str(self.y2)