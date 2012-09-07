from __future__ import division

import math
import pygame as pg
import vec
import constants as c

# Colors.
PARTICLE_COLOR = (64, 64, 64)
WALL_COLOR = (32, 32, 32)
DIRECTION_COLOR = (255, 255, 255)
THRUST_COLOR = (196, 32, 32)
BRAKE_COLOR = (16, 16, 16)

class Graphics(object):
    def __init__(self, display):
        self.display = display

    def draw(self, obj):
        drawing_functions = {
            'player': self.draw_player,
            'particle': self.draw_particle,
            'wall': self.draw_wall,
        }
        drawing_functions[obj.graphics_type](obj)

    def draw_particle(self, particle):
        self.circle(PARTICLE_COLOR, particle.pos, particle.radius)

    def draw_player(self, player):
        # Show whether or not the player is thrusting.
        if player.do_thrust:
            trailing_point = vec.add(
                player.pos,
                vec.norm(player.direction, -1.5 * player.radius),
            )
            self.line(THRUST_COLOR, player.pos, trailing_point, .5 * player.radius)
        if player.boost_heavy_time_remaining > 0.0:
            trailing_point = vec.add(
                player.pos,
                vec.norm(player.direction, -2.0 * player.radius),
            )
            self.line(THRUST_COLOR, player.pos, trailing_point, 1.5 * player.radius)

        # Show braking and boosting charge up.
        if player.do_brake:
            # Redden the brake color as we charge.
            color = vec.add(
                BRAKE_COLOR,
                vec.mul(THRUST_COLOR, player.boost_charge_time / c.player_boost_ready_time)
            )
            # Vibrate if we are fully charged.
            r = 1.2
            if player.boost_charge_time == c.player_boost_ready_time:
                r += 0.1 * math.sin(6 * (2*math.pi) * pg.time.get_ticks() / 1000)
            self.circle(color, player.pos, r)


        self.draw_particle(player)

        # Show the player pointing towards a direction.
        leading_point = vec.add(
            player.pos,
            vec.norm(player.direction, player.radius),
        )
        self.line(DIRECTION_COLOR, player.pos, leading_point, .2 * player.radius)

    def draw_wall(self, wall):
        self.line(WALL_COLOR, wall.p1, wall.p2, .25)

    # Drawing utility functions.

    def line(self, color, a, b, width):
        pg.draw.line(
            self.display.screen,
            color,
            self.display.to_screen(a),
            self.display.to_screen(b),
            max(1, int(width * self.display.pixels_per_unit)),
        )

    def circle(self, color, center, radius):
        pg.draw.circle(
            self.display.screen,
            color,
            self.display.to_screen(center),
            int(radius * self.display.pixels_per_unit),
        )
