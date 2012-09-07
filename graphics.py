from __future__ import division

import math
import pygame as pg
import vec

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

        # Show braking.
        if player.do_brake:
            self.circle(BRAKE_COLOR, player.pos, 1.2 * player.radius)

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
