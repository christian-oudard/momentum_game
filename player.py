import vec

from inputmanager import InputManager
from particle import Particle
import constants as c

INPUT = InputManager.getInstance()

class Player(Particle):
    def update(self, elapsed_seconds):
        # Check input and determine force applied to the player.
        player_force_input = (INPUT.x_axis, -INPUT.y_axis)
        if player_force_input != (0, 0):
            player_force_norm = vec.norm(player_force_input)
        else:
            player_force_norm = (0, 0)
        player_force = vec.mul(player_force_norm, c.player_strength)
        player_force = vec.sub(
            player_force,
            vec.mul(self.velocity,  c.player_control),
        )
        if vec.mag2(self.velocity) < c.min_speed2:
            self.velocity = vec.mul(
                player_force_norm,
                c.min_speed * (1 + c.drag_per_second * c.initial_speed_seconds),
            )
            player_force = None

        super(Player, self).update(elapsed_seconds, player_force)

