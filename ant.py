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

        self.maxSpeed = 15
        self.steerStrength = 10
        self.wanderStrength = 0.1

        self.position = position
        self.velocity = np.random.rand(2) * 10
        self.desiredDirection = np.random.rand(2)

        self.color = white

    def update(self):
        # Update desired direction
        random_mag = random.uniform(0, 1)
        random_theta = random.uniform(0, 2*math.pi)
        random_vector = np.array([random_mag * math.cos(random_theta), random_mag * math.sin(random_theta)])
        dd = (self.desiredDirection + random_vector * self.wanderStrength)
        self.desiredDirection = dd / np.linalg.norm(dd)

        desiredVelocity = self.desiredDirection * self.maxSpeed
        desiredSteeringForce = (desiredVelocity - self.velocity) * self.steerStrength
        acceleration = self.clampMagnitude(desiredSteeringForce, self.steerStrength)

        self.velocity = self.clampMagnitude(self.velocity + acceleration * 0.05, self.maxSpeed)
        self.position += self.velocity * 0.05

    def clampMagnitude(self, vector, maxLength):
        mag = np.linalg.norm(vector)

        if mag > maxLength:
            theta = math.atan(vector[0] / vector[1])
            vector = np.array([maxLength * math.cos(theta), maxLength * math.sin(theta)])

        return vector

    def show(self, screen):
        pygame.draw.circle(screen, self.color, self.position, 2)