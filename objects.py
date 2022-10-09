'''
This file contains class definitions for multiple world objects:
1. Food items
2. Pheromones
'''
import pygame
from parameters import *
from datastructs import *


class Food_Layer:

    def __init__(self, color=green):
        top_left = Vector(0, 0)
        bot_right = Vector(resolution[0], resolution[1])
        boundary = Box(top_left, bot_right)

        self.food_tree = QTree(boundary)
        self.color = color

    def show(self, screen):
        # Traverse down the QTree and display every point encountered
        self.show_aux(screen, self.food_tree)

    def query_radius(self, center, radius):
        found_points = []
        self.food_tree.query_radius(center, radius, found_points)
        return found_points

    def search(self, point):
        return self.food_tree.search(point)

    def insert(self, food):
        self.food_tree.insert(food)

    def show_aux(self, screen, tree_node: QTree):
        for point in tree_node.points:
            pygame.draw.circle(screen, self.color, (point.x, point.y), 2)

        if tree_node.divided:
            self.show_aux(screen, tree_node.nw)
            self.show_aux(screen, tree_node.ne)
            self.show_aux(screen, tree_node.sw)
            self.show_aux(screen, tree_node.se)
