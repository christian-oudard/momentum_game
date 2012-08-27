"""vector module

This module provides 3 classes related to vectors:
Point2dFloat - a float-valued 2-dimensional point
Vector2dFloat - a float-valued 2-dimensional vector
Coord - an integer-valued coordinate point

There are also two utility functions for vectors:
dot_prod(v1, v2) - dot product of two vectors
angle(v1, v2) - angle between two vectors

Each class has operators defined so they can be used as numerical types.
The math operator overload functions distinguish between points and
vectors. For example, a point plus a vector yields a point, and two
points added together is nonsensical and not allowed. Other than that,
tuples and lists may be substituted into most operators and will be
automatically converted to the correct class. This is a convenience
measure.

"""

import math

# module constants #
_pi = math.pi
_two_pi = 2*_pi

# functions #
def dot_prod(v1, v2):
    """Return a the dot-product of two 2-D vectors."""
    return v1[0]*v2[0] + v1[1]*v2[1]

def angle(v1, v2):
    """Return the angle between two 2-D vectors.

    v1 and v2 must be castable as Vector2dFloat.
    If the magnitude of either vector is 0, a VectorError is raised.
    The return value is in radians, and is of type float.
    """
    if type(v1) != Vector2dFloat:
        v1 = Vector2dFloat(v1)
    if type(v2) != Vector2dFloat:
        v2 = Vector2dFloat(v2)
    try:
        a = math.acos(dot_prod(v1,v2) / math.sqrt(v1.mag2 * v2.mag2))
    except ZeroDivisionError:
        raise VectorError('Angle with a zero vector is undefined')
    else:
        return min([a, _two_pi-a])    


# classes #

class VectorError(Exception):
    """Exception class for errors in vector module"""
    pass


class Point2dFloat(object):

    """2-Dimensional float-valued point.
    
    This class has readable and writable properties x and y,
    corresponding to the dimensions of the point. It also can function
    as a list with 2 elements.
    """
    
    def __init__(self, *args):
        if len(args) == 0 or args[0] is None:
            self.x, self.y = (0,0)
        elif len(args) == 1:
            try:
                self.x = args[0][0]
                self.y = args[0][1]
            except IndexError:
                raise VectorError('Point2dFloat must have two dimensions.')
            except TypeError:
                raise VectorError('Point2dFloat must have two dimensions.')
            except ValueError:
                raise VectorError('Point2dFloat type must be compatible with float.')
        else:
            try:
                self.x = args[0]
                self.y = args[1]
            except ValueError:
                raise VectorError('Point2dFloat type must be compatible with float.')

    # property management functions #

    def _get_x(self):
        return self._x
    def _set_x(self, value):
        self._x = float(value)
    def _get_y(self):
        return self._y    
    def _set_y(self, value):
        self._y = float(value)

    # properties #
    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)

    # operator overloads #
    def __str__(self):
        return '(%.2f, %.2f)' % (self._x, self._y)
    def __repr__(self):
        return 'Point2dFloat(%f, %f)' % (self._x, self._y)

    def __getitem__(self, key):
        if   key == 0: return self._x
        elif key == 1: return self._y
        else: raise IndexError
    def __setitem__(self, key, value):
        if   key == 0: self.x = value
        elif key == 1: self.y = value
        else: raise IndexError

    def __eq__(self, other):
        if type(other) != type(self) and type(other) != tuple and type(other) != list:
            raise VectorError('Comparison of incompatible types: Vector2dFloat and %s' % type(other))
        return (self._x == other[0] and self._y == other[1])
    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        raise VectorError('Invalid vector comparison.')

    def __len__(self):
        return 2

    def __iter__(self):
        yield self._x
        yield self._y

    def __add__(self, other):
        return Point2dFloat(self._x + other[0], self._y + other[1])
    def __iadd__(self, other):
        self._x += other[0]
        self._y += other[1]
        return self

    def __sub__(self, other):
        return Point2dFloat(self._x - other[0], self._y - other[1])
    def __isub__(self, other):
        self._x -= other[0]
        self._y -= other[1]
        return self

    def __mul__(self, other):
        return Point2dFloat(self._x * other, self._y * other)
    def __imul__(self, other):
        self._x *= other
        self._y *= other
        return self



class Vector2dFloat(Point2dFloat):

# TODO:
# finish unittests
# optimize
#   keep mag in mag^2 form to speed up calcs
#   cache mag (and others) for future use so it doesn't have to be recalced every frickin time

    """2-Dimensional float-valued point.
    
    Properties:
    x -- the X component of the vector
    y -- the Y component of the vector
    mag -- the magnitude of the vector
    mag2 -- mag squared
    dir -- the vector of unit length with the same direction
    
    Each property is get-able and set-able. You can set the 'dir'
    property to a Vector, tuple, or list. This will rotate the vector
    to the same direction as the argument, keeping its magnitude. The
    magnitude of the operand does not have to be 1.
    
    mag2 is faster to calculate than mag, because it avoids a sqrt call.
    It should be used, for example, when comparing the magnitude of
    multiple vectors to a variable. It should not be used if you have to
    square or sqrt something to set or get it.
    
    The class also can function as a list with 2 elements.
    
    Instance Methods:
    reverse -- the opposite of a vector
    reverse_ip -- reverse a vector in place
    perp -- returns a perpendicular vector
    component -- component of a vector in a direction
    project -- vector projection
    
    """

    def __init__(self, *args):
        super(Vector2dFloat, self).__init__(*args)
        #self.__mag_cache

    # functions #
    def reverse(self):
        """Return the opposite of the vector."""
        return Vector2dFloat(-self._x, -self._y)
    
    def reverse_ip(self):
        """Reverse the vector in place."""
        self._x = -self._x
        self._y = -self._y

    def perp(self):
        """Return a perpendicular vector
        
        This function returns a vector of equal magnitude but rotated
        pi/2 radians counter clockwise.
        """
        return Vector2dFloat(self._y, -self._x)

    def component(self, other):
        """Return the vector component of this vector on another vector.
        
        This function calculates the vector component of a vector in the
        direction of the argument, and returns it as a float. The
        magnitude of the argument is irrelevent.
        """
        if type(other != Vector2dFloat):
            other = Vector2dFloat(other)
        if other.mag2 == 0:
            return 0.0
        return dot_prod(self, other.dir)

    def project(self, other):
        """Return the vector projection onto another vector.
        
        This function returns a vector in the same direction as the
        argument, but with magnitude v1.component(v2).
        """
        if type(other != Vector2dFloat):
            other = Vector2dFloat(other)
        return other.dir * self.component(other)

    # property management functions #
    
    def _get_mag2(self):
        return self._x**2 + self._y**2
    def _set_mag2(self, value):
        self.mag = math.sqrt(value)
    def _get_mag(self):
        return math.sqrt(self._x**2 + self._y**2)
    def _set_mag(self, value):
        self.__init__(self.dir * value)
    
    def _get_dir(self):
        if self.mag == 0:
            return Vector2dFloat(0,0)
            #raise VectorError('Zero length vector has no direction')
        return self.__truediv__(self.mag)
    def _set_dir(self, value):
        value = Vector2dFloat(value).dir
        self.__init__(value * self.mag)

    def _get_theta(self):
        return math.atan2(self._y, self._x)%_two_pi
    def _set_theta(self, value):
        theta = value % _two_pi
        if theta % (_pi/4) == 0:
            if theta == 0:         self.dir = (1,0)
            elif theta == _pi:     self.dir = (-1,0)
            elif theta == _pi/2:   self.dir = (0,1)
            elif theta == _pi*3/2: self.dir = (0,-1)
            elif theta == _pi/4:   self.dir = (1,1)
            elif theta == _pi*3/4: self.dir = (-1,1)
            elif theta == _pi*5/4: self.dir = (-1,-1)
            elif theta == _pi*7/4: self.dir = (1,-1)
        else:
            if _pi/2 <= theta < _pi*3/2: sign = -1
            else: sign = 1
            self.dir = (sign, sign*math.tan(theta))
            
    # properties #
    mag   = property(_get_mag, _set_mag)
    mag2  = property(_get_mag2, _set_mag2)
    dir   = property(_get_dir, _set_dir)
    theta = property(_get_theta, _set_theta)

    # operator overloads #
    def __str__(self):
        return '<%.2f, %.2f>' % (self._x, self._y)
    def __repr__(self):
        return '<%f, %f>' % (self._x, self._y)

    def __eq__(self, other):
        if type(other) != type(self) and type(other) != tuple and type(other) != list:
            return False
            #raise VectorError('Comparison of incompatible types: Vector2dFloat and %s' % type(other)')
        return (self._x == other[0] and self._y == other[1])
    def __ne__(self, other):
        return not self == other
    def __lt__(self, other):
        raise VectorError('Invalid vector comparison.')

    def __neg__(self):
        return self.reverse()

    def __add__(self, other):
        if type(other) != Vector2dFloat and type(other) != tuple and type(other) != list:
            raise TypeError('Cannot add Vector2dFloat and %s' % type(other))
        return Vector2dFloat(self._x + other[0], self._y + other[1])
    def __radd__(self, other):
        if type(other) != Point2dFloat and type(other) != tuple and type(other) != list:
            raise TypeError
        return Point2dFloat(other[0] + self._x, other[1] + self._y)
    
    def __sub__(self, other):
        return Vector2dFloat(self._x - other[0], self._y - other[1])
    def __rsub__(self, other):
        return Point2dFloat(other[0] - self._x, other[1] - self._y)

    def __mul__(self, other):
        return Vector2dFloat(self._x * other, self._y * other)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __imul__(self, other):
        self._x *= other
        self._y *= other
        return self

    def __div__(self, other):
        return self.__truediv__(other)
    def __idiv__(self, other):
        return self.__itruediv__(other)
    def __truediv__(self, other):
        return Vector2dFloat(self._x / other, self._y / other)
    def __itruediv__(self, other):
        self._x /= other
        self._y /= other
        return self


class Coord(object):
    
    """Integer-valued coordinate point.
    
    This class represents a coordinate point on a 2-dimensional plane.
    It has getable and setable properties x and y, representing its
    components. Coord objects can be manipulated mathematically like
    integers.    
    """

    def __init__(self, *args):
        if len(args) == 0 or args[0] is None:
            self.x, self.y = (0,0)
        elif len(args) == 1:
            try:
                self.x = args[0][0]
                self.y = args[0][1]
            except IndexError:
                raise VectorError('Coord must have two dimensions.')
            except TypeError:
                raise VectorError('Coord must have two dimensions.')
            except ValueError:
                raise VectorError('Coord type must be compatible with int.')
        else:
            try:
                self.x = args[0]
                self.y = args[1]
            except ValueError:
                raise VectorError('Coord type must be compatible with int.')

    # property management functions #

    def get_x(self):
        return self._x
    def set_x(self, value):
        self._x = int(value)
    def get_y(self):
        return self._y    
    def set_y(self, value):
        self._y = int(value)

    # properties #
    x = property(get_x, set_x)
    y = property(get_y, set_y)

    # operator overloads #
    def __str__(self):
        return '(%.2f, %.2f)' % (self._x, self._y)
    def __repr__(self):
        return 'Coord(%f, %f)' % (self._x, self._y)

    def __getitem__(self, key):
        if   key == 0: return self._x
        elif key == 1: return self._y
        else: raise IndexError
    def __setitem__(self, key, value):
        if   key == 0: self.x = value
        elif key == 1: self.y = value
        else: raise IndexError

    def __eq__(self, other):
        return (self._x == other[0] and self._y == other[1])
    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return 2

    def __iter__(self):
        yield self._x
        yield self._y

    def __add__(self, other):
        return Coord(self._x + other[0], self._y + other[1])
    def __iadd__(self, other):
        self._x += other[0]
        self._y += other[1]
        return self

    def __sub__(self, other):
        return Coord(self._x - other[0], self._y - other[1])
    def __isub__(self, other):
        self._x -= other[0]
        self._y -= other[1]
        return self
    
    def __mul__(self, other):
        return Coord(self._x * other, self._y * other)
    def __imul__(self, other):
        self._x *= other
        self._y *= other
        return self

    def __div__(self, other):
        return self.__truediv__(other)
    def __idiv__(self, other):
        return self.__itruediv__(other)
    def __truediv__(self, other):
        return Coord(self._x / other, self._y / other)
    def __itruediv__(self, other):
        self._x /= other
        self._y /= other
        return self    
    