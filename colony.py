import pygame
from pygame import Vector2
from ant import Ant
from objects import Particle
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

    def update(self, food):
        for ant in self.sprites:
            # If not targetting food, and not holding food, try targetting food
            if ant.target is None and not ant.holding_food:
                food_list = pygame.sprite.spritecollide(ant, food, False, collided=ant_detect_food)
                if len(food_list) > 0:
                    ant.target = food_list[0].position.copy()

            if ant.target is not None and not ant.holding_food:
                ant.follow_target()
                food_collide = pygame.sprite.spritecollide(ant, food, False)
                if len(food_collide) > 0:
                    ant.holding_food = True
                    food.remove(food_collide[0])

            else:
                ant.wander()

        self.sprites.update()

    def show(self, screen):
        self.sprites.draw(screen)
        pygame.draw.circle(screen, self.color, self.position.get_coord(), self.r)
