# Dennis Tye
# CPSC 386-01
# 11/26/2021
# dennis.tye@csu.fullerton.edu
#
# Snake Game
#
# This my Game File

import sys
import pygame
from scene import TitleScene
def run_game():

    width = 800
    height = 800
    fps = 60

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    current_scene = TitleScene()
    while current_scene is not None:
        pressed_keys = pygame.key.get_pressed()

        filtered_events = []
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_scene.end_scene()
                sys.exit()
            elif event.type == pygame.QUIT:
                current_scene.end_scene()
                sys.exit()
            else:
                filtered_events.append(event)

        current_scene.handle_input(filtered_events)
        current_scene.update()
        current_scene.draw(screen)

        current_scene = current_scene.next

        pygame.display.flip() 
        clock.tick(fps)