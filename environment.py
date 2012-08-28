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

INPUT = InputManager.getInstance()

# physics constants
_drag_per_second = 0.15
_drag_coefficient = math.log(1 - _drag_per_second)
_initial_speed_seconds = 0.1
_min_speed = 1.0
_min_speed2 = _min_speed ** 2
_max_speed = 40
_max_speed2 = _max_speed ** 2
_player_strength = 40.0
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
        
        # Wall-particle collisions.
        for w in self.walls:
            for p in self.particles:
                w.collide_wall(p)
                    
        # Particle collisions.
        #TODO: Use an algorithm faster than O(n**2).
        for (p1, p2) in every_pair(self.particles):
            particle.collide_elastic(p1, p2)
        
        # Max speed, drag, and stop.
        drag_multiplier = math.exp(_drag_coefficient * elapsed_seconds)
        for p in self.particles:
            velocity2 = vec.mag2(p.velocity)
            if velocity2 > _max_speed2:
                p.velocity = vec.norm(p.velocity, _max_speed)
            elif velocity2 < _min_speed2:
                p.velocity = (0,0)
            else:
                p.velocity = vec.mul(p.velocity, drag_multiplier)
            
        # Kludge, use the 0 element of the object list for the player.
        player = self.obj_list[0]
        player_force_input = (INPUT.x_axis, -INPUT.y_axis)
        if player_force_input != (0, 0):
            player_force_norm = vec.norm(player_force_input)
        else:
            player_force_norm = (0, 0)
        player_force = vec.mul(player_force_norm, _player_strength)

        player_force = vec.sub(
            player_force,
            vec.mul(player.velocity,  _player_control),
        )
        if vec.mag2(player.velocity) < _min_speed2:
            player.velocity = vec.mul(
                player_force_norm,
                _min_speed * (1 + _drag_per_second * _initial_speed_seconds),
            )
            player.update(elapsed_seconds)
        else:
            player.update(elapsed_seconds, player_force)
            
        # Hackish update of all the other objects normally
        #for obj in self.obj_list:
        for obj in self.obj_list[1:]:
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
