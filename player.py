import vec

from inputmanager import InputManager
from particle import Particle
import constants as c

INPUT = InputManager.getInstance()

def heading_to_vector(heading):
    return vec.rotate((1, 0), heading)

def thrust_for_speed(speed):
    for s, t in c.player_thrust_curve:
        if s is None or speed < s:
            return t

class Player(Particle):
    def __init__(self, **kwargs):
        self.heading = kwargs.pop('heading', 0) # Heading in radians.
        self.direction = heading_to_vector(self.heading)
        super(Player, self).__init__(**kwargs)

    def update(self, elapsed_seconds):
        # Handle turning. The left and right keys turn the player.
        self.heading += INPUT.x_axis * c.player_turn_rate_radians * elapsed_seconds
        self.direction = heading_to_vector(self.heading)

        # The up key thrusts, and the down key brakes.
        speed = vec.mag(self.velocity)
        player_force = (0, 0)
        if INPUT.y_axis == +1:
            # Handle thrust.
            # We vary the thrust depending on how fast the player is
            # already moving.
            thrust = thrust_for_speed(speed)
            player_force = vec.mul(self.direction, thrust)
        elif INPUT.y_axis == -1:
            # Handle braking.
            # Always oppose the current velocity.
            if speed >= c.player_minimum_brake_speed:
                player_force = vec.norm(self.velocity, -c.player_braking_strength)

        # Handle rudder. We continuously bring the direction of the
        # player's movement to be closer in line with the direction
        # it is facing.
        target_velocity = vec.norm(self.direction, speed)
        rudder_force = vec.vfrom(self.velocity, target_velocity)
        rudder_force = vec.mul(rudder_force, c.player_rudder_strength)
        player_force = vec.add(player_force, rudder_force)

        super(Player, self).update(elapsed_seconds, player_force)
