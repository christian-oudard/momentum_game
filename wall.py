from vector import Point2dFloat, Vector2dFloat

class Wall(object):
    def __init__(self, p1, p2, **kwds):
        self.p1 = Point2dFloat(p1)
        self.p2 = Point2dFloat(p2)
        self.tangent = Vector2dFloat(self.p2 - self.p1) # vector from p1 to p2
        self.normal = self.tangent.perp()
        
        self.graphic = kwds['graphic'] ##TEMP
        
    def update(self, elapsedticks):
        pass
        
    def collide_wall(self, p, restitution = 1):        
        v1 = Vector2dFloat(p.pos - self.p1) # vector from p1 to p
        v_dist = v1.project(self.normal) # perp vector from wall to p
        rad2 = p.radius**2
        
        # test distance from the wall
        if v_dist.mag2 > rad2:
            return
        
        v2 = Vector2dFloat(p.pos - self.p2) # vector from p2 to p

        # test whether p is too far off the end of the segment
        if v1.component(self.tangent) < 0:
            if v1.mag2 > rad2:
                return
            else:
                if p.velocity.component(v1) > 0: # must be headed toward
                    return
                p.rebound(v1, self.p1, restitution)
                return
        if v2.component(self.tangent) > 0:
            if v2.mag2 > rad2:
                return
            else:
                if p.velocity.component(v2) > 0: # must be headed toward
                    return
                else:
                    p.rebound(v2, self.p2, restitution)
                    return    
        
        # test that p is headed toward the wall
        if p.velocity.component(v_dist) > 0:
            return
        else:
            p.rebound(self.normal, p.pos - v_dist, restitution)
