from __future__ import print_function

import traceback

import vec
import constants as c
from environment import Environment
from particle import Particle
from bumper import Bumper


def assert_vectors_equal(a, b):
    for da, db in zip(a, b):
        assert abs(da - db) < c.epsilon, '{} != {}'.format(a, b)


def test_bumper():
    northwest = vec.norm((-1, -1))
    northeast = vec.norm((1, -1))

    env = Environment()
    env.load_level([
        (Bumper, dict(pos=(0,0), velocity=(0,0), radius=3)),
        (Particle, dict(pos=(6, 0), velocity=vec.norm(northwest, c.max_speed), mass=1, radius=3.1)),
    ])

    # The particle starts out heading northwest.
    bumper, particle = env.particles
    assert_vectors_equal(vec.norm(particle.velocity), northwest)

    # After it bounces, it goes northeast.
    for _ in range(10):
        env.update(1)
        assert_vectors_equal(vec.norm(particle.velocity), northeast)


def test_collision():
    env = Environment()
    env.load_level([
        (Particle, dict(pos=(-1, 0), velocity=(20, 0), mass=1, radius=1, restitution=1, drag_rate=0)),
        (Particle, dict(pos=(1, 0), velocity=(0, 0), mass=1, radius=1, restitution=1, drag_rate=0)),
    ])

    # The left particle starts out heading to the right.
    left, right = env.particles
    assert_vectors_equal(left.velocity, (20, 0))
    assert_vectors_equal(right.velocity, (0, 0))

    # After it bounces, it has transferred all its momentum to the right particle.
    for _ in range(10):
        env.update(1)
        assert_vectors_equal(left.velocity, (0, 0))
        assert_vectors_equal(right.velocity, (20, 0))


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
