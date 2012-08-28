import vec

from inputmanager import InputManager
from particle import Particle
import constants as c

INPUT = InputManager.getInstance()

def heading_to_vector(heading):
    return vec.rotate((1, 0), heading)

def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0

def thrust_for_speed(speed):
    for s, t in c.player_thrust_curve:
        if not s or speed < s:
            return t

def braking_for_speed(speed):
    for s, t in c.player_braking_curve:
        if not s or speed < s:
            return t

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
        # Determine the current speed in the direction we are facing.
        # This can be negative.
        speed = vec.dot(self.velocity, self.direction)
        if sign(speed) == sign(INPUT.y_axis):
            thrust = thrust_for_speed(abs(speed))
        else:
            thrust = braking_for_speed(abs(speed))

        player_force = vec.mul(
            self.direction,
            INPUT.y_axis * thrust,
        )
        super(Player, self).update(elapsed_seconds, player_force)
