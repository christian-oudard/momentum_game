import constants as c
from particle import Particle

class Bumper(Particle):
    graphics_type = 'bumper'
    restitution = c.restitution_bumper
    immovable = True
