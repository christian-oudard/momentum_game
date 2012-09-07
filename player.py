from __future__ import division

import vec

from particle import Particle
import constants as c

def heading_to_vector(heading):
    return vec.rotate((1, 0), heading)

def interpolate(low, high, amount):
    return low + (high - low) * amount

def curve_value(key, curve):
    for s, t in curve:
        if s is None or key < s:
            return t

class Player(Particle):
    graphics_type = 'player'

    def __init__(self, **kwargs):
        self.input = None
        self.heading = kwargs.pop('heading', 0) # Heading in radians.
        self.direction = heading_to_vector(self.heading)
        self.turning_time = 0.0
        super(Player, self).__init__(**kwargs)

    def set_input(self, inp):
        self.input = inp

    def update(self, elapsed_seconds, force=None):
        # Handle turning. The left and right keys turn the player.
        if self.input.x_axis == 0:
            self.turning_time = 0.0
        else:
            self.turning_time += elapsed_seconds

        if self.turning_time >= c.player_start_turn_time:
            turn_rate = c.player_turn_rate_radians
        else:
            turn_rate = interpolate(
                c.player_start_turn_rate_radians,
                c.player_turn_rate_radians,
                self.turning_time / c.player_start_turn_time,
            )

        self.heading += self.input.x_axis * turn_rate * elapsed_seconds
        self.direction = heading_to_vector(self.heading)

        # The up key thrusts, and the down key brakes.
        speed = vec.mag(self.velocity)
        force = (0, 0)
        if self.input.y_axis == +1:
            # Handle thrust.
            # We vary the thrust depending on how fast the player is
            # already moving.
            thrust = curve_value(speed, c.player_thrust_curve)
            force = vec.add(
                force,
                vec.mul(self.direction, thrust),
            )
        elif self.input.y_axis == -1:
            # Handle braking.
            # Always oppose the current velocity.
            if speed >= c.player_minimum_brake_speed:
                force = vec.add(
                    force,
                    vec.norm(self.velocity, -c.player_braking_strength),
                )

        # Handle rudder. We continuously bring the direction of the
        # player's movement to be closer in line with the direction
        # it is facing.
        target_velocity = vec.norm(self.direction, speed)
        rudder_force = vec.vfrom(self.velocity, target_velocity)
        rudder_force = vec.mul(rudder_force, c.player_rudder_strength)
        force = vec.add(force, rudder_force)

        super(Player, self).update(elapsed_seconds, force)
