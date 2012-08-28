import math

# Physics constants.

# Speed limits.
min_speed = 0.2
min_speed2 = min_speed ** 2
max_speed = 40.0
max_speed2 = max_speed ** 2

# Drag.
# We vary drag based on velocity, specified in ranges.
# Each range is specified as (upper_velocity, drag).
# Drag is defined as the amount of velocity lost every second, and is in
# the range of 0 to infinity.
drag_curve = [
    (None, 1.5),
]

# Player physics.
player_strength = 30.0
player_turn_rate = 1.0 # full rotations / second
player_turn_rate_radians = player_turn_rate * (2 * math.pi)

# Collision restitution.
restitution_wall = 0.4
restitution_particle = 1.1
