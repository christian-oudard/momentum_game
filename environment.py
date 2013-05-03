from __future__ import division

from player import Player
from particle import Particle, collide_particles
from wall import Wall
import constants as c

class Environment(object):
    def __init__(self, inputs=None):
        if inputs is None:
            inputs = []
        self.inputs = inputs
        self.objects = []
        self.players = []
        self.particles = []
        self.walls = []

    def load_level(self, level):
        for object_class, args in level:
            if isinstance(args, dict):
                obj = object_class(**args)
            else:
                obj = object_class(*args)
            self.objects.append(obj)
            if isinstance(obj, Player):
                self.players.append(obj)
            if isinstance(obj, Particle):
                self.particles.append(obj)
            if isinstance(obj, Wall):
                self.walls.append(obj)

        for inp, p in zip(self.inputs, self.players):
            p.set_input(inp)
        for i, p in enumerate(self.players):
            p.number = i

    def update(self, elapsed_ticks):
        elapsed_seconds = elapsed_ticks / 1000

        #TODO: Use collision algorithms faster than O(n**2).

        # Particle collisions.
        for (p1, p2) in every_pair(self.particles):
            restitution = max(p1.restitution, p2.restitution)
            collide_particles(p1, p2, restitution)

        # Wall-particle collisions.
        for w in self.walls:
            for p in self.particles:
                w.collide_wall(p, c.restitution_wall)

        for o in self.particles:
            o.update(elapsed_seconds)

        # Check whether a player has won.
        for p in self.players:
            if not p.dead and p.damage > p.player_health:
                print('Player {} is dead.'.format(p.number + 1))
                p.dead = True
                self.objects.remove(p)
                self.particles.remove(p)


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
                yield a, b
