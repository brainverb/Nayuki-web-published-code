# 
# Primitive recursive functions
# Copyright (c) 2012 Nayuki Minase
# 


# ---- Classes for primitive recursive functions ----

# Abstract base class of all primitive recursive functions.
# All subclasses should be designed to be immutable.
class PrimRecFunc(object):
	
	# xs is an array of integers.
	def eval(self, xs):
		raise NotImplementedError()
	
	def __str__(self):
		raise NotImplementedError()


# Zero function: Z(x) = 0
class _Z(PrimRecFunc):  # Private class
	
	def eval(self, xs):
		assert len(xs) == 1
		assert xs[0] >= 0
		return 0
	
	def __str__(self):
		return "Z"

Z = _Z()  # Public singleton instance


# Successor function: S(x) = x + 1
class _S(PrimRecFunc):  # Private class
	
	def eval(self, xs):
		assert len(xs) == 1
		assert xs[0] >= 0
		return xs[0] + 1
	
	def __str__(self):
		return "S"

S = _S()  # Public singleton instance


# Projection function: I_{n,i}(x_0, ..., x_{n-1}) = x_i
class I(PrimRecFunc):
	
	# Integer n is the arity of the function, with n > 0. Integer i is the index to take.
	def __init__(self, n, i):
		assert n > 0 and 0 <= i < n
		self.n = n
		self.i = i
	
	def eval(self, xs):
		assert len(xs) == self.n
		for x in xs:
			assert x >= 0
		return xs[self.i]
	
	def __str__(self):
		return "I({},{})".format(self.n, self.i)


# Composition function: C_{f, g_0, ..., g_{k-1}}(xs) = f(g_0(xs), ..., g_{k-1}(xs))
class C(PrimRecFunc):
	
	# f is a PrimRecFunc, and gs is an array of PrimRecFunc.
	def __init__(self, f, gs):
		self.f  = f
		self.gs = gs
	
	def eval(self, xs):
		return self.f.eval([g.eval(xs) for g in self.gs])
	
	def __str__(self):
		return "C({}, [{}])".format(str(self.f), ", ".join([str(g) for g in self.gs]))


# Primitive recursion: R_{f,g}(y, xs) = if (y == 0) then (f xs) else g(R_{f,g}(y-1, xs), y-1, xs)
class R(PrimRecFunc):
	
	# f and g each is a PrimRecFunc.
	def __init__(self, f, g):
		self.f = f
		self.g = g
	
	def eval(self, xs):
		assert len(xs) >= 2
		y = xs[0]
		if y == 0:
			return self.f.eval(xs[1:])
		else:
			return self.g.eval([self.eval([y-1] + xs[1:])] + [y-1] + xs[1:])
	
	def __str__(self):
		return "R({}, {})".format(str(self.f), str(self.g))


# Native function implementation
class Native(PrimRecFunc):
	
	# f is a function that takes an array of integers and returns an integer.
	def __init__(self, f):
		self.f = f
	
	def eval(self, xs):
		return self.f(xs)
	
	def __str__(self):
		return "Native"



# ---- Library of primitive recursive functions ----

# The ordering is unnatural (especially compared to the Haskell function) because some functions depend on others, and the dependency must be at the top.

# -- Early functions --

# Constant: const_{n}(x) = n
# This is actually a PRF generator
def const(n):
	assert n >= 0
	if n == 0:
		return Z
	else:
		return C(S, [const(n - 1)])

# Is zero: z(x, y) = if x == 0 then 1 else 0
z = C(R(const(1), C(Z, [I(3,0)])), [I(1,0), Z])

# Multiplex/select: mux(x, y, z) = if x == True then y else z. (x is Boolean; y and z are numbers)
mux = R(I(2,1), I(4,2))


# -- Boolean functions --
# 0 means false, 1 means true, and all other values cause unspecified behavior

# Negation (NOT): prnot(x)
prnot = z

# Conjunction (AND): prand(x, y)
prand = R(Z, I(3,2))

# Disjunction (OR): pror(x, y)
pror = R(I(1,0), C(S, [I(3,1)]))

# Exclusive OR (XOR): prxor(x, y)
prxor = R(I(1,0), C(prnot, [I(3,2)]))


# -- Arithmetic functions --

# Predecessor: pred(0) = 0; pred(x) = x - 1
pred = C(R(Z, I(3,1)), [I(1,0), Z])

# Addition/sum: add(x, y) = x + y
add = R(I(1,0), C(S, [I(3,0)]))

# Reverse subtraction: subrev(x, y) = max(y - x, 0)
subrev = R(I(1,0), C(pred, [I(3,0)]))

# Subtraction/difference: sub(x, y) = max(x - y, 0)
sub = C(subrev, [I(2,1), I(2,0)])

# Absolute difference: diff(x, y) = abs(x - y)
diff = C(add, [sub, subrev])

# Minimum: min(x, y) = if x <= y then x else y
min = C(subrev, [subrev, I(2,1)])

# Maximum: max(x, y) = if x >= y then x else y
max = C(add, [subrev, I(2,0)])

# Multiplication/product: mul(x, y) = x * y
mul = R(Z, C(add, [I(3,0), I(3,2)]))

# Power/exponentiation: exp(x, y) = x ^ y
exp = C(R(const(1), C(mul, [I(3,2), I(3,0)])), [I(2,1), I(2,0)])

# Factorial: factorial(x) = x!
factorial = C(R(const(1), C(mul, [C(S, [I(3,1)]), I(3,0)])), [I(1,0), Z])


# -- Comparison functions --
# Every function returns only Boolean values, i.e. 0 or 1

# Is nonzero: nz(x, y) = if x == 0 then 0 else 1
nz = C(R(Z, C(const(1), [I(3,0)])), [I(1,0), Z])

# Equal: eq(x, y) = if x == y then 1 else 0
eq = C(z, [diff])

# Not equal: neq(x, y) = if x != y then 1 else 0
neq = C(nz, [diff])

# Less than: lt(x, y) = if x < y then 1 else 0
lt = C(nz, [subrev])

# Less than or equal: le(x, y) = if x <= y then 1 else 0
le = C(z, [sub])

# Greater than: gt(x, y) = if x > y then 1 else 0
gt = C(nz, [sub])

# Greater than or equal: ge(x, y) = if x >= y then 1 else 0
ge = C(z, [subrev])


# -- Late functions --

# Is even: even(x) = if x mod 2 == 0 then 1 else 0
even = C(R(const(1), C(prnot, [I(3,0)])), [I(1,0), Z])

# Modulo: mod(x, y) = if y != 0 then (x mod y) else x
mod = C(R(I(2,0), C(mux, [C(ge, [I(4,0), I(4,3)]), C(sub, [I(4,0), I(4,3)]), I(4,0)])), [I(2,0), I(2,0), I(2,1)])

# Truncating division: div(x, y) = if y != 0 then floor(x / y) else x
div = C(R(C(Z, [I(2,0)]), C(mux, [C(le, [C(mul, [C(S, [I(4,0)]), I(4,3)]), I(4,2)]), C(S, [I(4,0)]), I(4,0)])), [I(2,0), I(2,0), I(2,1)])

# Is divisible: divisible(x, y) = if (y > 0 and x mod y == 0) or x == 0 then 1 else 0
divisible = C(z, [mod])

# Is prime: prime(x) = if x is prime then 1 else 0
prime = C(eq, [C(R(Z, C(add, [C(divisible, [I(3,2), I(3,1)]), I(3,0)])), [I(1,0), I(1,0)]), const(1)])
