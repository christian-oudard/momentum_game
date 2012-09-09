import pygame as pg

class InputManager(object):
    """Manager class for keyboard and joystick input

    Handles tracking of keyboard state, and mapping of keys and joystick
    buttons to game inputs.

    Keeps an internal model of any axes defined, with values of 1, 0, or -1.

    The keymap is a dictionary mapping button names to a single key, or axis
    names to a pair of keys for the negative and positive direction.
    """

    def __init__(self, keymap):
        # For each axis, we use key events to track the last direction that was
        # pressed, to disambiguate when both keys are pressed at once.
        # Initialize the list of axis names, the axis readout attributes, and
        # the last known direction.
        self.buttons = {}
        self.axes = {}
        self.axes_last = {}
        for key, value in keymap.items():
            if isinstance(value, tuple):
                self.axes[key] = value
                setattr(self, key, 0)
                self.axes_last[key] = False
            else:
                self.buttons[key] = value

    def track_keypress(self, key):
        for axis, keys in self.axes.items():
            if key == keys[0]:
                self.axes_last[axis] = -1
            elif key == keys[1]:
                self.axes_last[axis] = +1

    def update(self):
        pressed_keys = pg.key.get_pressed()

        # Check axis values.
        for axis, keys in self.axes.items():
            neg = pressed_keys[keys[0]]
            pos = pressed_keys[keys[1]]
            if not pos and not neg:
                value = 0
            elif pos and not neg:
                value = +1
            elif neg and not pos:
                value = -1
            else:
                value = self.axes_last[axis]
            setattr(self, axis, value)

        # Check button values.
        for button, key in self.buttons.items():
            value = bool(pressed_keys[key])
            setattr(self, button, value)
