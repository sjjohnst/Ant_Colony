import pygame
from parameters import *
from objects import Food
from qtree import *
from colony import Colony
from ant import Ant
from vector import *

'''
Sam Johnston
December 2021
'''

# Initialize pygame
pygame.display.init()
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

pause = False

# a = Ant(Vector(resolution[0]/2, resolution[1]/2))
# print(a.position)

colony = Colony([resolution[0]/2, resolution[1]/2], 100)

# Instantiate a quad tree
top_left = Point(0, 0)
bot_right = Point(resolution[0], resolution[1])
box = Box(top_left, bot_right)
tree = QTree(box)

draw_food = False

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
            if event.key == pygame.K_SPACE:
                pause = not pause

        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_food = True

        if event.type == pygame.MOUSEBUTTONUP:
            draw_food = False

    if draw_food:
        x, y = pygame.mouse.get_pos()
        food = Food(x, y)
        tree.insert(food)

    if not pause:
        # pygame.draw.circle(screen, orange, (100, 10), 2)
        colony.update(delta_time)
        colony.show(screen)
        # a.update(delta_time)
        # a.show(screen)
        tree.show(screen)

    pygame.display.flip()

print(delta_time)
pygame.quit()