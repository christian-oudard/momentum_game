# TODO
# de-uglify the constructor

from __future__ import division
import math

import vec

class Particle(object):
    def __init__(
        self,
        pos=(0, 0),
        velocity=(0, 0),
        mass=1.0,
        radius=None,
        graphic=None,
    ):
        self.pos = pos
        self.velocity = velocity
        self.mass = mass
        if radius is None:
            radius = math.sqrt(self.mass)
        self.radius = radius
        self.graphic = graphic
        
    def update(self, elapsed_seconds, force = None):
        if force is not None:
            self.velocity = vec.add(
                self.velocity,
                vec.mul(force, (elapsed_seconds / self.mass)),
            )
        self.pos = vec.add(
            self.pos,
            vec.mul(self.velocity, elapsed_seconds),
        )

    def rebound(self, normal, point=None, restitution=1):
        # Split into normal and tangential components.
        tangent = vec.perp(normal)
        v_tangent = vec.proj(self.velocity, tangent)
        v_normal = vec.proj(self.velocity, normal)
        # Invert normal component and recombine, with restitution.
        v_normal = vec.neg(v_normal)
        self.velocity = vec.add(
            v_tangent,
            vec.mul(v_normal, restitution),
        )
        # If the particle is partially inside the wall, move it out.
        if point is not None:
            v = vec.vfrom(point, self.pos)
            if vec.mag2(v) < self.radius ** 2:
                v = vec.norm(v, self.radius)
                self.pos = vec.add(point, v)

def intersect(p1, p2):
    distance2 = vec.mag2(vec.vfrom(p1.pos, p2.pos))
    return distance2 <= (p1.radius + p2.radius)**2
    
def collide_elastic(p1, p2, restitution = 1):
    # Test if p1 and p2 are actually intersecting.
    if not intersect(p1, p2):
        return

    # Vector spanning between the centers, normal to contact surface.
    v_span = vec.vfrom(p1.pos, p2.pos)
    
    # Split into normal and tangential components.
    normal = vec.norm(v_span)
    tangent = vec.perp(normal)
    v1_tangent = vec.proj(p1.velocity, tangent)
    v2_tangent = vec.proj(p2.velocity, tangent)

    # Calculate initial velocities.
    p1_initial = vec.dot(p1.velocity, normal)
    p2_initial = vec.dot(p2.velocity, normal)

    # Don't collide if particles were actually moving away from each other, so
    # they don't get stuck inside one another.
    if p1_initial - p2_initial < 0:
        return
    
    # Elastic collision equations along normal component.
    m1, m2 = p1.mass, p2.mass
    m1plusm2 = (m1 + m2) / restitution
    p1_final = (
        p1_initial * (m1 - m2) / m1plusm2 + 
        p2_initial * (2 * m2) / m1plusm2
    )
    p2_final = (
        p2_initial * (m2 - m1) / m1plusm2 + 
        p1_initial * (2 * m1) / m1plusm2
    )
    
    #print 'restitution = %.12f' % (-(p1_final-p2_final)/(p1_initial-p2_initial)) # debug
    
    # Tangential component is unchanged, recombine.
    p1.velocity = vec.add(
        v1_tangent,
        vec.mul(normal, p1_final),
    )
    p2.velocity = vec.add(
        v2_tangent,
        vec.mul(normal, p2_final),
    )

    # Adjust faster particle not to clip inside slower one.
    v_span = vec.norm(v_span, p1.radius + p2.radius)
    if vec.mag2(p1.velocity) >= vec.mag2(p2.velocity):
        p1.pos = vec.sub(p2.pos, v_span)
    else:
        p2.pos = vec.add(p1.pos, v_span)
    
