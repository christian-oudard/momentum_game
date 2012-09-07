import math
from particle import Particle
from player import Player
from wall import Wall

level0 = [
    (Player, dict(pos=(2,2), velocity=(0,0), mass=1.0, radius=1.0)),
    (Particle, dict(pos=(0,3),velocity=(-1,3), mass=1)),
    (Particle, dict(pos=(-5,0),velocity=(-1,2), mass=.25)),
    (Particle, dict(pos=(3,-3),velocity=(0,-3), mass=5)),
    (Wall, [(-3,-3), (-6,3)]),
    (Wall, [(6,3), (6,-3)]),
    (Wall, [(0,8), (-15,12)]),
    (Wall, [(-15,12), (-12,-7)]),
    (Wall, [(-12,-7), (2,-11)]),
    (Wall, [(2,-11), (14,-10)]),
    (Wall, [(14,-10), (17,2)]),
    (Wall, [(17,2), (15,13)]),
    (Wall, [(15,13), (0,8)]),
]

level1 = [
    (Player, dict(pos=(6,6), heading=math.pi*-3/4, velocity=(0,0), mass=1.0, radius=1.0)),
    (Player, dict(pos=(-6,-6), heading=math.pi*1/4, velocity=(0,0), mass=1.0, radius=1.0)),
    (Particle, dict(pos=(0,0),velocity=(0,0), mass=10)),
    (Particle, dict(pos=(5, -5),velocity=(0,0), mass=5)),
    (Particle, dict(pos=(-5, 5),velocity=(0,0), mass=5)),
    (Particle, dict(pos=(10, -10),velocity=(0,0), mass=2)),
    (Particle, dict(pos=(-10, 10),velocity=(0,0), mass=2)),
    (Particle, dict(pos=(15, -15),velocity=(0,0), mass=.5)),
    (Particle, dict(pos=(-15, 15),velocity=(0,0), mass=.5)),
    (Wall, [(-20,-20), (-20,20)]),
    (Wall, [(-20,20), (20,20)]),
    (Wall, [(20,20), (20,-20)]),
    (Wall, [(20,-20), (-20,-20)]),
    (Wall, [(-12,-8), (-8,-12)]),
    (Wall, [(12,8), (8,12)]),
]
