import pygame
from pygame.math import Vector2
from parameters import *
from objects import Food
from ant import Ant
from colony import Colony

'''
Sam Johnston
December 2021
'''

# Initialize pygame
pygame.display.init()
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

pause = False

# Sprite Groups
n = 100
colony_x, colony_y = 250, 250
colony = Colony((colony_x, colony_y), n)
# for i in range(n):
#     ant = Ant(Vector2(colony_x, colony_y))
#     ant.add(colony)

food_group = pygame.sprite.Group()
food_point = Vector2(-1, -1)

pheromone_group_0 = pygame.sprite.Group()
pheromone_group_1 = pygame.sprite.Group()

draw = False
draw_food_mode = True

run = True
while run:
    if not pause:
        screen.fill(bckgrnd)
        delta_time = clock.tick(fps)

        frame_rate = int(clock.get_fps())
        pygame.display.set_caption("Ant Colony Simulation - FPS : ( {} )".format(frame_rate))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    draw_food_mode = not draw_food_mode

            if event.type == pygame.MOUSEBUTTONDOWN:
                draw = True

            if event.type == pygame.MOUSEBUTTONUP:
                draw = False

        if draw and draw_food_mode:
            x, y = pygame.mouse.get_pos()
            if x != food_point.x or y != food_point.y:
                new_food = Food(Vector2(x, y), green)
                new_food.add(colony.food)
                food_point.x = x
                food_point.y = y

        colony.update()
        food_group.draw(screen)
        colony.show(screen)

        pygame.display.flip()

pygame.quit()