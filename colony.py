import pygame
from pygame import Vector2
from ant import Ant
from objects import Food, Pheromone
from parameters import *
from datastructs import Vector


def ant_detect_food(ant, food):
    # Food is a circle with position and radius
    # Ant "collides" (detects) food if it is in its search 'cone' in direction its facing
    ant_pos = ant.position.copy()
    food_pos = food.position.copy()

    distance = ant_pos.distance_to(food_pos)

    if distance > ant.radius:
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


class Colony:

    def __init__(self, position, num_ants):
        super().__init__()

        self.position = Vector(position[0], position[1])
        self.r = 15
        self.n = num_ants
        self.color = orange

        self.image = pygame.image.load("ant_hill_sprite.png")

        self.sprites = pygame.sprite.Group()
        for i in range(self.n):
            new_ant = Ant(Vector2(position[0], position[1]))
            new_ant.add(self.sprites)

        self.food = pygame.sprite.Group()
        self.pheromones_home = pygame.sprite.Group()
        self.pheromones_food = pygame.sprite.Group()

    def update(self):
        for ant in self.sprites:
            # Target pheromones if detecting any
            if ant.holding_food:
                if ant.time_to_place_pheromone():
                    ant.t_last_p = pygame.time.get_ticks() / 1000.0
                    pheromone = Pheromone(ant.position, red, 7.0)
                    pheromone.add(self.pheromones_food)

                # Target next closest pheromone
                pheromone_list = pygame.sprite.spritecollide(ant, self.pheromones_home, False, collided=ant_detect_pheromone)
                if len(pheromone_list) > 0:
                    ant.target = pheromone_list[0].position.copy()

            else:
                if ant.time_to_place_pheromone():
                    ant.t_last_p = pygame.time.get_ticks() / 1000.0
                    pheromone = Pheromone(ant.position, blue, 7.0)
                    pheromone.add(self.pheromones_home)

                # If not targetting food, and not holding food, try targetting food
                food_list = pygame.sprite.spritecollide(ant, self.food, False, collided=ant_detect_food)
                if len(food_list) > 0:
                    ant.target = food_list[0].position.copy()
                else:
                    ant.target = None

                if ant.target is None:
                    # Target next closest pheromone
                    pheromone_list = pygame.sprite.spritecollide(ant, self.pheromones_food, False, collided=ant_detect_pheromone)
                    if len(pheromone_list) > 0:
                        ant.target = pheromone_list[0].position.copy()

                    else:
                        ant.target = None

            if ant.target is not None:
                ant.follow_target()
                food_collide = pygame.sprite.spritecollide(ant, self.food, False)
                if len(food_collide) > 0:
                    ant.holding_food = True
                    self.food.remove(food_collide[0])
            else:
                ant.wander()

        self.sprites.update()
        self.pheromones_home.update()

    def show(self, screen):
        self.pheromones_food.draw(screen)
        self.pheromones_home.draw(screen)
        self.food.draw(screen)
        self.sprites.draw(screen)
        pygame.draw.circle(screen, self.color, self.position.get_coord(), self.r)
