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
        self.max_speed = 1.0

        # Position, speed and direction
        self.position = position
        init_speed = np.random.random_sample() * self.max_speed
        init_direction = np.random.random_sample() * 2 * PI

        self.velocity = Vector(init_speed*math.cos(init_direction), init_speed*math.sin(init_direction))

        # Wandering parameters
        init_speed = np.random.random_sample() * self.max_speed
        init_direction = np.random.random_sample() * 2 * PI
        self.desired_velocity = Vector(init_speed*math.cos(init_direction), init_speed*math.sin(init_direction))
        self.wander_strength = 0.1
        self.steer_strength = 0.05

        # print(self.velocity, self.desired_velocity)

    def update(self):

        # Update position and velocity
        self.position = self.position + self.velocity

        # Update velocity towards desired
        self.velocity = slerp(self.velocity, self.desired_velocity, self.steer_strength)

        # Update desired by random perturbation
        r = list(np.random.randn(2))
        random_perturbation = Vector(r[0], r[1])
        # random_perturbation.clamp(self.wander_strength)
        # self.desired_velocity = self.desired_velocity + random_perturbation

        # Clamp desired velocity and true velocity
        self.velocity.clamp(self.max_speed)
        self.desired_velocity.clamp(self.max_speed)

    def show(self, screen):
        # print(self.position.get_coord())
        pygame.draw.circle(screen, self.color, self.position.get_coord(), 2)
