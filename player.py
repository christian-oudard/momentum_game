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
        self.rudder_force = (0, 0)

        # States
        self.do_coast = False
        self.do_thrust = False
        self.do_brake = False
        self.turn_direction = 0
        self.turning_time = 0.0
        self.boost_charge_time = 0.0
        self.boost_time_remaining = 0.0
        self.boost_heavy_time_remaining = 0.0

        # Damage
        self.damage = 0.0
        self.dead = False
        self.player_health = kwargs.pop('player_health', c.player_health)

        super(Player, self).__init__(**kwargs)

        self.original_mass = self.mass

    def set_input(self, inp):
        self.input = inp

    def update(self, elapsed_seconds, force=None, extra_drag=0):
        self.update_state(elapsed_seconds)
        force, extra_drag = self.update_physics(elapsed_seconds)

        super(Player, self).update(elapsed_seconds, force, extra_drag)

    def update_state(self, elapsed_seconds):
        """
        Update the player state based on controller input and timed effects.

        The up key thrusts, and the down key brakes.
        The left and right keys turn left and right.

        Turning has a ramp up period.

        Holding the brake key charges up a boost.
        """
        prev_do_brake = self.do_brake

        self.interpret_controls()

        # Turning.
        if self.turn_direction == 0:
            self.turning_time = 0.0
        else:
            self.turning_time += elapsed_seconds

        # Trigger boost by releasing the brake key once charged.
        if (
            prev_do_brake and not self.do_brake and
            self.boost_charge_time >= c.player_boost_ready_time
        ):
            self.boost_time_remaining = c.player_boost_time
            self.boost_heavy_time_remaining = c.player_boost_heavy_time

        # Time out boost state.
        self.boost_time_remaining -= elapsed_seconds
        self.boost_time_remaining = max(self.boost_time_remaining, 0.0)
        self.boost_heavy_time_remaining -= elapsed_seconds
        self.boost_heavy_time_remaining = max(self.boost_heavy_time_remaining, 0.0)

        # Charge boost by holding the brake key.
        if self.do_brake and self.speed == 0:
            self.boost_charge_time += elapsed_seconds
            self.boost_charge_time = min(
                self.boost_charge_time,
                c.player_boost_ready_time,
            )
        else:
            self.boost_charge_time = 0.0

    def interpret_controls(self):
        if not hasattr(self.input, 'turn_direction'):
            # Interpret controls using x and y axis to pick a target direction,
            # then translate into turn direction and thrust.
            # If the player is pushing towards a direction and not braking,
            # then it is thrusting.
            self.do_brake = self.input.brake
            self.turn_direction = 0
            self.do_thrust = False
            self.intended_direction = (self.input.x_axis, -self.input.y_axis)
            if self.intended_direction != (0, 0):
                if not self.do_brake:
                    self.do_thrust = True
                # Determine which direction we should turn to come closer to the
                # correct one.
                side = vec.dot(self.intended_direction, vec.perp(self.direction))
                if (
                    vec.angle(self.intended_direction, self.direction) <
                    c.player_intended_turn_threshold
                ):
                    self.turn_direction = 0
                elif side < 0:
                    self.turn_direction = +1
                elif side > 0:
                    self.turn_direction = -1
        else:
            # Interpret controls using thrust, brake, and turn direction.
            self.turn_direction = self.input.turn_direction
            self.do_brake = self.input.brake
            self.do_thrust = self.input.thrust and not self.do_brake

    def update_physics(self, elapsed_seconds):
        # Handle turning.
        if self.turning_time >= c.player_start_turn_time:
            turn_rate = c.player_turn_rate_radians
        else:
            turn_rate = interpolate(
                c.player_start_turn_rate_radians,
                c.player_turn_rate_radians,
                self.turning_time / c.player_start_turn_time,
            )

        self.heading += self.turn_direction * turn_rate * elapsed_seconds
        self.direction = heading_to_vector(self.heading)

        # Handle thrust.
        force = (0, 0)
        if self.do_thrust:
            # We vary the thrust depending on how fast the player is
            # already moving.
            thrust = curve_value(self.speed, c.player_thrust_curve)
            force = vec.add(
                force,
                vec.mul(self.direction, thrust),
            )

        # Handle braking.
        extra_drag = 0
        if self.do_brake:
            extra_drag = c.player_braking_drag

        # Handle boost.
        if self.boost_time_remaining > 0.0:
            force = vec.add(
                force,
                vec.mul(self.direction, c.player_boost_strength),
            )
        # Get heavy while boosting.
        if self.boost_heavy_time_remaining > 0.0:
            self.mass = self.original_mass * c.player_boost_heavy_multiplier
            self.restitution = c.player_boost_restitution
        else:
            self.mass = self.original_mass
            self.restitution = c.restitution_particle

        # Handle rudder.
        self.rudder_force = (0, 0)
        if self.velocity != (0, 0):
            # Only use the rudder if the player is thrusting or turning.
            if self.do_thrust or self.turn_direction != 0:
                self.rudder_force = self.calc_rudder_force()
                force = vec.add(force, self.rudder_force)

        return force, extra_drag

    def calc_rudder_force(self):
        # We continuously bring the direction of the player's movement to be
        # closer in line with the direction it is facing.
        target_velocity = vec.norm(self.direction, self.speed)
        force = vec.vfrom(self.velocity, target_velocity)
        if force == (0, 0):
            return (0, 0)

        # The strength of the rudder is highest when acting perpendicular to
        # the direction of movement.
        v_perp = vec.norm(vec.perp(self.velocity))
        angle_multiplier = abs(vec.dot(v_perp, self.direction))
        strength = self.speed * c.player_rudder_strength
        strength = min(strength, c.player_max_rudder_strength)
        strength *= angle_multiplier
        if strength == 0:
            return (0, 0)

        force = vec.norm(force, strength)
        return force

    def rebound(self, *args, **kwargs):
        v_initial = self.velocity
        super(Player, self).rebound(*args, **kwargs)
        v_final = self.velocity

        # Apply damage based on the difference in momentum.
        v_diff = vec.sub(v_final, v_initial)
        self.damage += vec.mag(v_diff) * self.mass
