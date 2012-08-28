from __future__ import division
import math
from pygame import Rect

import vec
from singletonmixin import Singleton
from inputmanager import InputManager
import particle
from particle import Particle
import wall
from wall import Wall
import constants as c

INPUT = InputManager.getInstance()

class Environment(Singleton):
    def __init__(self):
        pass # singleton
        
    def init(self):
        self.obj_list = []
        self.particles = []
        self.walls = []
        
    def add_obj(self, obj):
        self.obj_list.append(obj)
        if isinstance(obj, Particle):
            self.particles.append(obj)
        elif isinstance(obj, Wall):
            self.walls.append(obj)
    
    def update(self, elapsed_ticks):
        elapsed_seconds = elapsed_ticks/1000
        
        # Wall-particle collisions.
        for w in self.walls:
            for p in self.particles:
                w.collide_wall(p)
                    
        # Particle collisions.
        #TODO: Use an algorithm faster than O(n**2).
        for (p1, p2) in every_pair(self.particles):
            particle.collide_elastic(p1, p2)
        
        # Max speed, drag, and stop.
        #TODO: move to particle class.
        drag_multiplier = math.exp(c.drag_coefficient * elapsed_seconds)
        for p in self.particles:
            velocity2 = vec.mag2(p.velocity)
            if velocity2 > c.max_speed2:
                p.velocity = vec.norm(p.velocity, c.max_speed)
            elif velocity2 < c.min_speed2:
                p.velocity = (0,0)
            else:
                p.velocity = vec.mul(p.velocity, drag_multiplier)
            
        for obj in self.obj_list:
            obj.update(elapsed_seconds)

def every_pair(iterable):
    """An iterator through every pair in iterable
    
    Yields each distinct unordered pair. Only works if all items only
    compare equal to themselves.
    """
    for a in iterable:
        for b in iterable:
            if a is b:
                break
            else:
                yield (a,b)
