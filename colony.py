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

        self.position = position
        self.n = num_ants
        self.color = orange

        self.ant_dict = {}
        for i in range(self.n):
            self.ant_dict[str(i)] = Ant(Vector(self.position[0], self.position[1]))

    def update(self):
        for a in self.ant_dict.values():
            a.update()

    def show(self, screen):
        # display all ants
        for a in self.ant_dict.values():
            a.show(screen)

        # display ant hill
        pygame.draw.circle(screen, self.color, self.position, 15)
