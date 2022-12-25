import pygame
from pygame import Vector2
import random
import numpy as np
import math
from parameters import *

PI = math.pi

'''
Ant class
1. Implement Ant wandering aimlessly. Make it smooth
2. Add food items, have ants detect and steer towards food
3. Add in pheromones, have ants leave trails and follow trails
'''


class Ant(pygame.sprite.Sprite):
    def __init__(self, position: Vector2):
        super().__init__()

        self.images = []
        self.images.append(pygame.image.load("ant_sprite_0.png"))
        self.images.append(pygame.image.load("ant_sprite_1.png"))
        self.images.append(pygame.image.load("ant_sprite_0.png"))
        self.images.append(pygame.image.load("ant_sprite_2.png"))
        self.index = 0

        self.food_image = pygame.image.load("ant_sprite_food.png")

        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=position)

        self.width = self.rect.width
        self.height = self.rect.height

        self.max_speed = 3.5

        # Position, speed and direction
        self.position = position
        self.velocity = Vector2(random.uniform(-1.0, 1.0),
                                random.uniform(-1.0, 1.0))

        # Wandering parameters
        self.desired_direction = Vector2(random.uniform(-1.0, 1.0),
                                         random.uniform(-1.0, 1.0))
        self.desired_direction.scale_to_length(self.max_speed)
        self.wander_strength = 10 # Maximum degrees of change possible for updating desired direction
        self.steer_strength = 1.5

        # Last time updated
        self.t0 = pygame.time.get_ticks() / 100.0
        # Last time placed a pheromone
        self.t_last_p = pygame.time.get_ticks() / 1000.0

        # For grabbing food from the map
        self.target = None
        self.holding_food = False
        self.radius = 25
        self.p_radius = 25
        self.viewAngle = 60

    def time_to_place_pheromone(self):
        dt = pygame.time.get_ticks() / 1000.0 - self.t_last_p
        return dt >= 0.5

    def update_position(self):
        dt = pygame.time.get_ticks() / 100.0 - self.t0
        self.t0 = pygame.time.get_ticks() / 100.0

        desired_steering_force = self.desired_direction.slerp(self.velocity, 0) * self.steer_strength
        acceleration = desired_steering_force.clamp_magnitude(0, self.max_speed)

        self.velocity = self.velocity + acceleration * dt
        self.velocity.clamp_magnitude_ip(self.max_speed)
        self.position = self.position + self.velocity * dt

    def wander(self):
        # Update desired direction by rotating by a random angle, range set by wander strength
        angle = random.uniform(-self.wander_strength, self.wander_strength)
        self.desired_direction.rotate_ip(angle)
        self.update_position()

    def follow_target(self):
        # Update desired direction by rotating by a random angle, range set by wander strength
        self.desired_direction = self.target - self.position
        self.update_position()

    def update(self):
        if not self.holding_food:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
        else:
            self.image = self.food_image

        # move image rectangle to position, and update rotation to match velocity
        angle = self.velocity.as_polar()[1] + 90
        self.image = pygame.transform.rotate(self.image, -angle)
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = self.position

    # def update_dir(self, food_tree, pheromone_tree):
    #     # Update the ants desired direction based on state and nearby items
    #     if self.holding_food:
    #         # We are holding food, follow blue pheromones
    #         self.follow_pheromones(pheromone_tree, 0)
    #
    #         # Target the colony if nearby and holding food
    #         target_radius = 50
    #         if self.position.distance_to(self.colony.position) < target_radius:
    #             self.desired_direction = (self.colony.position - self.position) * self.max_speed
    #
    #         # Drop off food if in range, turn 180 degrees
    #         drop_off_radius = 20
    #         if self.position.distance_to(self.colony.position) < drop_off_radius:
    #             self.holding_food = False
    #             self.targetFood = None
    #             self.velocity.rotate(PI)
    #             self.desired_direction.rotate(PI)
    #
    #     elif self.targetFood is None:
    #         allFood = food_tree.query_radius(self.position, self.radius)
    #         if len(allFood) > 0:
    #             food = random.choice(allFood)
    #             dir_to_food = food - self.position
    #             dir_to_food.normalize()
    #
    #             if dir_to_food.angle_to(self.position) < self.viewAngle / 2:
    #                 self.targetFood = food
    #                 self.desired_direction = self.targetFood - self.position
    #             else:
    #                 # No nearby food to target, follow red pheromones if any
    #                 self.follow_pheromones(pheromone_tree, 1)
    #
    #         else:
    #             # No nearby food to target, follow red pheromones if any
    #             self.follow_pheromones(pheromone_tree, 1)
    #
    #     else:
    #         # We are targetting food, keep targetting it
    #
    #         self.desired_direction = self.targetFood - self.position
    #         self.desired_direction.normalize()
    #
    #         # pickup food if in range
    #         pickup_radius = 10
    #         if self.position.distance_to(self.targetFood) < pickup_radius:
    #             self.holding_food = True
    #             food_tree.delete(self.targetFood)
    #             self.targetFood = None
    #             # self.desired_direction.rotate(PI)
    #
    # def place_pheromones(self, pheromone_tree):
    #     dt = pygame.time.get_ticks() / 1000.0 - self.t_last_p
    #     if dt < 0.2:
    #         return
    #
    #     position_copy = copy.copy(self.position)
    #     if self.holding_food is True:
    #         # Place red pheromones, follow blue pheromones
    #         pheromone_tree.insert(position_copy, 1)
    #         self.t_last_p = pygame.time.get_ticks() / 1000.0
    #
    #     elif self.targetFood is None:
    #         # Place blue pheromones, follow red pheromones
    #         pheromone_tree.insert(position_copy, 0)
    #         self.t_last_p = pygame.time.get_ticks() / 1000.0
    #
    #     else: # not holding food, but targetting a food item
    #         # Place blue pheromones
    #         self.t_last_p = pygame.time.get_ticks() / 1000.0
    #         pheromone_tree.insert(position_copy, 1)
    #
    # def follow_pheromones(self, pheromone_tree, type):
    #     # Update desired direction to be in area with most pheromones of 'type' [0,1]
    #
    #     # Get current forward direction of the ant as an angle
    #     direction = copy.copy(self.velocity)
    #     direction.normalize()
    #     theta = 30*PI/180
    #
    #     # Get base unit vectors for 15degrees, 0degrees and -15degrees
    #     left_vec = copy.copy(direction)
    #     centre_vec = copy.copy(direction)
    #     right_vec = copy.copy(direction)
    #
    #     # Rotate vectors based on direction of ant
    #     left_vec.rotate(theta)
    #     right_vec.rotate(-theta)
    #
    #     # get center position of each query circle
    #     pos_left = left_vec * self.p_distance + self.position
    #     pos_centre = centre_vec * self.p_distance + self.position
    #     pos_right = right_vec * self.p_distance + self.position
    #
    #     # Query each circle for pheromones of desired type
    #     left_items = pheromone_tree.query_radius(pos_left, self.p_radius, type)
    #     centre_items = pheromone_tree.query_radius(pos_centre, self.p_radius, type)
    #     right_items = pheromone_tree.query_radius(pos_right, self.p_radius, type)
    #
    #     if left_items == 0 and centre_items == 0 and right_items == 0:
    #         return
    #
    #     if left_items >= centre_items and left_items >= right_items:
    #         self.desired_direction = left_vec * self.max_speed
    #     elif centre_items >= right_items and centre_items >= left_items:
    #         self.desired_direction = centre_vec * self.max_speed
    #     elif right_items >= centre_items and right_items >= left_items:
    #         self.desired_direction = right_vec * self.max_speed
    #     else:
    #         pass
