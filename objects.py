'''
This file contains class definitions for multiple world objects:
1. Food items
2. Pheromones
'''
import pygame
from parameters import *


class Food:

    def __init__(self, x, y, color=green):
        self.x = x
        self.y = y
        self.color = color

    def show(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 5)

