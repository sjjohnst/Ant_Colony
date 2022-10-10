import pygame
from parameters import *
from objects import Food_Layer, Pheromone_Layer
from colony import Colony
from datastructs import *

'''
Sam Johnston
December 2021
'''

# Initialize pygame
pygame.display.init()
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

pause = False

# Instantiate the colony
n = 10
colony = Colony([250, 250], n)

# Instantiate a quad tree to store food
food_tree = Food_Layer()
food_point = Vector(-1, -1)

pheromone_layer = Pheromone_Layer()

draw = False
draw_food_mode = True

run = True
while run:
    if not pause:
        screen.fill(black)
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
            food_point = Vector(x, y)
            food_tree.insert(food_point)

    colony.update(food_tree, pheromone_layer)

    pheromone_layer.show(screen)
    pheromone_layer.update()
    food_tree.show(screen)
    colony.show(screen)

    pygame.display.flip()

pygame.quit()