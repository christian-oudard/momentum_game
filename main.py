from __future__ import division, print_function
import random

import pygame as pg
from display import Display
from environment import Environment
from input_manager import InputManager
import levels

PHYSICS_FPS = 60
PHYSICS_TICK_MS = 1000 / PHYSICS_FPS
SCREENSIZE = (1024, 768)


def main():
    pg.init()
    pg.font.init()

    #TEMP: hardcoded keymaps.
    inputs = [
        #InputManager({
        #    'x_axis': (pg.K_j, pg.K_l),
        #    'y_axis': (pg.K_k, pg.K_i),
        #    'brake': pg.K_SPACE,
        #}),
        InputManager({
            'thrust': pg.K_UP,
            'brake': pg.K_DOWN,
            'turn_direction': (pg.K_LEFT, pg.K_RIGHT),
        }),
        InputManager({
            'thrust': pg.K_PERIOD,
            'brake': pg.K_e,
            'turn_direction': (pg.K_o, pg.K_u),
        }),
    ]

    env = Environment(inputs)
    disp = Display(env, SCREENSIZE)
    env.load_level(levels.versus) # TEMP, hardcoded level selection.

    main_loop(env, disp)

    pg.quit()


def main_loop(env, disp):
    """
    Run the main game loop.

    We decouple the display framerate from the physics update framerate,
    putting as many physics frames as necessary between display frames.

    The display framerate is capped at the physics framerate.
    """
    # FPS tracking.
    update_fps_event = pg.USEREVENT + 1
    pg.time.set_timer(update_fps_event, 700)

    clock = pg.time.Clock()
    clock.tick()  # necessary, or the first tick will be very large

    start_time = pg.time.get_ticks()

    # One iteration of the loop is one physics frame.
    # Not every iteraton will incur a draw() call if we aren't caught up.
    frame_count = 0
    while True:
        frame_count += 1
        # Process events.
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return
            elif e.type == pg.KEYDOWN:
                key = e.key
                if key == pg.K_ESCAPE:
                    pg.event.post(pg.event.Event(pg.QUIT))
                else:
                    for inp in env.inputs:
                        inp.track_keypress(e.key)
            elif e.type == pg.MOUSEMOTION:
                pass
            elif e.type == pg.MOUSEBUTTONDOWN:
                pass
            elif e.type == pg.MOUSEBUTTONUP:
                pass
            elif e.type == update_fps_event:
                disp.set_fps(clock.get_fps())

        # Check pressed keys.
        pressed_keys = pg.key.get_pressed()
        for inp in env.inputs:
            inp.update(pressed_keys)

        # Update the environment.
        # the current time.
        env.update(PHYSICS_TICK_MS)

        # Check if we are caught up to the current time, and if so, take the
        # time to draw the screen.
        elapsed_time = pg.time.get_ticks() - start_time
        target_frame = (elapsed_time / 1000) * PHYSICS_FPS
        if frame_count > target_frame:
            disp.draw()
            clock.tick(PHYSICS_FPS)  # Limit display framerate.


if __name__ == '__main__':
    main()
