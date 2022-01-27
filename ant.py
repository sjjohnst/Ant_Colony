import pygame
import random
import numpy as np
import math
from parameters import *
from vector import *

PI = math.pi


'''
Ant class
1. Implement Ant wandering aimlessly. Make it smooth
2. Add food items, have ants detect and steer towards food
3. Add in pheromones, have ants leave trails and follow trails
'''


class Ant:
    def __init__(self, position: Vector):

        # Constant attributes
        self.color = white
        self.maxSpeed = 0.1
        self.steerStrength = 0.06
        self.wanderStrength = 0.02

        self.position = position
        self.velocity = rand_inUnitCircle()
        self.desiredDirection = rand_inUnitCircle()

    def update(self, t):

        self.desiredDirection = (self.desiredDirection + rand_inUnitCircle() * self.wanderStrength).normalize()

        desiredVelocity = self.desiredDirection * self.maxSpeed
        desiredSteeringForce = (desiredVelocity - self.velocity) * self.steerStrength
        acceleration = desiredSteeringForce.clamp(self.steerStrength)

        self.velocity = (self.velocity + acceleration * t).clamp(self.maxSpeed)
        self.position = self.position + self.velocity * t

    def show(self, screen):
        # print(self.position.get_coord())
        pygame.draw.circle(screen, self.color, self.position.get_coord(), 5)
