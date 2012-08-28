import pygame as pg

# Colors.
PARTICLE_COLOR = (128, 64, 64)
WALL_COLOR = (64, 128, 64)

class Graphics(object):
    def __init__(self, display):
         self.display = display

    def draw_particle(self, particle):
        pg.draw.circle(
            self.display.screen, 
            PARTICLE_COLOR,
            self.display.to_screen(particle.pos),
            int(particle.radius * self.display.pixels_per_unit),
        )

    def draw_wall(self, wall):
        pg.draw.line(
            self.display.screen,
            WALL_COLOR,
            self.display.to_screen(wall.p1),
            self.display.to_screen(wall.p2),
            1, # width
        )
