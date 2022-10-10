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
    def __init__(self, position: Vector, colony):

        # Constant attributes
        self.color = white
        self.max_speed = 5.0
        self.colony = colony

        # Position, speed and direction
        self.position = position
        init_speed = np.random.random_sample() * self.max_speed
        init_direction = np.random.random_sample() * 2 * PI
        self.velocity = Vector(init_speed*math.cos(init_direction), init_speed*math.sin(init_direction))

        # Wandering parameters
        self.desired_direction = Vector()
        self.wander_strength = 0.15
        self.steer_strength = 5.0

        # Last time updated
        self.t0 = pygame.time.get_ticks() / 100.0
        # Last time placed a pheromone
        self.t_last_p = pygame.time.get_ticks() / 1000.0

        # For grabbing food from the map
        self.targetFood = None
        self.holding_food = False
        self.radius = 20
        self.p_distance = 15
        self.p_radius = 5
        self.viewAngle = 15 * PI / 180

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

    def update_dir(self, food_tree, pheromone_tree):
        # Update the ants desired direction based on state and nearby items
        if self.holding_food:
            # We are holding food, follow blue pheromones
            self.follow_pheromones(pheromone_tree, 0)

            # drop off food if in range, turn 180 degrees
            drop_off_radius = 10
            if self.position.distance_to(self.colony.position) < drop_off_radius:
                self.holding_food = False
                self.targetFood = None
                self.velocity.rotate(PI)

        elif self.targetFood is None:
            allFood = food_tree.query_radius(self.position, self.radius)
            if len(allFood) > 0:
                food = random.choice(allFood)
                dir_to_food = food - self.position
                dir_to_food.normalize()

                if angle(dir_to_food, self.velocity) < self.viewAngle / 2:
                    self.targetFood = food
            else:
                # No nearby food to target, follow red pheromones if any
                self.follow_pheromones(pheromone_tree, 1)

        else:
            # We are targetting food, keep targetting it

            self.desired_direction = self.targetFood - self.position
            self.desired_direction.normalize()

            # pickup food if in range
            pickup_radius = 0.1
            if self.position.distance_to(self.targetFood) < pickup_radius:
                self.holding_food = True
                food_tree.delete(self.targetFood)
                self.targetFood = None

    def place_pheromones(self, pheromone_tree):
        dt = pygame.time.get_ticks() / 1000.0 - self.t_last_p
        if dt < 0.2:
            return

        position_copy = copy.copy(self.position)
        if self.holding_food is True:
            # Place red pheromones, follow blue pheromones
            pheromone_tree.insert(position_copy, 1)
            self.t_last_p = pygame.time.get_ticks() / 1000.0

        elif self.targetFood is None:
            # Place blue pheromones, follow red pheromones
            pheromone_tree.insert(position_copy, 0)
            self.t_last_p = pygame.time.get_ticks() / 1000.0

        else: # not holding food, but targetting a food item
            # Place blue pheromones
            self.t_last_p = pygame.time.get_ticks() / 1000.0
            pheromone_tree.insert(position_copy, 1)

    def follow_pheromones(self, pheromone_tree, type):
        # Update desired direction to be in area with most pheromones of 'type' [0,1]

        # Get current forward direction of the ant as an angle
        direction = copy.copy(self.velocity)
        direction.normalize()
        theta = 30*PI/180

        # Get base unit vectors for 15degrees, 0degrees and -15degrees
        left_vec = copy.copy(direction)
        centre_vec = copy.copy(direction)
        right_vec = copy.copy(direction)

        # Rotate vectors based on direction of ant
        left_vec.rotate(theta)
        right_vec.rotate(-theta)

        # get center position of each query circle
        pos_left = left_vec * self.p_distance + self.position
        pos_centre = centre_vec * self.p_distance + self.position
        pos_right = right_vec * self.p_distance + self.position

        # Query each circle for pheromones of desired type
        left_items = pheromone_tree.query_radius(pos_left, self.p_radius, type)
        centre_items = pheromone_tree.query_radius(pos_centre, self.p_radius, type)
        right_items = pheromone_tree.query_radius(pos_right, self.p_radius, type)

        if left_items == 0 and centre_items == 0 and right_items == 0:
            return

        if left_items >= centre_items and left_items >= right_items:
            self.desired_direction = left_vec * self.max_speed
        elif centre_items >= right_items and centre_items >= left_items:
            self.desired_direction = centre_vec * self.max_speed
        elif right_items >= centre_items and right_items >= left_items:
            self.desired_direction = right_vec * self.max_speed
        else:
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
