import pygame
import random
import numpy as np
import math
from parameters import *

'''
Ant class
1. Implement Ant wandering aimlessly. Make it smooth
'''


class Ant:
    def __init__(self, position):

        # Constant attributes
        self.color = white
        self.max_speed = 10

        # Position and velocity
        self.velocity = np.random.randn(2)
        self.position = position

        # Wandering parameters
        self.desired_direction = np.random.randn(2)
        self.wander_strength = 0.15
        self.steer_strength = 0.08

    def update(self):

        # update position and velocity
        self.position = self.position + self.velocity
        self.velocity = self.velocity + (self.desired_direction - self.velocity)*self.steer_strength

        # update desired velocity
        self.desired_direction = self.desired_direction + np.random.randn(2)*self.wander_strength

    def show(self, screen):
        pygame.draw.circle(screen, self.color, self.position, 2)