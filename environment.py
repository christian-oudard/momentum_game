from __future__ import division
import math
from singletonmixin import Singleton
from pygame import Rect
from inputmanager import InputManager
from vector import Vector2dFloat
import particle
from particle import Particle
import wall
from wall import Wall

INPUT = InputManager.getInstance()

# constants #
_origin = Vector2dFloat(0,0)

# physics constants
_drag_per_second = 0.15
_drag_coefficient = math.log(1 - _drag_per_second)
_initial_speed_seconds = 0.1
_min_speed = 1.0
_min_speed2 = _min_speed ** 2
_max_speed = 40
_max_speed2 = _max_speed ** 2
_player_strength = 10.0
_player_control = .4

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
        
        # wall-particle collisions #
        for w in self.walls:
            for p in self.particles:
                w.collide_wall(p)
                    
        # particle collisions #
        for (p1, p2) in every_pair(self.particles):
            particle.collide_elastic(p1, p2)
        
        # max speed, drag, and stop #
        drag_multiplier = math.exp(_drag_coefficient * elapsed_seconds)
        for p in self.particles:
            velo2 = p.velocity.mag2
            if velo2 > _max_speed2:
                p.velocity.mag = _max_speed
            elif velo2 < _min_speed2:
                p.velocity = Vector2dFloat(0,0)
            else:
                p.velocity = drag_multiplier * p.velocity
            
##        for obj in self.obj_list:
##            obj.update(elapsedticks)

        ##TEMP
        player_force = Vector2dFloat(INPUT.x_axis, -INPUT.y_axis).dir * _player_strength
        player_force -= self.obj_list[0].velocity * _player_control
        if self.obj_list[0].velocity.mag2 < _min_speed2:
            self.obj_list[0].velocity = player_force.dir * (_min_speed * (1 + _drag_per_second * _initial_speed_seconds))
            self.obj_list[0].update(elapsed_seconds)
        else:
            self.obj_list[0].update(elapsed_seconds, player_force)
        for obj in self.obj_list[1:]:
            obj.update(elapsed_seconds)
        ##

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
