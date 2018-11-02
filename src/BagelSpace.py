import os
import sys

import numpy as np
import pygame


DESIRED_RESOLUTION = (1280, 720)


class SpaceShip(pygame.sprite.Sprite):
    SPACE_SHIP_IS_LEFT = 1
    SPACE_SHIP_IS_RIGHT = 2
    SPRITE_LEFT = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'data', 'ship.png'))
    SPRITE_RIGHT = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'data', 'ship.png'))
    SPACE_SHIP_LEFT_BOUND = np.array([[0,0],[DESIRED_RESOLUTION[0] / 2, DESIRED_RESOLUTION[1]]])
    DEFAULT_VELOCITY = 3
    MIDDLE_POS = DESIRED_RESOLUTION[0] / 2

    def __init__(self, position, space_ship_side):
        super().__init__()
        self.position = np.array(position)
        self.space_ship_side = space_ship_side
        if not any(self.SPACE_SHIP_LEFT_BOUND[0] <= self.position) or not any(self.position < self.SPACE_SHIP_LEFT_BOUND[1]):
            raise ValueError
        self.velocity = np.array([0, 0])

    def process_input(self, event):
        if event.type == pygame.JOYHATMOTION:
            if event.dict['hat'] == 0:
                self.velocity = self.DEFAULT_VELOCITY * np.array(event.dict['value'])
        elif event.type == pygame.JOYBUTTONUP:
            pass
        elif event.type == pygame.JOYBUTTONDOWN:
            pass

    def tick(self, tick_count):
        new_position = self.position + self.velocity
        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            self.position = np.clip(new_position, [0,0], [self.MIDDLE_POS,DESIRED_RESOLUTION[1]])
        else:
            self.position = np.clip(new_position, [self.MIDDLE_POS,0], DESIRED_RESOLUTION)

    def blit(self, screen):
        screen.blit(self.SPRITE_LEFT, self.position)


class SpaceBagels:
    BACKGROUND = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'data', 'background.jpg'))

    def __init__(self, *args):
        self._screen = pygame.display.set_mode(DESIRED_RESOLUTION)
        pygame.display.set_caption('SpaceBagels')
        self.player_left = SpaceShip((100, 360))
        self.player_right = SpaceShip((1180, 360))

    def process_input(self, event):
        if event.dict['joy'] == 0:
            self.player_left.process_input(event)
        elif event.dict['joy'] == 1:
            self.player_right.process_input(event)

    def tick(self, tick_count):
        self.player_left.tick(tick_count)
        self.player_right.tick(tick_count)
        self.blit()

    def blit(self):
        self._screen.blit(self.BACKGROUND, (0, 0))
        self.player_left.blit(self._screen)
        self.player_right.blit(self._screen)


def main():
    pygame.init()

    target_fps = 60
    target_frametime_ms = 1000. / target_fps
    last_frametime = 0

    clock = pygame.time.Clock()

    pygame.joystick.init()
    if pygame.joystick.get_count() < 2:
        print('Need at least two controllers to play.')
        pygame.quit()
        sys.exit()
    joysticks = [pygame.joystick.Joystick(idx) for idx in range(2)]
    for joystick in joysticks:
        joystick.init()

    game = SpaceBagels()

    while True:
        for event in pygame.event.get():
            if event.type in (pygame.JOYHATMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
                print(event)
                game.process_input(event)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        last_frametime += clock.tick()
        tick_count = last_frametime // target_frametime_ms
        last_frametime = last_frametime % target_frametime_ms

        game.tick(tick_count)
        pygame.display.flip()


if __name__ == '__main__':
    main()
