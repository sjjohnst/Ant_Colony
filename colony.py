import random
import pygame
from pygame import Vector2
from ant import Ant
from parameters import *
from datastructs import Vector

'''
Colony class
1. Init with a number of ants, spawn all on same spot and let wander.
'''


class Colony:

    def __init__(self, position, num_ants):

        self.position = Vector(position[0], position[1])
        self.r = 15
        self.n = num_ants
        self.color = orange

        self.ant_sprites = pygame.sprite.Group()
        self.ant_dict = {}
        for i in range(self.n):
            new_ant = Ant(Vector2(position[0], position[1]), self)
            self.ant_dict[str(i)] = new_ant
            self.ant_sprites.add(new_ant)

    def update(self, food_tree, p_tree):
        # Update every ant, using food and pheromones
        for a in self.ant_dict.values():
            a.update()
            # a.detect_wall()
            # a.update_dir(food_tree, p_tree)
            # a.place_pheromones(p_tree)

    def show(self, screen):
        self.ant_sprites.draw(screen)
        pygame.draw.circle(screen, self.color, self.position.get_coord(), self.r)
