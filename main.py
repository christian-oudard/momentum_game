import pygame as pg
from display import Display
from environment import Environment
from input_manager import InputManager
import levels

# constants #
MAXFPS = 1000
SCREENSIZE = (1024, 768)

def main():
    pg.init()
    pg.font.init()

    #TEMP: hardcoded keymaps.
    inputs = [
        InputManager({
            'x_axis': (pg.K_LEFT, pg.K_RIGHT),
            'y_axis': (pg.K_DOWN, pg.K_UP),
            'brake': pg.K_RCTRL,
        }),
        InputManager({
            'thrust': pg.K_e,
            'brake': pg.K_d,
            'turn_direction': (pg.K_s, pg.K_f),
        }),
    ]

    env = Environment(inputs)
    disp = Display(env, SCREENSIZE)
    env.load_level(levels.versus) # TEMP, hardcoded level selection.

    # FPS tracking.
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
                else:
                    for inp in inputs:
                        inp.track_keypress(e.key)
            elif e.type == pg.MOUSEMOTION:
                pass
            elif e.type == pg.MOUSEBUTTONDOWN:
                pass
            elif e.type == pg.MOUSEBUTTONUP:
                pass
            elif e.type == update_fps_event:
                disp.set_fps(clock.get_fps())

        # updates #
        for inp in inputs:
            inp.update()
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
