"""
defines a class for layout generation
"""

class Plot:
	def __init__(self, pathname, desc):
		self.pathname = pathname
		self.desc = desc
		self.me = "{'path':'%s', 'description':\"\"\"%s\"\"\"}" % (self.pathname,
			self.desc)

	def __str__(self):
		return self.me

	def __repr__(self):
		return self.me

class Layout:
	def __init__(self, name, base, lplots):
		""" lplots = list of lists of plots """
		self.name = name
		self.base = base
		self.me = "%s(dqmitems, '%s'" % (self.base, self.name)
		for p in lplots:
			self.me += ", "+str(p)
		self.me += ")"

	def __str__(self):
		return self.me

	def __repr__(self):
		return self.me

class Group:
	def __init__(self, name, mute, **wargs):
		#	initialize based on which tokens to group
		self.name = name
		self.tokens = {"hasher":0, "var":0, "task":0}
		for key in wargs.keys():
			if key not in self.tokens.keys():
				raise NameError
			self.tokens[key] = wargs[key]
		self.l = []
		self.mute = mute # mute for shifter layouts
	
	def add(self, p):
		""" either adds or discards """
		self.l.append(p)

	def empty(self):
		return len(self.l)==0

	def group(self, n, m):
		ll = []
		for i in range(n):
			l = []
			for j in range(m):
				lid = i*m+j
				if lid>=len(self.l):
					continue
				else:
					l.append(self.l[lid])
			ll.append(l)
		return ll

	def dump(self):
		""" return a list of of lists of plots """
		n = len(self.l)
		import math
		m = int(math.floor(math.sqrt(float(n))))
		if m*m==n:
			return self.group(m,m)
		elif m*(m+1)<n:
			return self.group(m+1,m+1)
		else:
			return self.group(m, m+1)

	def include(self, detail):
		if not detail and self.mute:
			return False
		else:
			return True

if __name__=="__main__":
	p1 = Plot("PATH1", "DESCRIPTION1")
	p2 = Plot("PATH2", "DESCRIPTION2")

	l = Layout("LAYOUT1", "hcallayout", [p1, p2])
	print l
