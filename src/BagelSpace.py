import os
import sys

import numpy as np
import pygame


DESIRED_RESOLUTION = (1280, 720)


class Missile(pygame.sprite.Sprite):
    SPRITE = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'img', 'machine_gun_bullet1.png'))

    def __init__(self, pos, vel):
        super().__init__()
        self.position = np.array(pos)
        self.velocity = np.array(vel)

    def tick(self):
        self.position += self.velocity

    def blit(self, screen):
        screen.blit(self.SPRITE, self.position)

    @property
    def rect(self):
        rect = self.SPRITE.get_rect()
        rect.x, rect.y = self.position
        return rect


class SpaceShip(pygame.sprite.Sprite):
    SPACE_SHIP_IS_LEFT = 1
    SPACE_SHIP_IS_RIGHT = 2
    SPRITE_LEFT = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'img', 'red_ship_1.png'))
    SPRITE_RIGHT = pygame.image.load(os.path.join(os.path.dirname(__file__), '..', 'img', 'blue_ship.png'))
    SPACE_SHIP_LEFT_BOUND = np.array([[0,0],
                                      np.array([DESIRED_RESOLUTION[0] / 2, DESIRED_RESOLUTION[1]]) - SPRITE_LEFT.get_size()])
    SPACE_SHIP_RIGHT_BOUND = np.array([[DESIRED_RESOLUTION[0] / 2,0],
                                      np.array(DESIRED_RESOLUTION) - SPRITE_LEFT.get_size()])
    DEFAULT_VELOCITY = 3
    MIDDLE_POS = DESIRED_RESOLUTION[0] / 2

    def __init__(self, position, space_ship_side):
        super().__init__()
        self.position = np.array(position)
        self.space_ship_side = space_ship_side
        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            if any(self.SPACE_SHIP_LEFT_BOUND[0] > self.position) or any(self.position > self.SPACE_SHIP_LEFT_BOUND[1]):
                raise ValueError
        else:
            if any(self.SPACE_SHIP_RIGHT_BOUND[0] > self.position) or any(self.position > self.SPACE_SHIP_RIGHT_BOUND[1]):
                raise ValueError
        self.velocity = np.array([0, 0])
        self.firing = False
        self.missiles = []

    def process_input(self, event):
        if event.type == pygame.JOYHATMOTION:
            if event.dict['hat'] == 0:
                self.velocity = self.DEFAULT_VELOCITY * np.array(event.dict['value'])
                self.velocity[1] *= -1
        elif event.type == pygame.JOYBUTTONUP:
            self.firing = False
        elif event.type == pygame.JOYBUTTONDOWN:
            self.firing = True

    def tick(self):
        new_position = self.position + self.velocity
        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            self.position = np.clip(new_position, [0,0], np.array([self.MIDDLE_POS,DESIRED_RESOLUTION[1]])-self.SPRITE_LEFT.get_size())
            missile_velocity = (3, 0)
        else:
            self.position = np.clip(new_position, [self.MIDDLE_POS,0], np.array(DESIRED_RESOLUTION)-self.SPRITE_RIGHT.get_size())
            missile_velocity = (-3, 0)
        if self.firing:
            self.missiles.append(Missile(self.position, missile_velocity))
        for missile in self.missiles.copy():
            missile.tick()
            if 0 > missile.position[0] or missile.position[0] > DESIRED_RESOLUTION[0]:
                self.missiles.remove(missile)

    def blit(self, screen):
        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            screen.blit(self.SPRITE_LEFT, self.position)
        else:
            screen.blit(self.SPRITE_RIGHT, self.position)
        for missile in self.missiles:
            missile.blit(screen)

    @property
    def rect(self):
        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            rect = self.SPRITE_LEFT.get_rect()
        else:
            rect = self.SPRITE_RIGHT.get_rect()
        rect.x, rect.y = self.position
        return rect

    def get_objects(self):
        return [self, *self.missiles]


class SpaceBagels:
    def __init__(self):
        self._screen = pygame.display.set_mode(DESIRED_RESOLUTION)
        pygame.display.set_caption('SpaceBagels')
        self.player_left = SpaceShip((100, 360), SpaceShip.SPACE_SHIP_IS_LEFT)
        self.player_right = SpaceShip((1180, 360), SpaceShip.SPACE_SHIP_IS_RIGHT)

    def process_input(self, event):
        if event.dict['joy'] == 0:
            self.player_left.process_input(event)
        elif event.dict['joy'] == 1:
            self.player_right.process_input(event)

    def tick(self, tick_count):
        for tick in range(tick_count):
            self.player_left.tick()
            self.player_right.tick()
            self.detect_collisions()
        self.blit()

    def blit(self):
        self.player_left.blit(self._screen)
        self.player_right.blit(self._screen)

    def detect_collisions(self):
        player_left_objects = self.player_left.get_objects()
        player_right_objects = self.player_right.get_objects()
        if pygame.sprite.spritecollideany(self.player_left, player_right_objects):
            print("Player Left hit")
        if pygame.sprite.spritecollideany(self.player_right, player_left_objects):
            print("Player Right hit")


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
        tick_count = int(last_frametime // target_frametime_ms)
        last_frametime = last_frametime % target_frametime_ms

        game.tick(tick_count)
        pygame.display.flip()


if __name__ == '__main__':
    main()
