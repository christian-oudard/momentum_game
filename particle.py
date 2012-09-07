from __future__ import division
import math

import vec
import constants as c

class Particle(object):
    graphics_type = 'particle'

    def __init__(
        self,
        pos=(0, 0),
        velocity=(0, 0),
        mass=1.0,
        radius=None,
    ):
        self.last_pos = pos
        self.pos = pos
        self.velocity = velocity
        self.mass = mass
        if radius is None:
            radius = math.sqrt(self.mass)
        self.radius = radius
        
    def update(self, elapsed_seconds, force=None):
        # Apply drag.
        # Decrease the magnitude of the velocity vector by
        # the amount of drag.
        speed = vec.mag(self.velocity)
        drag = c.drag_rate * elapsed_seconds
        if drag > speed:
            self.velocity = (0, 0)
        elif drag != 0 and self.velocity != (0, 0):
            drag_vector = vec.norm(self.velocity, -drag)
            self.velocity = vec.add(
                self.velocity,
                drag_vector,
            )

        # Limit to maximum speed.
        speed = vec.mag(self.velocity)
        if speed > c.max_speed:
            self.velocity = vec.norm(self.velocity, c.max_speed)

        # Apply force if necessary.
        if force is not None:
            self.velocity = vec.add(
                self.velocity,
                vec.mul(force, (elapsed_seconds / self.mass)),
            )

        # Update position based on velocity.
        self.last_pos = self.pos
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
    
def collide_particles(p1, p2, restitution = 1):
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

    # Tangential component is unchanged, recombine.
    p1.velocity = vec.add(
        v1_tangent,
        vec.mul(normal, p1_final),
    )
    p2.velocity = vec.add(
        v2_tangent,
        vec.mul(normal, p2_final),
    )
