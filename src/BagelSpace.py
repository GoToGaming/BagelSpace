import os
import sys

import pygame


DESIRED_RESOLUTION = (1280, 720)


class SpaceShip(pygame.sprite.Sprite):
    SPRITE_LEFT = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'data', 'ship.png'))
    SPRITE_RIGHT = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'data', 'ship.png'))
    DEFAULT_VELOCITY = 3

    def __init__(self, position):
        super().__init__()
        self.position = list(position)
        self.velocity = [0, 0]

    def process_input(self, event):
        if event.type == pygame.JOYHATMOTION:
            if event.dict['hat'] == 0:
                self.velocity[0] = self.DEFAULT_VELOCITY * event.dict['value'][0]
                self.velocity[1] = self.DEFAULT_VELOCITY * event.dict['value'][1]
        elif event.type == pygame.JOYBUTTONUP:
            pass
        elif event.type == pygame.JOYBUTTONDOWN:
            pass

    def tick(self, *args):
        pass

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

    def tick(self, *args):
        self.player_left.tick(args)
        self.player_right.tick(args)
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
            #else:
                #print('Unhandled event: {}'.format(event))

        last_frametime += clock.tick()
        tick_count = last_frametime // target_frametime_ms
        last_frametime = last_frametime % target_frametime_ms
        fps = clock.get_fps()

        game.tick(fps, tick_count)
        pygame.display.flip()


if __name__ == '__main__':
    main()