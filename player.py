import vec

from inputmanager import InputManager
from particle import Particle
import constants as c

INPUT = InputManager.getInstance()

def heading_to_vector(heading):
    return vec.rotate((1, 0), heading)


class Player(Particle):
    def __init__(self, **kwargs):
        self.heading = kwargs.pop('heading', 0) # Heading in radians.
        self.direction = heading_to_vector(self.heading)
        super(Player, self).__init__(**kwargs)

    def update(self, elapsed_seconds):
        # The left and right keys turn the player, and the up and down
        # keys thrust forward and backward.
        self.heading += INPUT.x_axis * c.player_turn_rate_radians * elapsed_seconds
        self.direction = heading_to_vector(self.heading)
        input_strength = INPUT.y_axis * c.player_strength
        player_force = vec.mul(self.direction, input_strength)
        super(Player, self).update(elapsed_seconds, player_force)
