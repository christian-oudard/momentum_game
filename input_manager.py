import pygame as pg

class InputManager(object):
    """Manager class for keyboard and joystick input
    
    Handles tracking of keyboard state, and mapping of keys and joystick
    buttons to game inputs. Keeps an internal model of the joystick
    axes, each having values of 1, 0, or -1.
    
    Properties:
    x_axis -- -1 for left, +1 for right, 0 for neutral
    y_axis -- -1 for down, +1 for up, 0 for neutral
    """
    
    def __init__(self):
        self.x_axis = 0
        self.y_axis = 0
        self.right_last = True
        self.up_last = True
        
        #TEMP: hardcoded keymap.
        self.keymap = {
            'up': pg.K_UP,
            'down': pg.K_DOWN,
            'right': pg.K_RIGHT,
            'left': pg.K_LEFT,
        }

    def update(self):
        keys = pg.key.get_pressed()
        
        # check x-axis
        right_key = keys[self.keymap['right']]
        left_key = keys[self.keymap['left']]
        
        if not right_key and not left_key:
            self.x_axis = 0
        elif right_key and not left_key:
            self.x_axis = +1
        elif not right_key and left_key:
            self.x_axis = -1
        else:
            if self.right_last:
                self.x_axis = +1
            else:
                self.x_axis = -1
        
        # check y-axis
        up_key = keys[self.keymap['up']]
        down_key = keys[self.keymap['down']]
        
        if not up_key and not down_key:
            self.y_axis = 0
        elif up_key and not down_key:
            self.y_axis = +1
        elif not up_key and down_key:
            self.y_axis = -1
        else:
            if self.up_last:
                self.y_axis = +1
            else:
                self.y_axis = -1

INPUT = InputManager()
