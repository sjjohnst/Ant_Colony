import pygame
import random
import numpy as np
import math
from parameters import *

PI = math.pi


def to_polar(v):
    r = magnitude(v)
    theta = math.atan(v[1]/v[0])
    return [r, theta]


def to_cartesian(v):
    x = v[0] * math.cos(v[1])
    y = v[0] * math.sin(v[1])
    return [x, y]


def magnitude(v):
    return math.sqrt(v[0]**2 + v[1]**2)


def normalize(v):
    len = magnitude(v)
    if len == 0.0:
        return v
    inv_len = 1.0/len
    return list(np.multiply(v, inv_len))


def scale(v, s):
    return [v[0]*s, v[1]*s]


def clamp_vector(v, clip):
    current_speed = magnitude(v)
    v_new = v
    if current_speed > clip:
        theta = math.atan(v[1] / v[0])
        v_new[0] = clip * math.cos(theta)
        v_new[1] = clip * math.sin(theta)

    return v_new


def angle(v1, v2):
    inner = np.inner(v1, v2)
    norms = np.linalg.norm(v1) * np.linalg.norm(v2)

    cos = inner / norms
    rad = np.arccos(np.clip(cos, -1.0, 1.0))

    return rad


def slerp(start, end, t):
    start = normalize(start)
    end = normalize(end)

    theta = angle(start, end)
    sin_theta = math.sin(theta) + 1e-10

    a = math.sin((1 - t) * theta) / sin_theta
    b = math.sin(t * theta) / sin_theta

    return scale(start, a) + scale(end, b)


'''
Ant class
1. Implement Ant wandering aimlessly. Make it smooth
2. Add food items, have ants detect and steer towards food
3. Add in pheromones, have ants leave trails and follow trails
'''


class Ant:
    def __init__(self, position):

        # Constant attributes
        self.color = white
        self.max_speed = 1.0

        # Position, speed and direction
        self.position = position
        init_speed = np.random.random_sample() * self.max_speed
        init_direction = np.random.random_sample() * 2 * PI
        self.velocity = to_cartesian([init_speed, init_direction])

        # Wandering parameters
        init_speed = np.random.random_sample() * self.max_speed
        init_direction = np.random.random_sample() * 2 * PI
        self.desired_velocity = to_cartesian([init_speed, init_direction])
        self.wander_strength = 0.1
        self.steer_strength = 0.1

        print(self.velocity, self.desired_velocity)

    def update(self):

        # update position and velocity
        self.position = self.position + self.velocity
        self.velocity = slerp(self.velocity, self.desired_velocity, self.steer_strength)

        # update desired velocity
        desired_speed, desired_theta = to_polar(self.desired_velocity)
        update_theta = np.random.uniform(-self.wander_strength*2*PI, self.wander_strength*2*PI)
        update_speed = np.random.uniform(-self.wander_strength*self.max_speed, self.wander_strength*self.max_speed)

        self.desired_velocity = to_cartesian([desired_speed+update_speed, desired_theta+update_theta])

        # clamp vectors
        self.velocity = clamp_vector(self.velocity, self.max_speed)
        self.desired_velocity = clamp_vector(self.desired_velocity, self.max_speed)

    def show(self, screen):
        pygame.draw.circle(screen, self.color, (self.position[0], self.position[1]), 2)

