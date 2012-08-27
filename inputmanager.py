from singletonmixin import Singleton
import pygame
from pygame.locals import *

class InputManager(Singleton):
    """Manager class for keyboard and joystick input
    
    Handles tracking of keyboard state, and mapping of keys and joystick
    buttons to game inputs. Keeps an internal model of the joystick
    axes, each having values of 1, 0, or -1.
    
    Properties:
    x_axis -- -1 for left, +1 for right, 0 for neutral
    y_axis -- -1 for down, +1 for up, 0 for neutral
    """
    
    def __init__(self):
        self.__x_axis = 0
        self.__y_axis = 0
        self.right_last = True
        self.up_last = True
        
    def init(self):
        ##TEMP
        self.keymap = {'up':K_UP,
                       'down':K_DOWN,
                       'right':K_RIGHT,
                       'left':K_LEFT}
        ##
    def update(self):
        keys = pygame.key.get_pressed()
        
        # check x-axis
        right_key = keys[self.keymap['right']]
        left_key = keys[self.keymap['left']]
        
        if not right_key and not left_key:
            self.__x_axis = 0
        elif right_key and not left_key:
            self.__x_axis = +1
        elif not right_key and left_key:
            self.__x_axis = -1
        else:
            if self.right_last:
                self.__x_axis = +1
            else:
                self.__x_axis = -1
        
        # check y-axis
        up_key = keys[self.keymap['up']]
        down_key = keys[self.keymap['down']]
        
        if not up_key and not down_key:
            self.__y_axis = 0
        elif up_key and not down_key:
            self.__y_axis = +1
        elif not up_key and down_key:
            self.__y_axis = -1
        else:
            if self.up_last:
                self.__y_axis = +1
            else:
                self.__y_axis = -1
                
        
    # property management functions #
    def get_x_axis(self):
        return self.__x_axis
    def get_y_axis(self):
        return self.__y_axis
    def get_up(self):
        return self.__y_axis == 1
    def get_down(self):
        return self.__y_axis == -1
    def get_right(self):
        return self.__x_axis == 1
    def get_left(self):
        return self.__x_axis == -1
    
    # properties #
    x_axis = property(get_x_axis)
    y_axis = property(get_y_axis)
    up = property(get_up)
    down = property(get_down)
    right = property(get_right)
    left = property(get_left)
        