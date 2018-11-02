import os
import sys

import pygame


DESIRED_RESOLUTION = (1280, 720)


class SpaceBagels:
    BACKGROUND = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'data', 'background.jpg'))

    def __init__(self, *args):
        self._screen = pygame.display.set_mode(DESIRED_RESOLUTION)
        pygame.display.set_caption('SpaceBagels')

    def process_input(self, *args):
        pass

    def tick(self, *args):
        self.blit()

    def blit(self):
        self._screen.blit(self.BACKGROUND, (0, 0))


def main():
    pygame.init()

    target_fps = 60
    target_frametime_ms = 1000. / target_fps
    last_frametime = 0

    clock = pygame.time.Clock()

    game = SpaceBagels()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                game.process_input(event.key)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        last_frametime += clock.tick()
        tick_count = last_frametime // target_frametime_ms
        last_frametime = last_frametime % target_frametime_ms
        fps = clock.get_fps()

        game.tick(fps, tick_count)
        pygame.display.flip()


if __name__ == '__main__':
    main()