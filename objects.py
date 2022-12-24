'''
This file contains class definitions for multiple world objects:
1. Food items
2. Pheromones
'''
import pygame.sprite
import random
from parameters import bckgrnd


class Particle(pygame.sprite.Sprite):
    def __init__(self, position, color):
        super().__init__()
        self.image = pygame.Surface([4, 4])
        self.image.fill(bckgrnd)
        self.image.set_colorkey(bckgrnd)
        self.rect = self.image.get_rect(center=position)
        self.radius = 2
        self.position = position

        s = 50
        r_shift = random.uniform(-s, s)
        g_shift = random.uniform(-s, s)
        b_shift = random.uniform(-s, s)

        new_r = min(max(color[0]+r_shift, 0), 255)
        new_g = min(max(color[1]+g_shift, 0), 255)
        new_b = min(max(color[2]+b_shift, 0), 255)
        color_shift = (new_r, new_g, new_b)

        pygame.draw.circle(self.image, color_shift, (2, 2), self.radius)

