# TODO
# de-uglify the constructor

from __future__ import division
import math
from vector import Point2dFloat, Vector2dFloat

class Particle(object):
    def __init__(self, **kwds):
        try:
            self.pos = Point2dFloat(kwds['pos'])
        except KeyError:
            self.pos = Point2dFloat(0,0)
        try:
            self.velocity = Vector2dFloat(kwds['velocity'])
        except KeyError:
            self.velocity = Vector2dFloat(0,0)
        try:
            self.mass = float(kwds['mass'])
        except KeyError:
            self.mass = 1.0
        try:
            self.radius = float(kwds['radius'])
        except KeyError:
            self.radius = math.sqrt(self.mass)
            
        self.graphic = kwds['graphic'] ##TEMP
        
    def update(self, elapsed_seconds, force = None):
        if force is not None:
            self.velocity += force * (elapsed_seconds/self.mass)
        self.pos = self.pos + (self.velocity * (elapsed_seconds))

    def rebound(self, normal, point=None, restitution=1):
        if type(normal) != Vector2dFloat:
            normal = Vector2dFloat(normal)
        # split into normal and tangential components
        tangent = normal.perp()
        v_tangent = self.velocity.project(tangent)
        v_normal = self.velocity.project(normal)
        # invert normal component
        self.velocity = v_tangent + v_normal.reverse() * restitution
        
        if point is not None:
            v = Vector2dFloat(self.pos - point)
            if v.mag2 < self.radius ** 2: # if point is too close
                v.mag = self.radius
                self.pos = point + v

def intersect(p1, p2):
    return Vector2dFloat(p1.pos - p2.pos).mag2 <= (p1.radius + p2.radius)**2
    
def collide_elastic(p1, p2, restitution = 1):
    # test if p1 and p2 collide, then bounce them
    if not intersect(p1, p2):
        return
    m1, m2 = p1.mass, p2.mass
    m1plusm2 = (m1 + m2)/restitution
    v_span = Vector2dFloat(p2.pos - p1.pos) # vector from p1 to p2, normal to contact surface
    
    # split into normal and tangential components
    tangent = v_span.perp()
    v1tangent = p1.velocity.project(tangent)
    v2tangent = p2.velocity.project(tangent)
    v1i = p1.velocity.component(v_span)
    v2i = p2.velocity.component(v_span)
    if v1i <= v2i: # if particles were actually moving away from each other
        return # don't collide
    
    # elastic collision equations along normal component
    v1f = ((m1 - m2)/(m1plusm2))*v1i + ((2*m2)/(m1plusm2))*v2i
    v2f = ((2*m1)/(m1plusm2))*v1i + ((m2 - m1)/(m1plusm2))*v2i
    
    #print 'restitution = %.12f' % (-(v1f-v2f)/(v1i-v2i)) # debug
    
    # tangential component is unchanged, recombine
    unit_normal = v_span.dir
    p1.velocity = unit_normal * v1f + v1tangent
    p2.velocity = unit_normal * v2f + v2tangent
    
    # adjust faster particle not to clip inside slower one
    v_span.mag = p1.radius + p2.radius
    if p1.velocity.mag2 >= p2.velocity.mag2:
        p1.pos = p2.pos - v_span
    else:
        p2.pos = p1.pos + v_span
    