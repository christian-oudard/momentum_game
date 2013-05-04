from __future__ import print_function

import traceback

import vec
import constants as c
from environment import Environment
from particle import Particle
from bumper import Bumper


def assert_vectors_equal(a, b):
    for da, db in zip(a, b):
        assert abs(da - db) < c.epsilon


def test_bumper_orbit():
    northwest = vec.norm((-1, -1))
    northeast = vec.norm((1, -1))

    # Sometimes when a particle is sent into a bumper really fast, it gets
    # stuck in an infinite bounce inside the bumper, and spins around it really fast.
    env = Environment([])
    env.load_level([
        (Bumper, dict(pos=(0,0), velocity=(0,0), radius=3)),
        (Particle, dict(pos=(6, 0), velocity=vec.norm(northwest, c.max_speed), mass=1, radius=3.1)),
    ])

    bumper, orbiter = env.particles

    # Starts heading northwest.
    assert_vectors_equal(vec.norm(orbiter.velocity), northwest)

    # After one tick, it bounces and is headed northeast
    env.update(1)
    assert_vectors_equal(vec.norm(orbiter.velocity), northeast)

    # It continues to the northeast, and does not get stuck.
    for _ in range(10):
        env.update(1)
        assert_vectors_equal(vec.norm(orbiter.velocity), northeast)


if __name__ == '__main__':
    for value in globals().values():
        if hasattr(value, '__call__') and value.__name__.startswith('test_'):
            print(value.__name__)
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
