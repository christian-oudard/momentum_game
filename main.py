from __future__ import division
import pygame as p
from singletonmixin import SingletonException
from displaymanager import DisplayManager
from environment import Environment
from inputmanager import InputManager

## TEMP
from vector import Vector2dFloat
from particle import Particle
from wall import Wall
from graphic import Graphic
from wallgraphic import WallGraphic
##

# debug switches #
SHOW_FPS = True

# constants #
MAXFPS = 60
SCREENSIZE = (800, 600)

# handle #
DISP = DisplayManager.getInstance()
ENV = Environment.getInstance()
INPUT = InputManager.getInstance()

def main():

    # init #
    p.init()
    p.font.init()
    ENV.init()
    DISP.init(SCREENSIZE)
    INPUT.init()

    if SHOW_FPS:
        update_fps = p.USEREVENT + 1
        p.time.set_timer(update_fps, 700)

    ##TEMP, set up level
    g = Graphic()
    wg = WallGraphic()
    
    player = Particle(pos=(2,2),velocity=(0,0), mass=.5, graphic=g)
    ENV.add_obj(player)
    
    ENV.add_obj(Particle(pos=(0,3),velocity=(-1,3), mass=1, graphic=g))
    ENV.add_obj(Particle(pos=(-5,0),velocity=(-1,2), mass=.25, graphic=g))
    ENV.add_obj(Particle(pos=(3,-3),velocity=(0,-3), mass=3, graphic=g))
         
    ENV.add_obj(Wall((0,10),(-10,3),graphic=wg))
    ENV.add_obj(Wall((-10,3),(2,-11),graphic=wg))
    ENV.add_obj(Wall((2,-11),(13,0),graphic=wg))
    ENV.add_obj(Wall((13,0),(0,10),graphic=wg))
    ENV.add_obj(Wall((-3,0),(3,0),graphic=wg))
    ##
    
    
    # vars #
    done = False
    clock = p.time.Clock()
    clock.tick()  # necessary, or the first tick will be very large
    
    # program loop #
    while not done:
        # events #
        for e in p.event.get():
            if e.type == p.QUIT: done = True
            elif e.type == p.KEYDOWN:
                key = e.key
                if key == p.K_ESCAPE:
                    p.event.post(p.event.Event(p.QUIT))
                elif key == p.K_UP:
                    INPUT.up_last = True
                elif key == p.K_DOWN:
                    INPUT.up_last = False
                elif key == p.K_RIGHT:
                    INPUT.right_last = True
                elif key == p.K_LEFT:
                    INPUT.right_last = False
            elif e.type == p.MOUSEMOTION:
                pass
            elif e.type == p.MOUSEBUTTONDOWN:
                pass
            elif e.type == p.MOUSEBUTTONUP:
                pass
            elif SHOW_FPS:
                if e.type == update_fps:
                    DISP.set_fps(clock.get_fps())

        # logic #
        INPUT.update()
        
        elapsedticks = clock.get_time()
        ENV.update(elapsedticks)
        
        # draw #
        DISP.draw()
        
        # tick #
        clock.tick(MAXFPS)
        
    # end program loop #

    p.quit()
    
if __name__ == '__main__':
    main()
