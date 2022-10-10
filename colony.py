import random
import pygame
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

        self.ant_dict = {}
        for i in range(self.n):
            self.ant_dict[str(i)] = Ant(Vector(position[0], position[1]), self)

    def update(self, food_tree, p_tree):
        # Update every ant, using food and pheromones
        for a in self.ant_dict.values():
            a.update()
            a.update_dir(food_tree, p_tree)
            a.place_pheromones(p_tree)

    def show(self, screen):
        # display all ants
        for a in self.ant_dict.values():
            a.show(screen)

        # display ant hill
        pygame.draw.circle(screen, self.color, self.position.get_coord(), self.r)
