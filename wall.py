from __future__ import division

import vec
import constants as c

class Wall(object):
    graphics_type = 'wall'

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.tangent = vec.vfrom(self.p1, self.p2)
        self.normal = vec.perp(self.tangent)
        
    def update(self, elapsedticks):
        pass
        
    def collide_wall(self, p, restitution = 1):        
        # First, check that we haven't crossed through the wall due to
        # extreme speed and low framerate.
        intersection = intersect_segments(self.p1, self.p2, p.last_pos, p.pos)
        if intersection:
            p.pos = p.last_pos
            p.rebound(self.normal, intersection, restitution)
            return

        # Find vectors to each endpoint of the segment.
        v1 = vec.vfrom(self.p1, p.pos)
        v2 = vec.vfrom(self.p2, p.pos)

        # Find a perpendicular vector from the wall to p.
        v_dist = vec.proj(v1, self.normal)

        # Test distance from the wall.
        radius2 = p.radius**2
        if vec.mag2(v_dist) > radius2:
            return
        
        # Test for collision with the endpoints of the segment.
        # Check whether p is too far off the end of the segment, by checking
        # the sign of the vector projection, then a radius check for the
        # distance from the endpoint.
        if vec.dot(v1, self.tangent) < 0:
            if vec.mag2(v1) > radius2:
                return
            p.rebound(v1, self.p1, restitution)
            return
        if vec.dot(v2, self.tangent) > 0:
            if vec.mag2(v2) > radius2:
                return
            p.rebound(v2, self.p2, restitution)
            return    

        # Test that p is headed toward the wall.
        if vec.dot(p.velocity, v_dist) >= c.epsilon:
            return

        # We are definitely not off the ends of the segment, and close enough
        # that we are colliding.
        p.rebound(self.normal, vec.sub(p.pos, v_dist), restitution)


def counterclockwise(a, b, c):
    """
    Determine whether the points a, b, and c are listed in
    counterclockwise order.

    Reference:
    http://compgeom.cs.uiuc.edu/~jeffe/teaching/373/notes/x05-convexhull.pdf

    >>> counterclockwise((0, 2), (3, 0), (4, 4))
    True
    >>> counterclockwise((3, 0), (0, 2), (4, 4))
    False
    """
    ax, ay = a
    bx, by = b
    cx, cy = c
    return (cx - ax) * (by - ay) < (bx - ax) * (cy - ay)

def intersect_segments(a, b, c, d):
    """
    Determine whether line segments ab and cd intersect, and if so,
    return their intersection point.

    Reference:
    http://compgeom.cs.uiuc.edu/~jeffe/teaching/373/notes/x06-sweepline.pdf

    >>> intersect_segments((1, 0), (1, 7), (0, 3), (5, 2))
    (1, 2.8)
    >>> intersect_segments((1, 0), (5, 2), (0, 3), (1, 7)) is None
    True
    """
    if counterclockwise(a, c, d) == counterclockwise(b, c, d):
        return None
    elif counterclockwise(a, b, c) == counterclockwise(a, b, d):
        return None
    return intersect_lines(a, b, c, d)

def intersect_lines(a, b, c, d):
    """
    Determine the intersection point of infinite lines ab and cd.

    Reference:
    http://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    """
    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = d

    if ax == bx:
        slope_ab = None
    else:
        slope_ab = (by - ay) / (bx - ax)
        y_intercept_ab = ay - slope_ab * ax

    if cx == dx:
        slope_cd = None
    else:
        slope_cd = (dy - cy) / (dx - cx)
        y_intercept_cd = cy - slope_cd * cx

    if slope_ab == slope_cd:
        return None

    if slope_ab is None:
        x = ax
        y = slope_cd * x + y_intercept_cd
    elif slope_cd is None:
        x = cx
        y = slope_ab * x + y_intercept_ab
    else:
        x = (y_intercept_cd - y_intercept_ab) / (slope_ab - slope_cd)
        y = slope_ab * x + y_intercept_ab

    return (x, y)
