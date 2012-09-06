import math

# Physics constants.

# Speed limits.
min_speed = 0.2
min_speed2 = min_speed ** 2
max_speed = 40.0
max_speed2 = max_speed ** 2

# Drag.
# Drag rate is defined as the amount of speed lost every second, and is
# in the range of 0 to infinity.
drag_rate = 0.5

# Player physics.
player_turn_rate = 0.8 # full rotations / second
player_turn_rate_radians = player_turn_rate * (2 * math.pi)
player_rudder_strength = 5.0
# Player thrust strength varies based on the current speed in the
# direction it is already pointing.
player_thrust_curve = [
    (5.0, 55.0),
    (7.0, 45.0),
    (12.0, 35.0),
    (20.0, 10.0),
    (None, 0.1),
]
player_braking_strength = 30.0
player_minimum_brake_speed = 1.0

# Collision restitution.
restitution_wall = 0.6
restitution_particle = 1.0
