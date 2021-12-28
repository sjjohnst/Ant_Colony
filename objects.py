'''
This file contains class definitions for multiple world objects:
1. Food items
2. Pheromones
'''
from parameters import *


class Food:

    def __init__(self, x, y, color=green):
        self.x = x
        self.y = y
        self.color = color

    def show(self, ax):
        ax.scatter(self.x, self.y, color=self.color, s=10)

