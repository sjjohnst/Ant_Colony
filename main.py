import pygame
from parameters import *
from ant import Ant

'''
Sam Johnston
December 2021
'''

# Parameters
resolution = (400, 400)
black = (0, 0, 0)

# Initialize pygame
pygame.display.init()
screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()
fps = 30

pause = False

a = Ant((resolution[0]/2, resolution[1]/2))
print(a.position)

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

    if not pause:
        # pygame.draw.circle(screen, orange, (100, 10), 2)
        a.show(screen)
        a.update()

    pygame.display.flip()

pygame.quit()