import pygame
from displaymanager import DisplayManager

DISP = DisplayManager.getInstance()

# colors #
WALL_COLOR = (64, 128, 64)

class WallGraphic(object):
    def __init__(self):
        pass

    def draw(self, obj):
        pygame.draw.line(DISP.screen,
                         WALL_COLOR,
                         DISP.to_screen(obj.p1),
                         DISP.to_screen(obj.p2),
                         1)