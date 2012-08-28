from __future__ import division
import pygame as pg
from singletonmixin import SingletonException
from displaymanager import DisplayManager
from environment import Environment
from inputmanager import InputManager

# debug switches #
SHOW_FPS = True

# constants #
MAXFPS = 60
SCREENSIZE = (800, 600)

# handle #
INPUT = InputManager.getInstance()

def main():
    pg.init()
    pg.font.init()
    INPUT.init()

    env = Environment()
    disp = DisplayManager(env, SCREENSIZE)

    if SHOW_FPS:
        update_fps = pg.USEREVENT + 1
        pg.time.set_timer(update_fps, 700)
    
    # vars #
    done = False
    clock = pg.time.Clock()
    clock.tick()  # necessary, or the first tick will be very large
    
    # program loop #
    while not done:
        # events #
        for e in pg.event.get():
            if e.type == pg.QUIT: done = True
            elif e.type == pg.KEYDOWN:
                key = e.key
                if key == pg.K_ESCAPE:
                    pg.event.post(pg.event.Event(pg.QUIT))
                elif key == pg.K_UP:
                    INPUT.up_last = True
                elif key == pg.K_DOWN:
                    INPUT.up_last = False
                elif key == pg.K_RIGHT:
                    INPUT.right_last = True
                elif key == pg.K_LEFT:
                    INPUT.right_last = False
            elif e.type == pg.MOUSEMOTION:
                pass
            elif e.type == pg.MOUSEBUTTONDOWN:
                pass
            elif e.type == pg.MOUSEBUTTONUP:
                pass
            elif SHOW_FPS:
                if e.type == update_fps:
                    disp.set_fps(clock.get_fps())

        # logic #
        INPUT.update()
        
        elapsedticks = clock.get_time()
        env.update(elapsedticks)
        
        # draw #
        disp.draw()
        
        # tick #
        clock.tick(MAXFPS)
        
    # end program loop #

    pg.quit()
    
if __name__ == '__main__':
    main()
