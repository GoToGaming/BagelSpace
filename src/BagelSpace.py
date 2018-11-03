import os
import sys

import numpy as np
import pygame


DESIRED_RESOLUTION = (1280, 720)
SPRITES = {}

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)


class Missile(pygame.sprite.Sprite):
    MISSILE_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'machine_gun_bullet1.png')

    def __init__(self, pos, velocity):
        super().__init__()
        self.position = np.array(pos)
        self.velocity = np.array(velocity)

    def tick(self):
        self.position += self.velocity

    def blit(self, screen):
        screen.blit(SPRITES[self.MISSILE_FILE_NAME], self.position)

    @property
    def rect(self):
        rect = SPRITES[self.MISSILE_FILE_NAME].get_rect()
        rect.x, rect.y = self.position
        return rect


class SpaceShip(pygame.sprite.Sprite):
    SPACE_SHIP_IS_LEFT = 1
    SPACE_SHIP_IS_RIGHT = 2
    SPRITE_LEFT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'red_ship_1.png')
    SPRITE_RIGHT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'blue_ship.png')
    DEFAULT_VELOCITY = 3
    MIDDLE_POS = DESIRED_RESOLUTION[0] / 2

    def __init__(self, position, space_ship_side, sprite):
        super().__init__()
        self.position = np.array(position)
        self.space_ship_side = space_ship_side
        self.health_percentage = 100
        self.ship_destroyed = False
        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            self.space_ship_bound = np.array([[0,0],
                                      np.array([DESIRED_RESOLUTION[0] / 2, DESIRED_RESOLUTION[1]]) - self.sprite.get_size()])
        else:
            self.space_ship_bound = np.array([[DESIRED_RESOLUTION[0] / 2,0],
                                       np.array(DESIRED_RESOLUTION) - self.sprite.get_size()])
        if any(self.space_ship_bound[0] > self.position) or any(self.position > self.space_ship_bound[1]):
            raise ValueError
        self.velocity = np.array([0, 0])
        self.firing = False
        self.missiles = []

    def damage_ship(self, health_percentage_div):
        self.health_percentage -= int(health_percentage_div)
        if self.health_percentage <= 0:
            self.health_percentage = 0
            self.ship_destroyed = True
        return self.ship_destroyed

    def increase_health_percentage(self, health_percentage_div):
        new_health_percentage = self.health_percentage + int(health_percentage_div)
        if new_health_percentage > 100:
            self.health_percentage = 100
        else:
            self.health_percentage = new_health_percentage

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
            self.position = np.clip(new_position, [0,0], np.array([self.MIDDLE_POS,DESIRED_RESOLUTION[1]])-self.sprite.get_size())
            missile_velocity = (3, 0)
        else:
            self.position = np.clip(new_position, [self.MIDDLE_POS,0], np.array(DESIRED_RESOLUTION)-self.sprite.get_size())
            missile_velocity = (-3, 0)
        if self.firing:
            self.missiles.append(Missile(self.position, missile_velocity))
        for missile in self.missiles.copy():
            missile.tick()
            if 0 > missile.position[0] or missile.position[0] > DESIRED_RESOLUTION[0]:
                self.missiles.remove(missile)

    def blit(self, screen):
        screen.blit(self.sprite, self.position)
        for missile in self.missiles:
            missile.blit(screen)

    @property
    def rect(self):
        rect = self.sprite.get_rect()
        rect.x, rect.y = self.position
        return rect

    def get_objects(self):
        return [self, *self.missiles]


class SpaceBagels:
    BACKGROUND_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'background.png')

    def __init__(self, screen):
        self._screen = screen
        self.player_left = SpaceShip((100, 360), SpaceShip.SPACE_SHIP_IS_LEFT, SPRITES[SpaceShip.SPRITE_LEFT_FILE_NAME])
        self.player_right = SpaceShip((1180, 360), SpaceShip.SPACE_SHIP_IS_RIGHT, SPRITES[SpaceShip.SPRITE_RIGHT_FILE_NAME])

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

    def _draw_text(self, string, size, x_middle, y_middle, color=yellow):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(string, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x_middle, y_middle)
        self._screen.blit(text_surface, text_rect)

    def _draw_text2(self, string, size, x, y, color=yellow):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(string, True, color)
        self._screen.blit(text_surface, (x, y))

    def blit(self):
        self._screen.blit(SPRITES[self.BACKGROUND_FILE_NAME], (0, 0))
        self.player_left.blit(self._screen)
        self.player_right.blit(self._screen)

    def detect_collisions(self):
        player_left_objects = self.player_left.get_objects()
        player_right_objects = self.player_right.get_objects()
        if pygame.sprite.spritecollideany(self.player_left, player_right_objects):
            print("Player Left hit")
            self.player_left.damage_ship(health_percentage_div=10)
        if pygame.sprite.spritecollideany(self.player_right, player_left_objects):
            print("Player Right hit")
            self.player_right.damage_ship(health_percentage_div=10)


class GameMenu:
    def __init__(self, screen):
        self._screen = screen
        self.game = SpaceBagels(self._screen)

    def process_input(self, event):
        if event.type in (pygame.JOYHATMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
            self.game.process_input(event)
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def tick(self, tick_count):
        self.game.tick(tick_count)

    def blit(self):
        self.game.blit()

    def select_input_method(self):
        pygame.joystick.init()
        if pygame.joystick.get_count() >= 2:
            print('Keyboard or joystick?')
        joysticks = [pygame.joystick.Joystick(idx) for idx in range(2)]
        for joystick in joysticks:
            joystick.init()


def main():
    pygame.init()

    target_fps = 60
    target_frametime_ms = 1000. / target_fps
    last_frametime = 0

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(DESIRED_RESOLUTION)
    pygame.display.set_caption('SpaceBagels')

    SPRITES[SpaceBagels.BACKGROUND_FILE_NAME] = pygame.image.load(SpaceBagels.BACKGROUND_FILE_NAME).convert()
    SPRITES[SpaceShip.SPRITE_LEFT_FILE_NAME] = pygame.image.load(SpaceShip.SPRITE_LEFT_FILE_NAME).convert_alpha()
    SPRITES[SpaceShip.SPRITE_RIGHT_FILE_NAME] = pygame.image.load(SpaceShip.SPRITE_RIGHT_FILE_NAME).convert_alpha()
    SPRITES[Missile.MISSILE_FILE_NAME] = pygame.image.load(Missile.MISSILE_FILE_NAME).convert_alpha()

    menu = GameMenu(screen)

    while True:
        for event in pygame.event.get():
            menu.process_input(event)

        last_frametime += clock.tick()
        tick_count = int(last_frametime // target_frametime_ms)
        last_frametime = last_frametime % target_frametime_ms

        menu.tick(tick_count)
        pygame.display.flip()


if __name__ == '__main__':
    main()
