from __future__ import division

import math

## Global physics

epsilon = 10**-10
max_speed = 100.0 # units / second
# Drag rate is defined as the amount of speed lost every second, and is
# in the range of 0 to infinity.
drag_rate = 0.5
# Collision restitution.
restitution_wall = 0.6
restitution_particle = 1.0

## Player physics.

player_rudder_strength = 3.0

player_start_turn_rate = 0.1 # full rotations / second
player_start_turn_rate_radians = player_start_turn_rate * (2 * math.pi)
player_start_turn_time = 0.25 # seconds
player_turn_rate = 1.0 # full rotations / second
player_turn_rate_radians = player_turn_rate * (2 * math.pi)

player_braking_strength = 20.0
player_minimum_brake_speed = 0.1
player_thrust_curve = [
    # Player thrust strength varies based on the current speed.
    (5.0, 55.0),
    (7.0, 45.0),
    (12.0, 35.0),
    (20.0, 10.0),
    (30.0, 5.0),
    (None, 0.1),
]

player_boost_ready_time = 0.4 # seconds
player_boost_time = 0.075 # seconds
player_boost_strength = 1200.0
player_boost_heavy_time = 0.5 # seconds
player_boost_heavy_multiplier = 6.0
player_boost_restitution = 1.3

player_health = 500
