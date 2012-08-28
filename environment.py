from __future__ import division

import itertools
import math

from pygame import Rect

import vec
from particle import Particle, collide_elastic
from player import Player
from wall import Wall
import constants as c

class Environment(object):
    def __init__(self):
        self.particles = []
        self.walls = []

        ##TEMP, set up level
        self.add_objects([
            Player(pos=(2,2),velocity=(0,0), mass=1.5),
            Particle(pos=(0,3),velocity=(-1,3), mass=1),
            Particle(pos=(-5,0),velocity=(-1,2), mass=.25),
            Particle(pos=(3,-3),velocity=(0,-3), mass=3),
            Wall((-3,0), (3,0)),
            Wall((0,8), (-15,12)),
            Wall((-15,12), (-12,-7)),
            Wall((-12,-7), (2,-11)),
            Wall((2,-11), (14,-10)),
            Wall((14,-10), (17,2)),
            Wall((17,2), (15,13)),
            Wall((15,13), (0,8)),
        ])
        ##

    def add_objects(self, objects):
        for o in objects:
            if isinstance(o, Particle):
                self.particles.append(o)
            elif isinstance(o, Wall):
                self.walls.append(o)
    
    def update(self, elapsed_ticks):
        elapsed_seconds = elapsed_ticks/1000
        
        #TODO: Use collision algorithms faster than O(n**2).
        
        # Wall-particle collisions.
        for w in self.walls:
            for p in self.particles:
                w.collide_wall(p)
                    
        # Particle collisions.
        for (p1, p2) in every_pair(self.particles):
            collide_elastic(p1, p2)
            
        for o in self.particles:
            o.update(elapsed_seconds)

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
