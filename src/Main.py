import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pygame

from src.Constants import DESIRED_RESOLUTION
from src.GameMenu import GameMenu


def main():
    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(DESIRED_RESOLUTION)
    pygame.display.set_caption('SpaceBagels')

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(idx) for idx in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()
    menu = GameMenu(screen, clock)

    while True:
        menu.process_inputs(pygame.event.get())

        pygame.display.flip()


if __name__ == '__main__':
    main()
