import pygame
import random
import numpy as np
import math
from parameters import *
from datastructs import Vector
import copy

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
        self.max_speed = 3.5

        # Position, speed and direction
        self.position = position
        init_speed = np.random.random_sample() * self.max_speed
        init_direction = np.random.random_sample() * 2 * PI
        self.velocity = Vector(init_speed*math.cos(init_direction), init_speed*math.sin(init_direction))

        # Wandering parameters
        self.desired_direction = Vector()
        self.wander_strength = 0.15
        self.steer_strength = 3.5

        self.t0 = pygame.time.get_ticks() / 100.0

        self.targetFood = None

    def update(self):

        dt = pygame.time.get_ticks() / 100.0 - self.t0
        self.t0 = pygame.time.get_ticks() / 100.0

        self.handle_food()
        random_unit_vector = Vector(random.uniform(-1.0, 1.0),
                                    random.uniform(-1.0, 1.0))
        self.desired_direction = self.desired_direction + random_unit_vector * self.wander_strength
        self.desired_direction.normalize()

        desired_velocity = self.desired_direction * self.max_speed
        desired_steering_force = (desired_velocity - self.velocity) * self.steer_strength
        acceleration = copy.copy(desired_steering_force)
        acceleration.clamp(self.steer_strength)

        self.velocity = self.velocity + acceleration * dt
        self.velocity.clamp(self.max_speed)
        self.position = self.position + self.velocity * dt

    def handle_food(self):
        if self.targetFood is None:
            pass
        else:
            self.desired_direction = self.targetFood - self.position
            self.desired_direction.normalize()

    def show(self, screen):
        # print(self.position.get_coord())
        pygame.draw.circle(screen, self.color, self.position.get_coord(), 2)
