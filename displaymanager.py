import pygame as p

import vec
from singletonmixin import Singleton
from environment import Environment
from inputmanager import InputManager

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
    def __init__(self):
        pass

    def init(self, screen_size):
        self.screen_size = screen_size
        self.pixels_per_unit = 20
        flags = p.HWSURFACE | p.DOUBLEBUF
        if FULLSCREEN:
            flags |= p.FULLSCREEN
        self.screen = p.display.set_mode(tuple(self.screen_size), flags)

        self.screen_origin = vec.div(self.screen_size, 2)
        
        self.widgets = []

        if SHOW_JOYSTICK:
            self.widgets.append(JoystickWidget(self))
        if SHOW_FPS:
            self.fps = 0.0
            self.widgets.append(FPSWidget(self))

    def draw(self):
        self.screen.fill(BG_COLOR)

        ## possibly split into terrain then object draw order
        for obj in ENV.obj_list:
            obj.graphic.draw(obj)

        for widget in self.widgets:
            widget.draw(self.screen)

        p.display.flip()

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
        self.font = p.font.SysFont(p.font.get_default_font(), 20)
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
        self.surface = p.Surface((30,30), p.SRCALPHA, 32)

    def draw(self, screen):
        self.surface.lock()
        self.surface.fill((0,0,0,0))
        p.draw.line(self.surface, (128,255,128), (14-10,14), (14+10,14), 2)
        p.draw.line(self.surface, (128,255,128), (14,14-10), (14,15+10), 2)
        joypos = vec.mul((INPUT.x_axis, -INPUT.y_axis), 8)
        p.draw.circle(
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
