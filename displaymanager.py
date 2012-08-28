import pygame as pg

import vec
from singletonmixin import Singleton
from environment import Environment
from inputmanager import InputManager
from graphics import Graphics

# debug switches #
SHOW_JOYSTICK = True
SHOW_FPS = True

# constants #
FULLSCREEN = False

# colors #
BG_COLOR = (128,128,255)

# handles #
ENV = Environment.getInstance()
INPUT = InputManager.getInstance()

class DisplayManager(Singleton):
    """
    The display manager owns the pygame screen object, and the translation
    between world coordinates and screen coordinates. It also dispatches to the
    Graphics class to draw various kinds of objects.
    """
    def __init__(self):
        pass

    def init(self, screen_size):
        self.screen_size = screen_size
        self.pixels_per_unit = 20
        flags = pg.HWSURFACE | pg.DOUBLEBUF
        if FULLSCREEN:
            flags |= pg.FULLSCREEN
        self.screen = pg.display.set_mode(tuple(self.screen_size), flags)

        self.screen_origin = vec.div(self.screen_size, 2)
        
        self.widgets = []

        if SHOW_JOYSTICK:
            self.widgets.append(JoystickWidget(self))
        if SHOW_FPS:
            self.fps = 0.0
            self.widgets.append(FPSWidget(self))

        self.graphics = Graphics(self)

    def draw(self):
        self.screen.fill(BG_COLOR)

        for p in ENV.particles:
            self.graphics.draw_particle(p)
        for w in ENV.walls:
            self.graphics.draw_wall(w)

        for widget in self.widgets:
            widget.draw(self.screen)

        pg.display.flip()

    def to_screen(self, pos):
        """Convert pos to screen coordinates.
        
        Takes a tuple a world position, and returns a tuple for the
        screen position.
        """
        x, y = vec.add(
            self.screen_origin,
            vec.mul(pos, self.pixels_per_unit),
        )
        return (int(x), int(y))

    def set_fps(self, fps):
        self.fps = fps


class FPSWidget(object):
    def __init__(self, display):
        self.display = display
        self.font = pg.font.SysFont(pg.font.get_default_font(), 20)
        self.color = (255,255,255)

    def draw(self, screen):
        surface = self.font.render(
            '%.0f fps' % self.display.fps,
            True,
            self.color,
        )
        width, height = self.display.screen_size
        x = width - surface.get_width() - 10
        y = 10
        screen.blit(surface, (x, y))

            
class JoystickWidget(object):
    def __init__(self, display):
        self.display = display
        self.surface = pg.Surface((30,30), pg.SRCALPHA, 32)

    def draw(self, screen):
        self.surface.lock()
        self.surface.fill((0,0,0,0))
        pg.draw.line(self.surface, (128,255,128), (14-10,14), (14+10,14), 2)
        pg.draw.line(self.surface, (128,255,128), (14,14-10), (14,15+10), 2)
        joypos = vec.mul((INPUT.x_axis, -INPUT.y_axis), 8)
        pg.draw.circle(
            self.surface,
            (196,64,64),
            vec.add(joypos, (15,15)),
            4,
        )
        self.surface.unlock()

        width, height = self.display.screen_size
        x = 10
        y = height - self.surface.get_height() - 10
        screen.blit(self.surface, (x, y))
