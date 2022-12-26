import pygame
from pygame import Vector2
from objects import Pheromone, Ant, AntHill
from parameters import *
import math

PI = math.pi


def ant_detect_food(ant, food):
    # Food is a circle with position and radius
    # Ant "collides" (detects) food if it is in its search 'cone' in direction its facing
    ant_pos = ant.position.copy()
    food_pos = food.position.copy()

    distance = ant_pos.distance_to(food_pos)

    if distance > ant.f_radius:
        return False

    dir_to = food_pos - ant_pos
    dir_to.normalize_ip()
    angle = dir_to.angle_to(ant.velocity)

    if angle < -180:
        angle = 360 + angle
    if angle > 180:
        angle = 360 - angle

    return -ant.viewAngle <= angle <= ant.viewAngle


def ant_detect_pheromone(ant, pheromone):
    # Food is a circle with position and radius
    # Ant "collides" (detects) food if it is in its search 'cone' in direction its facing
    ant_pos = ant.position.copy()
    p_pos = pheromone.position.copy()

    distance = ant_pos.distance_to(p_pos)

    if distance > ant.p_radius:
        return False

    dir_to = p_pos - ant_pos
    dir_to.normalize_ip()
    angle = dir_to.angle_to(ant.velocity)

    if angle < -180:
        angle = 360 + angle
    if angle > 180:
        angle = 360 - angle

    return -ant.viewAngle <= angle <= ant.viewAngle


class Environment:

    def __init__(self, position, num_ants):
        super().__init__()

        # Ant Hill features
        self.n = num_ants
        self.radius = 15
        self.ant_hill = AntHill(Vector2(position[0], position[1]))
        self.ant_hills = pygame.sprite.GroupSingle()
        self.ant_hill.add(self.ant_hills)

        # Sprite group of Ant objects
        self.sprites = pygame.sprite.Group()
        for i in range(self.n):
            new_ant = Ant(Vector2(position[0], position[1]))
            new_ant.add(self.sprites)

        # Sprite groups of Food and Pheromones
        self.food = pygame.sprite.Group()
        self.p_time = 10.0  # time in seconds that pheromones last on screen
        self.pheromones_home = pygame.sprite.Group()
        self.pheromones_food = pygame.sprite.Group()

    def place_pheromone(self, ant):
        if ant.time_to_place_pheromone():
            ant.t_last_p = pygame.time.get_ticks() / 1000.0

            if ant.holding_food:
                pheromone = Pheromone(ant.position, red, self.p_time)
                pheromone.add(self.pheromones_food)
            else:
                pheromone = Pheromone(ant.position, blue, self.p_time)
                pheromone.add(self.pheromones_home)

        else:
            pass

    def update(self):
        # Update driver for the simulation. Update all ants
        for ant in self.sprites:
            # Place pheromones
            self.place_pheromone(ant)

            # Update ant desired direction
            # If holding food, target blue pheromones, then home, then wander.
            if ant.holding_food:
                # Check if ant is inside ant hill
                intersect_hill = pygame.sprite.collide_circle(ant, self.ant_hill)
                if intersect_hill:
                    # Drop the food, and target centre of hill
                    ant.holding_food = False
                    ant.target = self.ant_hill.position.copy()

                else:
                    # Otherwise target next closest blue pheromone
                    pheromone = pygame.sprite.spritecollideany(ant, self.pheromones_home, collided=ant_detect_pheromone)
                    if pheromone is not None:
                        ant.target = pheromone.position.copy()

            else:
                # If not targetting food, and not holding food, try targetting food
                food = pygame.sprite.spritecollideany(ant, self.food, collided=ant_detect_food)
                if food is not None:
                    ant.target = food.position.copy()
                else:
                    ant.target = None

                if ant.target is None:
                    # Target next closest pheromone
                    pheromone = pygame.sprite.spritecollideany(ant, self.pheromones_food, collided=ant_detect_pheromone)
                    if pheromone is not None:
                        ant.target = pheromone.position.copy()
                    else:
                        ant.target = None

                food_collide = pygame.sprite.spritecollideany(ant, self.food)
                if food_collide is not None:
                    ant.holding_food = True
                    self.food.remove(food_collide)

            # Update ant position by following a target or wandering
            if ant.target is not None:
                ant.follow_target()
            else:
                ant.wander()

        # Update sprite images
        self.sprites.update()
        self.pheromones_food.update()
        self.pheromones_home.update()

    def show(self, screen):
        self.pheromones_food.draw(screen)
        self.pheromones_home.draw(screen)
        self.food.draw(screen)
        self.sprites.draw(screen)
        self.ant_hills.draw(screen)

