import vec

class Wall(object):
    def __init__(self, p1, p2, graphic=None):
        self.p1 = p1
        self.p2 = p2
        self.tangent = vec.vfrom(self.p1, self.p2)
        self.normal = vec.perp(self.tangent)
        
        self.graphic = graphic
        
    def update(self, elapsedticks):
        pass
        
    def collide_wall(self, p, restitution = 1):        
        # Find vectors to each endpoint of the segment.
        v1 = vec.vfrom(self.p1, p.pos)
        v2 = vec.vfrom(self.p2, p.pos)

        # Find a perpendicular vector from the wall to p.
        v_dist = vec.proj(v1, self.normal)

        # Test that p is headed toward the wall.
        if vec.dot(p.velocity, v_dist) > 0:
            return
        
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

        # We are definitely not off the ends of the segment, and close enough
        # that we are colliding.
        p.rebound(self.normal, vec.sub(p.pos, v_dist), restitution)
