# 
# Binary array set (Python)
# 
# Copyright (c) 2014 Project Nayuki
# http://www.nayuki.io/page/binary-array-set
# 
# (MIT License)
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# - The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# - The Software is provided "as is", without warranty of any kind, express or
#   implied, including but not limited to the warranties of merchantability,
#   fitness for a particular purpose and noninfringement. In no event shall the
#   authors or copyright holders be liable for any claim, damages or other
#   liability, whether in an action of contract, tort or otherwise, arising from,
#   out of or in connection with the Software or the use or other dealings in the
#   Software.
# 

import sys
if sys.version_info.major == 2:
	range = xrange


class BinaryArraySet(object):
	
	# Runs in O(1) time
	# For each i, self.values[i] is either None or it's an ascending-sorted array of length 2^i
	def __init__(self):
		self.clear()
	
	
	# Runs in O(1) time
	def __len__(self):
		return self.length
	
	
	# Runs in O(1) time
	def clear(self):
		self.values = []
		self.length = 0
	
	
	def __iter__(self):
		return BinaryArraySet.Iter(self)
	
	
	# Runs in O((log n)^2) time
	def __contains__(self, val):
		for vals in self.values:
			if vals is not None:
				# Binary search
				start = 0
				end = len(vals)
				while start < end:
					mid = (start + end) // 2
					midval = vals[mid]
					if val < midval:
						end = mid
					elif val > midval:
						start = mid + 1
					elif val == midval:
						return True
					else:
						raise AssertionError()
		return False
	
	
	# Runs in average-case O((log n)^2) time, worst-case O(n) time
	def add(self, val):
		# Checking for duplicates is expensive, taking O((log n)^2) time
		if val in self:
			return
		
		# The pure add portion below runs in amortized O(1) time
		toput = [val]
		for (i, vals) in enumerate(self.values):
			assert len(toput) == 1 << i
			if vals is None:
				self.values[i] = toput
				toput = None
				break
			else:
				# Merge two sorted arrays
				assert len(vals) == 1 << i
				next = []
				j = 0
				k = 0
				while j < len(vals) and k < len(toput):
					if vals[j] < toput[k]:
						next.append(vals[j])
						j += 1
					else:
						next.append(toput[k])
						k += 1
				next.extend(vals [j : ])
				next.extend(toput[k : ])
				assert len(next) == 2 << i
				toput = next
				self.values[i] = None
		if toput is not None:
			self.values.append(toput)
		self.length += 1
	
	
	# For unit tests
	def check_structure(self):
		if self.length < 0:
			raise AssertionError()
		
		sum = 0
		for (i, vals) in enumerate(self.values):
			if vals is not None:
				if len(vals) != 1 << i:
					raise AssertionError()
				sum += len(vals)
				for j in range(1, len(vals)):
					if vals[j - 1] >= vals[j]:
						raise AssertionError()
		if sum != self.length:
			raise AssertionError()
	
	
	
	# Not fail-fast on concurrent modification
	class Iter(object):
		
		# Constructor runs in O(log n) time
		def __init__(self, outer):
			self.values = outer.values
			self.index = 0
			while self.index < len(self.values) and self.values[self.index] is None:
				self.index += 1
			self.subindex = 0
		
		
		# Runs in amortized O(1) time, worst-case O(log n) time
		def __next__(self):  # Python 3
			if self.index >= len(self.values):
				raise StopIteration
			else:
				result = self.values[self.index][self.subindex]
				self.subindex += 1
				if self.subindex == len(self.values[self.index]):
					self.subindex = 0
					self.index += 1
					while self.index < len(self.values) and self.values[self.index] is None:
						self.index += 1
				return result
		
		next = __next__  # Python 2
