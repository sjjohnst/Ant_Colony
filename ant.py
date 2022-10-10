import pygame
import random
import numpy as np
import math
from parameters import *
from datastructs import Vector, angle
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
        self.wander_strength = 0.25
        self.steer_strength = 3.5

        # Last time updated
        self.t0 = pygame.time.get_ticks() / 100.0
        # Last time placed a pheromone
        self.t_last_p = pygame.time.get_ticks() / 1000.0

        # For grabbing food from the map
        self.targetFood = None
        self.holding_food = False
        self.radius = 30
        self.viewAngle = PI / 15

    def update(self):

        dt = pygame.time.get_ticks() / 100.0 - self.t0
        self.t0 = pygame.time.get_ticks() / 100.0

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

    def handle_food(self, food_tree):
        if self.targetFood is None:
            allFood = food_tree.query_radius(self.position, self.radius)
            if len(allFood) > 0:
                food = random.choice(allFood)
                dir_to_food = food - self.position
                dir_to_food.normalize()

                if angle(dir_to_food, self.velocity) < self.viewAngle / 2:
                    self.targetFood = food

        else:
            self.desired_direction = self.targetFood - self.position
            self.desired_direction.normalize()

            pickup_radius = 0.1
            if self.position.distance_to(self.targetFood) < pickup_radius:
                self.holding_food = True
                food_tree.delete(self.targetFood)
                self.targetFood = None

    def handle_pheromones(self, pheromone_tree):
        dt = pygame.time.get_ticks() / 1000.0 - self.t_last_p
        if dt < 0.5:
            return

        position_copy = copy.copy(self.position)
        if self.holding_food is True:
            # Place red pheromones, follow blue pheromones
            pheromone_tree.insert(position_copy, 1)
            self.t_last_p = pygame.time.get_ticks() / 1000.0
            self.follow_pheromones(0)

        elif self.targetFood is None:
            # Place blue pheromones, follow red pheromones
            pheromone_tree.insert(position_copy, 0)
            self.t_last_p = pygame.time.get_ticks() / 1000.0
            self.follow_pheromones(1)

        else: # not holding food, but targetting a food item
            # Place blue pheromones
            self.t_last_p = pygame.time.get_ticks() / 1000.0
            pheromone_tree.insert(position_copy, 0)

    def follow_pheromones(self, type):
        # Update desired direction to be in area with most pheromones of 'type' [0,1]
        pass

    def show(self, screen):
        # print(self.position.get_coord())
        velocity_dir = Vector(self.velocity.x, self.velocity.y)
        velocity_dir.normalize()

        if self.holding_food:
            food_pos = velocity_dir*3.0 + self.position
            pygame.draw.circle(screen, green, food_pos.get_coord(), 2.0)

        butt_segment = velocity_dir*-2.0 + self.position
        pygame.draw.circle(screen, self.color, butt_segment.get_coord(), 2)
        pygame.draw.circle(screen, self.color, self.position.get_coord(), 2)
