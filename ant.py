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
    def __init__(self, position=np.random.rand(2), nest=None):
        self.position = position * resolution
        self.velocity = np.random.randn(2)
        self.max_speed = 3
        self.nest = nest
        self.color = white

    def updateVelocity(self):

        delta_angle = math.pi/4
        delta_mag = 1.0

        i = self.velocity[0]
        j = self.velocity[1]
        mag = math.sqrt(i*i + j*j)
        angle = math.atan(i/j)

        new_angle = angle + random.uniform(-0.5, 0.5) * delta_angle
        new_mag = mag + random.uniform(-0.5, 0.5) * delta_mag

        new_i = new_mag * math.cos(new_angle)
        new_j = new_mag * math.sin(new_angle)

        self.velocity = np.array([new_i, new_j])

    def update(self):
        # Update position based on velocity
        self.position = self.position + self.velocity
        self.updateVelocity()

    def show(self, screen):
        pygame.draw.circle(screen, self.color, self.position, 2)