import pygame

from photobooth import Actions


class Keyboard:

    def next_action(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return Actions.QUIT
                if event.key == pygame.K_DOWN:
                    return Actions.TAKE_PICTURES
        return None
