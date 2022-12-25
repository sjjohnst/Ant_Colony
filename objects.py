'''
This file contains class definitions for multiple world objects:
1. Food items
2. Pheromones
'''
import pygame.sprite
import random
from parameters import bckgrnd


class Food(pygame.sprite.Sprite):
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


class Pheromone(pygame.sprite.Sprite):
    def __init__(self, position, color, decay_t):
        super().__init__()
        self.image = pygame.Surface([4, 4])
        self.image.fill(bckgrnd)
        self.image.set_colorkey(bckgrnd)
        self.rect = self.image.get_rect(center=position)
        self.radius = 2
        self.position = position

        self.decay_t = decay_t
        self.end_t = pygame.time.get_ticks() / 1000.0 + decay_t
        self.color = pygame.Color(color[0], color[1], color[2], 255)

        pygame.draw.circle(self.image, self.color, (2, 2), self.radius)

    def update(self):
        dist = self.end_t - pygame.time.get_ticks() / 1000.0
        if dist <= 0:
            self.kill()
        else:
            self.color.a = int(min((dist / self.decay_t)*255, 255))
            self.image.fill(bckgrnd)
            pygame.draw.circle(self.image, self.color, (2, 2), self.radius)
