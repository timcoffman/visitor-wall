import math ;

class VecSpace:
	def __init__(self):
		self.pts = []
	def vec2(self, x, y):
		v = Vec2(x,y)
		self.pts.append(v)
		return v
	def translate(self, dx, dy):
		for pt in self.pts:
			pt.translate(dx,dy)
		return self
	def rotate(self, radians):
		for pt in self.pts:
			pt.rotate(radians)
		return self
	def scale(self, mx, my=None):
		if my is None:
			my = mx
		for pt in self.pts:
			pt.scale(mx,my)
		return self
	def extents(self):
		min_x = min(pt.x for pt in self.pts)
		min_y = min(pt.y for pt in self.pts)
		max_x = max(pt.x for pt in self.pts)
		max_y = max(pt.y for pt in self.pts)
		return ( Vec2(min_x, min_y), Vec2(max_x,max_y) )
	def fit(self, width, height ):
		extents = self.extents()
		(emin, emax) = extents
		actualAspect = (emax.x - emin.x) / (emax.y - emin.y)
		targetAspect = width / height
		print( f'fit: extents: min: {emin}' )
		print( f'fit: extents: max: {emax}' )
		print( f'fit: aspect: actual: {actualAspect}' )
		print( f'fit: aspect: target: {targetAspect}' )
		scale = 1.0
		if targetAspect > actualAspect:
			scale = height / (emax.y - emin.y)
			print( f'fit: height: scale: {scale}' )
		else:
			scale = width / (emax.x - emin.x)
			print( f'fit: width: scale: {scale}' )
		self.translate( - (emax.x-emin.x)/2, - (emax.y-emin.y)/2 )
		self.scale( scale )
		self.translate( width/2.0, height/2.0 )
		print( f'fit: post: extents: max: {self.extents()[0]}' )
		print( f'fit: post: extents: min: {self.extents()[1]}' )

class Vec2:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def copy(self):
		return Vec2(self.x,self.y)
	def rotate(self, radians):
		c = math.cos(radians)
		s = math.sin(radians)
		x = self.x * c - self.y * s
		y = self.x * s + self.y * c
		self.x = x
		self.y = y
		return self
	def translate(self, dx, dy):
		self.x = self.x + dx
		self.y = self.y + dy
		return self
	def scale(self, mx, my=None):
		if my is None:
			my = mx
		self.x = self.x * mx
		self.y = self.y * my
		return self
	def __str__(self):
		return f'{self.x:.2f} {self.y:.2f}'
	def __getitem__(self, key):
		if key == 0:
			return self.x
		elif key == 1:
			return self.y
		else:
			raise IndexError( f'Vec2 only supports keys "0" and "1" but encountered "{key}"')

	def __setitem__(self, key, value):
		if key == 0:
			self.x = value
		elif key == 1:
			self.y = value
		else:
			raise IndexError( f'Vec2 only supports keys "0" and "1" but encountered "{key}"')
