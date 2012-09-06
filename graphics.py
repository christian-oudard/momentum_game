import pygame as pg
import vec

# Colors.
PARTICLE_COLOR = (128, 32, 64)
WALL_COLOR = (32, 32, 32)
DIRECTION_COLOR = (255, 255, 255)

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
        pg.draw.circle(
            self.display.screen, 
            PARTICLE_COLOR,
            self.display.to_screen(particle.pos),
            int(particle.radius * self.display.pixels_per_unit),
        )

    def draw_player(self, player):
        self.draw_particle(player)

        # Show the player pointing towards a direction.
        if player.direction != (0, 0):
            leading_point = vec.add(
                player.pos,
                vec.norm(player.direction, player.radius),
            )
        else:
            leading_point = player.pos
        pg.draw.line(
            self.display.screen,
            DIRECTION_COLOR,
            self.display.to_screen(player.pos),
            self.display.to_screen(leading_point),
            3, # width
        )

    def draw_wall(self, wall):
        pg.draw.line(
            self.display.screen,
            WALL_COLOR,
            self.display.to_screen(wall.p1),
            self.display.to_screen(wall.p2),
            3, # width
        )
