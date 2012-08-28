import pygame
from pygame import Rect
from displaymanager import DisplayManager

DISP = DisplayManager.getInstance()

# colors #
PARTICLE_COLOR = (128, 64, 64)

class Graphic(object):
    def __init__(self):
        pass

    def draw(self, obj):
        pygame.draw.circle(
            DISP.screen, 
            PARTICLE_COLOR,
            DISP.to_screen(obj.pos),
            int(obj.radius * DISP.pixels_per_unit),
        )
