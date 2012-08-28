import math

# Physics constants.
drag_per_second = 0.1
drag_coefficient = math.log(1 - drag_per_second)

min_speed = 2.0
min_speed2 = min_speed ** 2
max_speed = 40.0
max_speed2 = max_speed ** 2

player_strength = 40.0
player_turn_rate = 1.0 # full rotations / second
player_turn_rate_radians = player_turn_rate * (2 * math.pi)

restitution_wall = 0.5
restitution_particle = 1.1
