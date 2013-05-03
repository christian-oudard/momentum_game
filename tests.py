from __future__ import print_function

import traceback

from environment import Environment
from particle import Particle
from bumper import Bumper


def test_bumper_orbit():
    # Sometimes when a particle is sent into a bumper really fast, it gets
    # stuck in an infinite bounce inside the bumper, and spins around it really fast.
    env = Environment([])
    env.load_level([
        (Bumper, dict(pos=(0,0), velocity=(0,0), radius=3)),
        (Particle, dict(pos=(6, 0), velocity=(-1000,-1000), mass=1, radius=3.1)),
    ])
    bumper, orbiter = env.particles
    print(orbiter.velocity)
    env.update(1)
    print(orbiter.velocity)
    env.update(1)
    print(orbiter.velocity)
    env.update(1)
    print(orbiter.velocity)
    env.update(1)
    print(orbiter.velocity)
    env.update(1)
    print(orbiter.velocity)

    assert False

if __name__ == '__main__':
    for value in globals().values():
        if hasattr(value, '__call__') and value.__name__.startswith('test_'):
            print(value.__name__, end='')
            try:
                value()
            except AssertionError:
                print('FAIL')
                traceback.print_exc()
            except:
                print('ERROR')
                traceback.print_exc()
            else:
                print('OK')
