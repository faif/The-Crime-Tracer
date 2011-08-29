import unittest, pickle
from Vector2D import Vector2D


class Vector2DUnitTests(unittest.TestCase):

	def setUp(self):
		pass

	def testCreationAndAccess(self):
		v = Vector2D(111, 222)
		self.assert_(v.x == 111 and v.y == 222)
		v[0], v[1] = 333, 444
		self.assert_(v[0] == 333 and v[1] == 444)

	def testMath(self):
		v = Vector2D(111, 222)
		self.assertEqual(v + 1, Vector2D(112, 223))
		self.assert_(v - 2 == [109, 220])
		self.assert_(v * 3 == (333, 666))
		self.assert_(v / 2.0 == Vector2D(55.5, 111))
		self.assert_(v / 2 == (55, 111))
		self.assert_(v ** Vector2D(2, 3) == [12321, 10941048])
		self.assert_(v + [-11, 78] == Vector2D(100, 300))
		self.assert_(v / [11, 2] == [10, 111])

	def testReverseMath(self):
		v = Vector2D(111, 222)
		self.assert_(1 + v == Vector2D(112, 223))
		self.assert_(2 - v == [-109, -220])
		self.assert_(3 * v == (333, 666))
		self.assert_([222, 888] / v == [2, 4])
		self.assert_([111, 222] ** Vector2D(2, 3) == [12321, 10941048])
		self.assert_([-11, 78] + v == Vector2D(100, 300))

	def testUnary(self):
		v = Vector2D(111, 222)
		v = -v
		self.assert_(v == [-111, -222])
		v = abs(v)
		self.assert_(v == [111, 222])

	def testLength(self):
		v = Vector2D(3, 4)
		self.assert_(v.length == 5)
		self.assert_(v.get_length_sqrd() == 25)
		self.assert_(v.normalize_return_length() == 5)
		self.assert_(v.length == 1)
		v.length = 5
		self.assert_(v == Vector2D(3, 4))
		v2 = Vector2D(10, -2)
		self.assert_(v.get_distance(v2) == (v - v2).get_length())

	def testAngles(self):
		v = Vector2D(0, 3)
		self.assertEquals(v.angle, 90)
		v2 = Vector2D(v)
		v.rotate(-90)
		self.assertEqual(v.get_angle_between(v2), 90)
		v2.angle -= 90
		self.assertEqual(v.length, v2.length)
		self.assertEquals(v2.angle, 0)
		self.assertEqual(v2, [3, 0])
		self.assert_((v - v2).length < .00001)
		self.assertEqual(v.length, v2.length)
		v2.rotate(300)
		self.assertAlmostEquals(v.get_angle_between(v2), -60)
		v2.rotate(v2.get_angle_between(v))
		angle = v.get_angle_between(v2)
		self.assertAlmostEquals(v.get_angle_between(v2), 0)

	def testHighLevel(self):
		basis0 = Vector2D(5.0, 0)
		basis1 = Vector2D(0, .5)
		v = Vector2D(10, 1)
		self.assert_(v.convert_to_basis(basis0, basis1) == [2, 2])
		self.assert_(v.projection(basis0) == (10, 0))
		self.assert_(basis0.dot(basis1) == 0)

	def testCross(self):
		lhs = Vector2D(1, .5)
		rhs = Vector2D(4, 6)
		self.assert_(lhs.cross(rhs) == 4)

	def testComparison(self):
		int_vec = Vector2D(3, -2)
		flt_vec = Vector2D(3.0, -2.0)
		zero_vec = Vector2D(0, 0)
		self.assert_(int_vec == flt_vec)
		self.assert_(int_vec != zero_vec)
		self.assert_((flt_vec == zero_vec) == False)
		self.assert_((flt_vec != int_vec) == False)
		self.assert_(int_vec == (3, -2))
		self.assert_(int_vec != [0, 0])
		self.assert_(int_vec != 5)
		self.assert_(int_vec != [3, -2, -5])

	def testInplace(self):
		inplace_vec = Vector2D(5, 13)
		inplace_ref = inplace_vec
		inplace_src = Vector2D(inplace_vec)
		inplace_vec *= .5
		inplace_vec += .5
		inplace_vec /= (3, 6)
		inplace_vec += Vector2D(-1, -1)
		alternate = (inplace_src * 0.5 + 0.5) / Vector2D(3, 6) + [-1, -1]
		self.assertEquals(inplace_vec, inplace_ref)
		self.assertEquals(inplace_vec, alternate)

	def testPickle(self):
		testvec = Vector2D(5, .3)
		testvec_str = pickle.dumps(testvec)
		loaded_vec = pickle.loads(testvec_str)
		self.assertEquals(testvec, loaded_vec)


if __name__ == "__main__":
	unittest.main()
