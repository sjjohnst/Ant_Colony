'''
This file contains class definitions for multiple world objects:
1. Food items
2. Pheromones
'''
import pygame
from parameters import *
from datastructs import *
from queue import PriorityQueue


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

    def delete(self, food):
        return self.food_tree.delete(food)

    def show_aux(self, screen, tree_node: QTree):
        for point in tree_node.points:
            pygame.draw.circle(screen, self.color, (point.x, point.y), 2)

        if tree_node.divided:
            self.show_aux(screen, tree_node.nw)
            self.show_aux(screen, tree_node.ne)
            self.show_aux(screen, tree_node.sw)
            self.show_aux(screen, tree_node.se)


class Pheromone_Layer:

    def __init__(self, color0=blue, color1=red):
        top_left = Vector(0, 0)
        bot_right = Vector(resolution[0], resolution[1])
        boundary = Box(top_left, bot_right)

        self.p0_tree = QTree(boundary)
        self.p1_tree = QTree(boundary)
        self.color0 = color0
        self.color1 = color1

        # Time each pheromone lasts on the screen, in seconds
        self.max_dt = 15

        # for storing pheromone and time placed
        # Allows deleting after specific time interval
        self.pq = PriorityQueue()

    def update(self):
        for time, item in sorted(self.pq.queue):
            dt = pygame.time.get_ticks() / 1000.0 - time
            if dt >= self.max_dt:
                self.pq.get()
                type = item.payload
                if type == 0:
                    self.p0_tree.delete(item)
                else:
                    self.p1_tree.delete(item)
            else:
                break

    def show(self, screen):
        for time, item in self.pq.queue:
            dt = pygame.time.get_ticks() / 1000.0 - time
            color_alpha = max(0.0, (self.max_dt - dt) / self.max_dt)

            pos = item.get_coord()
            if item.payload == 0:
                color = [int(color_alpha*c) for c in self.color0]
                pygame.draw.circle(screen, color, pos, 2)
            else:
                color = [int(color_alpha * c) for c in self.color1]
                pygame.draw.circle(screen, color, pos, 2)

    def insert(self, position, type):
        time = pygame.time.get_ticks() / 1000.0
        position.time = time
        position.payload = type
        self.pq.put((time, position))
        if type == 0:
            self.p0_tree.insert(position)
        if type == 1:
            self.p1_tree.insert(position)

    def query_radius(self, centre, radius, type):
        found_points = []
        if type == 0:
            self.p0_tree.query_radius(centre, radius, found_points)
        else:
            self.p1_tree.query_radius(centre, radius, found_points)
        found_points_times = [point.time for point in found_points]
        return sum(found_points_times)
