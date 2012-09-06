import pygame as pg

import vec
from input_manager import INPUT
from graphics import Graphics

# debug switches #
SHOW_JOYSTICK = True
SHOW_INFO = True

# constants #
FULLSCREEN = False

# colors #
BG_COLOR = (128, 128, 255)

class Display(object):
    """
    The display manager owns the pygame screen object, and the translation
    between world coordinates and screen coordinates. It also dispatches to the
    Graphics class to draw various kinds of objects.

    Architecturally, the display manager looks at the environment, and shows it
    as it chooses, rather than having the environment tell the display manager
    how to show its various pieces.
    """
    def __init__(self, environment, screen_size):
        self.environment = environment
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
        if SHOW_INFO:
            self.fps = 0.0
            self.widgets.append(InfoWidget(self))

        self.graphics = Graphics(self)

    def draw(self):
        self.screen.fill(BG_COLOR)

        for o in self.environment.objects:
            self.graphics.draw(o)
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


class InfoWidget(object):
    text_color = (255, 255, 255)

    def __init__(self, display):
        self.display = display
        self.font = pg.font.SysFont(pg.font.get_default_font(), 20)

    def text(self):
        return [
            '{:.0f} fps'.format(self.display.fps),
            'player speed: {:.1f}'.format(
                vec.mag(self.display.environment.particles[0].velocity)),
        ]


    def draw(self, screen):
        screen_width, _screen_height = self.display.screen_size
        y = 10
        for line in self.text():
            surface = self.font.render(
                line,
                True,
                self.text_color,
            )
            x = screen_width - surface.get_width() - 10
            screen.blit(surface, (x, y))
            y += surface.get_height()


class JoystickWidget(object):
    green = (128, 255, 128)
    clear = (0, 0, 0, 0)
    red = (196, 64, 64)

    def __init__(self, display):
        self.display = display
        self.surface = pg.Surface((30, 30), pg.SRCALPHA, 32)

    def draw(self, screen):
        self.surface.lock()
        self.surface.fill(self.clear)
        pg.draw.line(
            self.surface,
            self.green,
            (14-10, 14),
            (14+10, 14),
            2,
        )
        pg.draw.line(
            self.surface,
            self.green,
            (14, 14-10),
            (14, 15+10),
            2,
        )
        joypos = vec.mul((INPUT.x_axis, -INPUT.y_axis), 8)
        pg.draw.circle(
            self.surface,
            self.red,
            vec.add(joypos, (15,15)),
            4,
        )
        self.surface.unlock()

        _width, height = self.display.screen_size
        x = 10
        y = height - self.surface.get_height() - 10
        screen.blit(self.surface, (x, y))
