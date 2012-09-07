import pygame as pg
from display import Display
from environment import Environment
from input_manager import INPUT

# constants #
MAXFPS = 60
SCREENSIZE = (800, 600)

def main():
    pg.init()
    pg.font.init()

    env = Environment()
    disp = Display(env, SCREENSIZE)

    update_fps_event = pg.USEREVENT + 1
    pg.time.set_timer(update_fps_event, 700)

    # vars #
    done = False
    clock = pg.time.Clock()
    clock.tick()  # necessary, or the first tick will be very large

    # program loop #
    while not done:
        # events #
        for e in pg.event.get():
            if e.type == pg.QUIT:
                done = True
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
            elif e.type == update_fps_event:
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
