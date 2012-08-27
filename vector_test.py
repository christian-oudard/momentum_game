import unittest
import math
import operator
import vector
from vector import VectorError
from vector import Point2dFloat as Point
from vector import Vector2dFloat as Vector
from vector import Coord

testvals = ((2, 4),
            (2.5, 53.342),
            (-2, -4),
            (1/3.0, 2.323423),
            (0, -3),
            (53, 0)
            )
specialvals = ((0,0),
               )

class TestConstructorPoint(unittest.TestCase):
    def test_normalinput(self):
        Point()
        Point(None)
        Point((2,4))
        Point([2.5, 53.342])
        Point(2,4)
        Point(1/3.0, 2.33333)
        for val in testvals:
            Point(val)
    
    def test_badinput(self):
        self.assertRaises(VectorError, Point, 'cheese')
        self.assertRaises(VectorError, Point, 3)
        self.assertRaises(VectorError, Point, [5])

class TestPropertiesPoint(unittest.TestCase):
    def setUp(self):
        self.p = Point()
    def test_nodelete(self):
        self.assertRaises(AttributeError, delattr, self.p, 'x')
    def test_convertfloat(self):
        self.p.x = int(5)
        self.assertEqual(type(self.p._x), float)
                
class TestOperatorsPoint(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Point((2,3))), '(2.00, 3.00)')
    def test_eq_ne(self):
        for val in testvals:
            self.assert_(Point(val) == Point(val) and
                     not Point(val) != Point(val) and
                         val == Point(val))
        self.assert_(Point(0,0) == Point(0.0, -0.0))
        self.assert_(Point(-1, 53) != Point(23, 5))
    def test_getitem_setitem(self):
        p = Point()
        p[0] = 5.0
        self.assertEqual(p.x, 5.0)
        for val in testvals:
            p = Point(val)
            self.assertEqual(p.x, p[0])
            self.assertEqual(p.y, p[1])
    def test_len(self):
        for val in testvals:
            self.assertEqual(len(Point(val)), 2)
    def test_iter(self):
        p = Point()
        for f in p:
            pass
    def test_add_sequence(self):
        self.assertEqual(Point(4, 5) + (3, -8), Point(7, -3))
    def test_sub_sequence(self):
        self.assertEqual(Point(-2, 5) - (2, -1), Point(-4, 6))
        

class TestConstructorVector(unittest.TestCase):
    def test_normalinput(self):
        Vector()
        Vector((2,4))
        Vector([2.5, 53.342])
        Vector(2,4)
        Vector(1/3.0, 2.33333)
        for val in testvals + specialvals:
            Vector(val)
    def test_badinput(self):
        self.assertRaises(VectorError, Vector, 'cheese')
        self.assertRaises(VectorError, Vector, 3)
        self.assertRaises(VectorError, Vector, [5])

class TestPropertiesVector(unittest.TestCase):
    def test_mag(self):
        v = Vector(3, -4)
        self.assertRaises(AttributeError, delattr, v, 'mag')
        self.assertEqual(v.mag, 5)
        v.mag = 10
        self.assertEqual(v, Vector(6,-8))
    def test_mag2(self):
        for val in testvals + specialvals:
            self.assertAlmostEqual(Vector(val).mag**2, Vector(val).mag2)
    def test_dir(self):
        self.assertRaises(AttributeError, delattr, Vector(), 'dir')
        self.assertRaises(VectorError, Vector().__getattribute__,'dir')
        for val in testvals:
            v = Vector(val)
            self.assertAlmostEqual(v.dir.mag, 1.0)
            self.assertEqual(v, v.dir * v.mag)
            v.dir = Vector(0,1)
            self.assertEqual(v.x, 0)
            v = Vector(val)
            v.dir = Vector(1,1).dir
            self.assertEqual(v.x, v.y)
            v = Vector(val)
            oldmag = v.mag
            v.dir = Vector(12342.235, -23523.6308).dir
            self.assertEqual(v.mag, oldmag)

    def test_theta(self):
        for val in testvals:
            a = Vector(val).theta
            self.assertEqual(vector.angle(val, (1,0)), min([a, 2*math.pi-a]))
            
class TestOperatorsVector(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Vector((2,3))), '<2.00, 3.00>')
    def test_eq_ne(self):
        for val in testvals:
            self.assert_(Vector(val) == Vector(val) and
                     not Vector(val) != Vector(val) and
                         val == Vector(val))
        self.assert_(Vector(0,0) == Vector(0.0, -0.0))
        self.assert_(Vector(-1, 53) != Vector(23, 5))
    def test_getitem_setitem(self):
        v = Vector()
        v[0] = 5.0
        self.assertEqual(v.x, 5.0)
        for val in testvals:
            v = Vector(val)
            self.assertEqual(v.x, v[0])
            self.assertEqual(v.y, v[1])
    def test_len(self):
        for val in testvals:
            self.assertEqual(len(Vector(val)), 2)
    def test_iter(self):
        v = Vector()
        for f in v:
            pass
    def test_neg(self):
        self.assertEqual(-Vector(-2, 5), Vector(2, -5))
    def test_radd(self):
        self.assertEqual(Point(1, 1) + Vector(3, 5), Point(4, 6))
        for val in testvals:
            self.assertEqual(type(val + Vector(val)), Point)
            v = Vector(val)
            v += val
            self.assertEqual(v, Vector(val) + val)
    def test_no_vector_plus_point(self):
        self.assertRaises(TypeError, operator.add, Vector(), Point())
    def test_mul(self):
        self.assertEqual(Vector(2, 3)*2, Vector(4, 6))
        v = v = Vector(5, -5)
        v *= .5
        self.assertEqual(tuple(v), (2.5, -2.5))
    def test_div(self):
        self.assertEqual(Vector(2, 3)/2, Vector(1, 1.5))
        v = v = Vector(5, -5)
        v /= .5
        self.assertEqual(tuple(v), (10, -10))

class TestMethodsVector(unittest.TestCase):
    def test_reverse(self):
        self.assertEqual(Vector(23, 53).reverse(), (-23, -53))
        v = Vector(-2, 5)
        v.reverse_ip()
        self.assertEqual(v, (2, -5))
    def test_perp(self):
        self.assertEqual(Vector(3,5).perp(), (5, -3))
        for val in testvals:
            self.assertEqual(vector.dot_prod(Vector(val).perp(), Vector(val)), 0)
    def test_project(self):
        self.assertEqual(Vector(-4,4).project((1,0)), Vector((-4, 0)))
        self.assertAlmostEqual(Vector(-3, 5).project((4,4)).mag, Vector(1,1).mag)
        self.assertAlmostEqual(Vector(-3, 5).project((-1,-1)).theta, Vector(1,1).theta)

class TestFunctions(unittest.TestCase):
    def test_dot_prod(self):
        self.assertEqual(vector.dot_prod((1,2), (3,4)), 11)
        for val in testvals:
            self.assertEqual(vector.dot_prod(val, (0,0)), 0)
    def test_angle(self):
        testangles = (((0,1), (1,0), math.pi/2),
                      ((7,-7), (1,0), math.pi/4),
                      ((2,0), (-1,0), math.pi),
                      ((1,0), (1,math.sqrt(3)), math.pi/3),
                      ((3,0), (math.sqrt(3),1), math.pi/6), 
                      ((2,2), (1,-1), math.pi/2),
                      ((5,5), (-math.sqrt(3),1), math.pi/4 + math.pi/3))
        for (v1,v2,a) in testangles:
            self.assertAlmostEqual(vector.angle(v1, v2), a)
            self.assertAlmostEqual(vector.angle(v2, v1), a) # both orders
        for val in testvals:
            self.assertEqual(vector.angle(val, Vector(val).perp()), math.pi/2) # perp makes pi/2
            self.assertEqual(vector.angle(val, val), 0) # same vector makes 0 rads
            self.assertRaises(VectorError, vector.angle, val, (0,0)) # v and (0,0) makes 0 rads

if __name__ == '__main__':
    try:
        import sys
        sys.argv.append('-v')
        unittest.main()
    except SystemExit:
        pass
