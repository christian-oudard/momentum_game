# TODO
# make field rotatable
# make screen_size, screen_origin, pixels_per_unit, fullscreen, etc
#   settable through functions

import pygame
from pygame.locals import *

from singletonmixin import Singleton
from vector import Coord, Point2dFloat
from environment import Environment
from inputmanager import InputManager

# debug switches #
_SHOW_JOYSTICK = True
_SHOW_FPS = True

# constants #
_FULL = False

# colors #
_BG_COLOR = (128,128,255)

# handles #
ENV = Environment.getInstance()
INPUT = InputManager.getInstance()

class DisplayManager(Singleton):
    def __init__(self):
        pass

    def init(self, screen_size):
        self.screen_size = Coord(screen_size)
        self.pixels_per_unit = 20
        flags = HWSURFACE | DOUBLEBUF
        if _FULL: flags |= FULLSCREEN
        self.screen = pygame.display.set_mode(tuple(self.screen_size), flags)

        self.screen_origin = self.screen_size / 2
        
        if _SHOW_JOYSTICK:
            self.__joystick_surface = pygame.Surface((30,30), SRCALPHA, 32)
        if _SHOW_FPS:
            pygame.font.init()
            self.__font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
            self.__fps = 0.0
            self.__fps_surface = None
            self._debug_update_fps_surface()

    def draw(self):
        self.screen.fill(_BG_COLOR)

        ## possibly split into terrain then object draw order

        for obj in ENV.obj_list:
            obj.graphic.draw(obj)
            
        if _SHOW_JOYSTICK:
            self._debug_update_joystick_surface()
            self.screen.blit(self.__joystick_surface, (10, self.screen_size.y - self.__joystick_surface.get_height() - 10))
        if _SHOW_FPS:
            self._debug_update_fps_surface()
            self.screen.blit(self.__fps_surface, (self.screen_size.x - self.__fps_surface.get_width() - 10, 10))
        
        pygame.display.flip()

    def to_screen(self, pos):
        """Convert pos to screen coordinates.
        
        Takes a Point2dFloat (or equivalent) representing a position,
        and returns a Coord for the screen position
        """
        if type(pos) != Point2dFloat:
            pos = Point2dFloat(pos)
        return self.screen_origin + pos * self.pixels_per_unit

    if _SHOW_JOYSTICK:
        def _debug_update_joystick_surface(self):
            self.__joystick_surface.lock()
            self.__joystick_surface.fill((0,0,0,0))
            pygame.draw.line(self.__joystick_surface, (128,255,128), (14-10,14), (14+10,14), 2)
            pygame.draw.line(self.__joystick_surface, (128,255,128), (14,14-10), (14,15+10), 2)
            joypos = Coord(INPUT.x_axis, -INPUT.y_axis) * 8
            pygame.draw.circle(self.__joystick_surface, (196,64,64), tuple(joypos + (15,15)), 4)
            self.__joystick_surface.unlock()
    
    if _SHOW_FPS:
        def debug_set_fps(self, fps):
            self.__fps = fps
            self._debug_update_fps_surface()
        def _debug_update_fps_surface(self):
            self.__fps_surface = self.__font.render('%.0f fps' % self.__fps, True, (255,255,255))
            

