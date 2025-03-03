import doctest
import math
import pickle
import random
import sys
import unittest
import verifyutils

# FIXME:  why is this required?
import pkg_resources


#
# mock import statement to correctly load python implemention
#


try:
	import builtins
except ImportError:
	import __builtin__ as builtins
else:
	from importlib import reload

realimport = builtins.__import__


def no_c_library(name, globals = None, locals=None, fromlist = (), level = 0):
	if name == '__segments':  # refuse to load C segments library
		raise ImportError
	return realimport(
		name,
		globals = globals,
		locals = locals,
		fromlist = fromlist,
		level = level
	)


#
#  How many times to repeat the algebraic tests
#


algebra_repeats = 8000
algebra_listlength = 200


#
# Some useful code.
#


def set1():
	return (
		segments.segment(-2, 2),
		segments.segment(-2, 2),
		segments.segment(-2, 2),
		segments.segment(-2, 2),
		segments.segment(-2, 2),
		segments.segment(-2, 2),
		segments.segment(-2, 2),
		segments.segment(-2, 2),
		segments.segment(-2, 2),
		segments.segment(-2, 2),
		segments.segment(-2, 2),
		segments.segment(-2, 2),
		segments.segment(-2, 2),
		segments.segment(-2, 2)
	)


def set2():
	return (
		segments.segment(-4, -3),
		segments.segment(-4, -2),
		segments.segment(-4,  0),
		segments.segment(-4,  2),
		segments.segment(-4,  4),
		segments.segment(-2,  4),
		segments.segment( 0,  4),
		segments.segment( 2,  4),
		segments.segment( 3,  4),
		segments.segment(-2,  2),
		segments.segment(-1,  1),
		segments.segment(-segments.infinity(), segments.infinity()),
		segments.segment(0, segments.infinity()),
		segments.segment(-segments.infinity(), 0)
	)


#
# Define the components of the test suite.
#


class test_infinity(unittest.TestCase):
	def test_math(self):
		a = segments.infinity()
		self.assertEqual(-a, -a)
		self.assertLess(-a, 0)
		self.assertLess(-a, a)
		self.assertGreater(0, -a)
		self.assertLess(0, a)
		self.assertGreater(a, -a)
		self.assertGreater(a, 0)
		self.assertEqual(a, a)

	def test__cmp__(self):
		try:
			cmp()
		except NameError:
			# Python 3 does not have cmp() builtin
			def cmp(a, b):
				return (a > b) - (a < b)
		a = segments.infinity()
		self.assertEqual( 0, cmp(-a, -a))
		self.assertEqual(-1, cmp(-a,  0))
		self.assertEqual(-1, cmp(-a,  a))
		self.assertEqual( 1, cmp( 0, -a))
		self.assertEqual(-1, cmp( 0,  a))
		self.assertEqual( 1, cmp( a, -a))
		self.assertEqual( 1, cmp( a,  0))
		self.assertEqual( 0, cmp( a,  a))

	def test__add__(self):
		a = segments.infinity()
		b = segments.infinity()
		self.assertEqual( b, (  a) + ( 10))
		self.assertEqual( b, (  a) + (-10))
		self.assertEqual(-b, ( -a) + ( 10))
		self.assertEqual(-b, ( -a) + (-10))
		self.assertEqual( b, ( 10) + (  a))
		self.assertEqual( b, (-10) + (  a))
		self.assertEqual(-b, ( 10) + ( -a))
		self.assertEqual(-b, (-10) + ( -a))
		self.assertEqual( b, (  a) + (  a))
		self.assertEqual(-b, ( -a) + ( -a))

	def test__sub__(self):
		a = segments.infinity()
		b = segments.infinity()
		self.assertEqual( b, (  a) - ( 10))
		self.assertEqual( b, (  a) - (-10))
		self.assertEqual(-b, ( -a) - ( 10))
		self.assertEqual(-b, ( -a) - (-10))
		self.assertEqual(-b, ( 10) - (  a))
		self.assertEqual(-b, (-10) - (  a))
		self.assertEqual( b, ( 10) - ( -a))
		self.assertEqual( b, (-10) - ( -a))
		self.assertEqual( b, (  a) - (  a))
		self.assertEqual(-b, ( -a) - ( -a))
		self.assertEqual( b, (  a) - ( -a))
		self.assertEqual(-b, ( -a) - (  a))

	def test__float__(self):
		a = segments.infinity()
		b = -segments.infinity()
		self.assertTrue(math.isinf(a))
		self.assertTrue(math.isinf(b))


class test_segment(unittest.TestCase):
	def test__new__(self):
		self.assertEqual((-2, 2), tuple(segments.segment(-2, 2)))
		self.assertEqual((-2, 2), tuple(segments.segment(2, -2)))
		self.assertEqual((-segments.infinity(), 2), tuple(segments.segment(-segments.infinity(), 2)))
		self.assertEqual((-segments.infinity(), 2), tuple(segments.segment(2, -segments.infinity())))
		self.assertEqual((2, segments.infinity()), tuple(segments.segment(segments.infinity(), 2)))
		self.assertEqual((2, segments.infinity()), tuple(segments.segment(2, segments.infinity())))
		self.assertEqual((-segments.infinity(), segments.infinity()), tuple(segments.segment(-segments.infinity(), segments.infinity())))

	def test__abs__(self):
		results = (
			1,
			2,
			4,
			6,
			8,
			6,
			4,
			2,
			1,
			4,
			2,
			segments.infinity(),
			segments.infinity(),
			segments.infinity()
		)
		list(map(lambda i, r, a: self.assertEqual((i, r), (i, abs(a))), range(len(results)), results, set2()))

	def testintersects(self):
		results = (
			False,
			False,
			True,
			True,
			True,
			True,
			True,
			False,
			False,
			True,
			True,
			True,
			True,
			True
		)
		list(map(lambda i, r, a, b: self.assertEqual((i, r), (i, a.intersects(b))), range(len(results)), results, set1(), set2()))

	def testconnects(self):
		results = (
			False,
			True,
			False,
			False,
			False,
			False,
			False,
			True,
			False,
			False,
			False,
			False,
			False,
			False
		)
		list(map(lambda i, r, a, b: self.assertEqual((i, r), (i, a.connects(b))), range(len(results)), results, set1(), set2()))

	def test__contains__(self):
		results = (
			False,
			False,
			False,
			False,
			False,
			False,
			False,
			False,
			False,
			True,
			True,
			False,
			False,
			False
		)
		list(map(lambda i, r, a, b: self.assertEqual((i, r), (i, a.__contains__(b))), range(len(results)), results, set1(), set2()))
		self.assertEqual(True, [1, 2] in segments.segment(0, 4))
		self.assertEqual(False, [1, 6] in segments.segment(0, 4))
		self.assertEqual(False, [-1, 2] in segments.segment(0, 4))
		self.assertEqual(False, [-1, 6] in segments.segment(0, 4))
		self.assertEqual(True, 2 in segments.segment(0, 4))

		# Paraphrasing the documentation for
		# glue.segment.__contains__ in ligo/segments.py: if a is a
		# segment or a sequence of length two, then `a in b` tests
		# if `b[0] <= a[0] <= a[1] <= b[1]`. Otherwise, `a in b`
		# tests if `b[0] <= a <= b[1]`. The following four tests
		# happen to work and return False in Python 2, but they
		# raise a TypeError in Python 3 because Python does not
		# permit comparisons of numbers with sequences. The
		# exception message is "'<' not supported between instances
		# of 'list' and 'int'".

		if sys.version_info.major <= 2:
			self.assertEqual(False, [] in segments.segment(0, 4))
			self.assertEqual(False, [0] in segments.segment(0, 4))
			self.assertEqual(False, [2] in segments.segment(0, 4))
			self.assertEqual(False, [1, 2, 3] in segments.segment(0, 4))
		else:
			with self.assertRaises(TypeError):
				self.assertEqual(False, [] in segments.segment(0, 4))
			with self.assertRaises(TypeError):
				self.assertEqual(False, [0] in segments.segment(0, 4))
			with self.assertRaises(TypeError):
				self.assertEqual(False, [2] in segments.segment(0, 4))
			with self.assertRaises(TypeError):
				self.assertEqual(False, [1, 2, 3] in segments.segment(0, 4))

	def testdisjoint(self):
		results = (
			+1,
			0,
			0,
			0,
			0,
			0,
			0,
			0,
			-1,
			0,
			0,
			0,
			0,
			0
		)
		list(map(lambda i, r, a, b: self.assertEqual((i, r), (i, a.disjoint(b))), range(len(results)), results, set1(), set2()))

	def testcontract(self):
		results = (
			segments.segment(-5, -2),
			segments.segment(-4, -2),
			segments.segment(-2, -2),
			segments.segment(-2,  0),
			segments.segment(-2,  2),
			segments.segment( 0,  2),
			segments.segment( 2,  2),
			segments.segment( 2,  4),
			segments.segment( 2,  5),
			segments.segment( 0,  0),
			segments.segment(-1,  1),
			segments.segment(-segments.infinity(), segments.infinity()),
			segments.segment(2, segments.infinity()),
			segments.segment(-segments.infinity(), -2)
		)
		list(map(lambda i, r, a: self.assertEqual((i, r), (i, a.contract(2))), range(len(results)), results, set2()))

	def test_typesafety(self):
		x = "segments.segment(10, 20)"
		y = "(20, 30)"
		z = "None"

		for op in ("|", "&", "-", "^"):
			for arg1, arg2 in (
				(x, z), (z, x)
			):
				expr = "%s %s %s" % (arg1, op, arg2)
				try:
					eval(expr)
				except TypeError:
					pass
				else:
					raise AssertionError("%s did not raise TypeError" % expr)
		# FIXME:  this doesn't work, should it?
		#self.assertEqual(eval("%s | %s" % (x, y)), segments.segmentlist([segments.segment(10, 30)]))


class test_segmentlist(unittest.TestCase):
	def test__sub__(self):
		self.assertEqual(segments.segmentlist([]), segments.segmentlist([]) - segments.segmentlist([]))
		self.assertEqual(segments.segmentlist([]), segments.segmentlist([]) - segments.segmentlist([segments.segment(-1,1)]))
		self.assertEqual(segments.segmentlist([segments.segment(-1,1)]) - segments.segmentlist([segments.segment(-1,1)]), segments.segmentlist([]))
		self.assertEqual(segments.segmentlist([]), segments.segmentlist([segments.segment(-1,1)]) - segments.segmentlist([segments.segment(-1,1)]))
		# This next test fails, but I don't know that that's not OK yet
		#self.assertEqual(segments.segmentlist([]), segments.segmentlist([segments.segment(0,0)]) - segments.segmentlist([segments.segment(0,0)]))

		self.assertEqual(segments.segmentlist([segments.segment(0,1)]), segments.segmentlist([segments.segment(0,1)]) - segments.segmentlist([segments.segment(2,3)]))
		self.assertEqual(segments.segmentlist([segments.segment(0,1)]), segments.segmentlist([segments.segment(0,1)]) - segments.segmentlist([segments.segment(2,3), segments.segment(4,5)]))
		self.assertEqual(segments.segmentlist([segments.segment(0,1)]), segments.segmentlist([segments.segment(0,1), segments.segment(2,3)]) - segments.segmentlist([segments.segment(2,3)]))
		self.assertEqual(segments.segmentlist([segments.segment(2,3)]), segments.segmentlist([segments.segment(0,1), segments.segment(2,3)]) - segments.segmentlist([segments.segment(0,1)]))
		self.assertEqual(segments.segmentlist([segments.segment(0,1), segments.segment(4,5)]), segments.segmentlist([segments.segment(0,1), segments.segment(2,3), segments.segment(4,5)]) - segments.segmentlist([segments.segment(2,3)]))

		self.assertEqual(segments.segmentlist([segments.segment(0,1)]), segments.segmentlist([segments.segment(0,2)]) - segments.segmentlist([segments.segment(1,2)]))
		self.assertEqual(segments.segmentlist([segments.segment(0.8, 0.9), segments.segment(1.0, 1.8)]), segments.segmentlist([segments.segment(0, 2)]) - segments.segmentlist([segments.segment(0, 0.8), segments.segment(0.9, 1.0), segments.segment(1.8, 2)]))

		self.assertEqual(segments.segmentlist([segments.segment(-5, 10)]), segments.segmentlist([segments.segment(-10,10)]) - segments.segmentlist([segments.segment(-15,-5)]))
		self.assertEqual(segments.segmentlist([segments.segment(-10, -5), segments.segment(5, 10)]), segments.segmentlist([segments.segment(-10,10)]) - segments.segmentlist([segments.segment(-5,5)]))
		self.assertEqual(segments.segmentlist([segments.segment(-10, 5)]), segments.segmentlist([segments.segment(-10,10)]) - segments.segmentlist([segments.segment(5,15)]))

		self.assertEqual(segments.segmentlist([segments.segment(0,5), segments.segment(45,50)]), segments.segmentlist([segments.segment(0,10), segments.segment(20,30), segments.segment(40,50)]) - segments.segmentlist([segments.segment(5, 45)]))

	def test__invert__(self):
		self.assertEqual(segments.segmentlist([segments.segment(-segments.infinity(), segments.infinity())]), ~segments.segmentlist([]))
		self.assertEqual(segments.segmentlist([]), ~segments.segmentlist([segments.segment(-segments.infinity(), segments.infinity())]))
		self.assertEqual(segments.segmentlist([segments.segment(-segments.infinity(), -5), segments.segment(5, segments.infinity())]), ~segments.segmentlist([segments.segment(-5,5)]))

	def test__and__(self):
		for i in range(algebra_repeats):
			a = verifyutils.random_coalesced_list(random.randint(1, algebra_listlength))
			b = verifyutils.random_coalesced_list(random.randint(1, algebra_listlength))
			c = a & b
			try:
				# make sure __and__ and __sub__ have the
				# correct relationship to one another
				self.assertEqual(c, a - (a - b))
				self.assertEqual(c, b - (b - a))
			except AssertionError as e:
				raise AssertionError(str(e) + "\na = " + str(a) + "\nb = " + str(b))

	def test__or__(self):
		for i in range(algebra_repeats):
			a = verifyutils.random_coalesced_list(random.randint(1, algebra_listlength))
			b = verifyutils.random_coalesced_list(random.randint(1, algebra_listlength))
			c = a | b
			try:
				# make sure c is coalesced
				self.assertTrue(verifyutils.iscoalesced(c))
				# make sure c contains all of a
				self.assertEqual(a, c & a)
				# make sure c contains all of b
				self.assertEqual(b, c & b)
				# make sure c contains nothing except a and b
				self.assertEqual(segments.segmentlist([]), c - a - b)
			except AssertionError as e:
				raise AssertionError(str(e) + "\na = " + str(a) + "\nb = " + str(b))

	def test__xor__(self):
		for i in range(algebra_repeats):
			a = verifyutils.random_coalesced_list(random.randint(1, algebra_listlength))
			b = verifyutils.random_coalesced_list(random.randint(1, algebra_listlength))
			c = a ^ b
			try:
				# c contains nothing that can be found in
				# the intersection of a and b
				self.assertFalse(c.intersects(a & b))
				# c contains nothing that cannot be found
				# in either a or b
				self.assertEqual(segments.segmentlist([]), c - a - b)
				# that c + the intersection of a and b
				# leaves no part of either a or b
				# unconvered
				self.assertEqual(segments.segmentlist([]), a - (c | a & b))
				self.assertEqual(segments.segmentlist([]), b - (c | a & b))
			except AssertionError as e:
				raise AssertionError(str(e) + "\na = " + str(a) + "\nb = " + str(b))

	def testprotract(self):
		self.assertEqual(segments.segmentlist([segments.segment(0, 20)]), segments.segmentlist([segments.segment(3, 7), segments.segment(13, 17)]).protract(3))

		# confirm that .protract() preserves the type of the
		# segment objects
		class MyCustomSegment(segments.segment):
			pass
		class MyCustomSegmentList(segments.segmentlist):
			def coalesce(self):
				# must override for test, but don't have to
				# implement because test case is too simple
				return self
		self.assertEqual(type(MyCustomSegmentList([MyCustomSegment(0, 10)]).protract(1)[0] ), MyCustomSegment)

	def testcontract(self):
		self.assertEqual(segments.segmentlist([segments.segment(0, 20)]), segments.segmentlist([segments.segment(3, 7), segments.segment(13, 17)]).contract(-3))

		# confirm that .contract() preserves the type of the
		# segment objects
		class MyCustomSegment(segments.segment):
			pass
		class MyCustomSegmentList(segments.segmentlist):
			def coalesce(self):
				# must override for test, but don't have to
				# implement because test case is too simple
				return self
		self.assertEqual(type(MyCustomSegmentList([MyCustomSegment(0, 10)]).contract(1)[0] ), MyCustomSegment)

	def testintersects(self):
		for i in range(algebra_repeats):
			a = verifyutils.random_coalesced_list(random.randint(1, algebra_listlength))
			b = verifyutils.random_coalesced_list(random.randint(1, algebra_listlength))
			c = a - b
			d = a & b
			try:
				if len(c):
					self.assertFalse(c.intersects(b))
				if len(d):
					self.assertTrue(d.intersects(a))
					self.assertTrue(d.intersects(b))
					self.assertTrue(a.intersects(b))
			except AssertionError as e:
				raise AssertionError(str(e) + "\na = " + str(a) + "\nb = " + str(b))

	def testextent(self):
		self.assertEqual(segments.segmentlist([(1, 0)]).extent(), segments.segment(0, 1))

	def testcoalesce(self):
		# check that mixed-type coalescing works
		x = segments.segmentlist([segments.segment(1, 2), segments.segment(3, 4), (2, 3)])
		try:
			self.assertEqual(x.coalesce(), segments.segmentlist([segments.segment(1, 4)]))
		except AssertionError as e:
			raise AssertionError("mixed type coalesce failed:  got %s" % str(x))

		# try a bunch of random segment lists
		for i in range(algebra_repeats):
			a = verifyutils.random_uncoalesced_list(random.randint(1, algebra_listlength))
			b = segments.segmentlist(a[:]).coalesce()
			try:
				self.assertTrue(verifyutils.iscoalesced(b))
				for seg in a:
					self.assertTrue(seg in b)
				for seg in a:
					b -= segments.segmentlist([seg])
				self.assertEqual(b, segments.segmentlist([]))
			except AssertionError as e:
				raise AssertionError(str(e) + "\na = " + str(a) + "\nb = " + str(b))

	def test_typesafety(self):
		w = "segments.segmentlist([segments.segment(0, 10), segments.segment(20, 30)])"
		x = "segments.segment(10, 20)"
		y = "[(10, 20)]"
		z = "None"

		for op in ("|", "&", "-", "^"):
			for arg1, arg2 in (
				# FIXME:  how should these behave?
				#(w, x), (x, w),
				(w, z), (z, w)
			):
				expr = "%s %s %s" % (arg1, op, arg2)
				try:
					eval(expr)
				except TypeError:
					pass
				else:
					raise AssertionError("%s did not raise TypeError" % expr)
		self.assertEqual(eval("%s | %s" % (w, y)), segments.segmentlist([segments.segment(0, 30)]))

class test_segmentlistdict(unittest.TestCase):
	@staticmethod
	def random_coalesced_segmentlistdict(n):
		seglists = segments.segmentlistdict()
		for key in map(chr, range(65, 65 + n)):
			seglists[key] = verifyutils.random_coalesced_list(random.randint(1, algebra_listlength))
		return seglists

	def testextent_all(self):
		a = segments.segmentlistdict({"H1": segments.segmentlist(), "L1": segments.segmentlist([segments.segment(25, 35)])})
		self.assertEqual(a.extent_all(), segments.segment(25, 35))

	def testintersects(self):
		a = segments.segmentlistdict({"H1": segments.segmentlist([segments.segment(0, 10), segments.segment(20, 30)])})
		b = segments.segmentlistdict({"H1": segments.segmentlist([segments.segment(5, 15)]), "L1": segments.segmentlist([segments.segment(25, 35)])})
		c = segments.segmentlistdict({"V1": segments.segmentlist([segments.segment(7, 13), segments.segment(27, 40)])})

		self.assertEqual(a.intersects(b), True)
		self.assertEqual(b.intersects(a), True)
		self.assertEqual(a.intersects(a), True)
		self.assertEqual(a.intersects(c), False)
		self.assertEqual(b.intersects(segments.segmentlistdict({})), False)
		self.assertEqual(segments.segmentlistdict({}).intersects(segments.segmentlistdict({})), False)

		self.assertEqual(a.intersects_all(b), False)
		self.assertEqual(b.intersects_all(a), True)

		self.assertEqual(a.all_intersects(b), True)
		self.assertEqual(b.all_intersects(a), False)

		self.assertEqual(a.all_intersects_all(b), False)

	def testpickle(self):
		a = segments.segmentlistdict({"H1": segments.segmentlist([segments.segment(0, 10), segments.segment(20, 30)])})
		a.offsets["H1"] = 10.0
		self.assertEqual(a, pickle.loads(pickle.dumps(a, protocol = 0)))
		self.assertEqual(a, pickle.loads(pickle.dumps(a, protocol = 1)))
		self.assertEqual(a, pickle.loads(pickle.dumps(a, protocol = 2)))

	def testvote(self):
		seglists = self.random_coalesced_segmentlistdict(15)
		seglists.vote(seglists, 6)

	def testintersection(self):
		seglists = self.random_coalesced_segmentlistdict(15)
		keys = ("A", "B", "C", "D")
		seglists.intersection(keys)


#
# Construct and run the test suite.
#


if __name__ == "__main__":
	# first with the pure Python segments implementation

	builtins.__import__ = no_c_library  # refuse to load C library
	try:
		from ligo import segments
	finally:
		# reinstate original import
		builtins.__import__ = realimport

	print("testing segments module %r" % segments.segment.__module__)
	verifyutils.segments = segments

	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(test_infinity))
	suite.addTest(unittest.makeSuite(test_segment))
	suite.addTest(unittest.makeSuite(test_segmentlist))
	suite.addTest(unittest.makeSuite(test_segmentlistdict))

	if not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():
		sys.exit(1)

	failures = doctest.testmod(segments)[0]
	if failures:
		sys.exit(bool(failures))

	# then with C extension implementation

	reload(segments)  # loads C library and re-executes copyreg.pickle
	print("testing segments module %r" % segments.segment.__module__)

	segments.infinity = segments.infinity
	segments.NegInfinity = segments.NegInfinity
	segments.PosInfinity = segments.PosInfinity
	segments.segment = segments.segment
	segments.segmentlist = segments.segmentlist

	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(test_infinity))
	suite.addTest(unittest.makeSuite(test_segment))
	suite.addTest(unittest.makeSuite(test_segmentlist))
	suite.addTest(unittest.makeSuite(test_segmentlistdict))

	if not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():
		sys.exit(1)

	failures = doctest.testmod(segments)[0]
	if failures:
		sys.exit(bool(failures))
