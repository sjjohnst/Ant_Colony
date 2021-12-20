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
        self.max_speed = 2

        # Position and velocity
        self.velocity = np.random.randn(2)
        self.position = position

        # Wandering parameters
        self.desired_direction = np.random.randn(2)
        self.wander_strength = 0.08
        self.steer_strength = 0.02

    def update(self):

        # update position and velocity
        self.position = self.position + self.velocity
        self.velocity = self.velocity + (self.desired_direction - self.velocity)*self.steer_strength
        self.velocity = self.clamp_vector(self.velocity)

        # update desired velocity
        self.desired_direction = self.desired_direction + np.random.randn(2)*self.wander_strength
        self.desired_direction = self.clamp_vector(self.desired_direction)

    def clamp_vector(self, vector):
        current_speed = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        if current_speed > self.max_speed:
            theta = math.atan(vector[1] / vector[0])
            vector[0] = self.max_speed * math.cos(theta)
            vector[1] = self.max_speed * math.sin(theta)

        return vector

    def show(self, screen):
        pygame.draw.circle(screen, self.color, self.position, 2)