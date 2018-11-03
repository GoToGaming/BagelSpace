import datetime
import os
import sys

import numpy as np
import pygame
import pygameMenu
from pygameMenu.locals import *


DESIRED_RESOLUTION = (1280, 720)
GAME_SCALE = 2
TARGET_FPS = 60
TARGET_FRAMETIME_MS = 1000. / TARGET_FPS
SPRITES = {}

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)


def load_image(path, scale=1, animation=False, flip_x=False, flip_y=False, alpha=True):
    if not animation:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, [x * scale for x in image.get_size()])
        image = pygame.transform.flip(image, flip_x, flip_y)
        if alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
        return image
    else:
        animation_array = []
        counter = 1
        while animation:
            try:
                image = pygame.image.load(path + str(counter) + ".png")
                image = pygame.transform.scale(image, [x * scale for x in image.get_size()])
                image = pygame.transform.flip(image, flip_x, flip_y)
                if alpha:
                    image = image.convert_alpha()
                else:
                    image = image.convert()
                animation_array.append(image)
                counter += 1
            except pygame.error:
                if len(animation_array) > 0:
                    return animation_array
                else:
                    raise FileNotFoundError


class Animation:

    def __init__(self, path, speed, scale=1, flip_x=False, flip_y=False, alpha = True):
        self.speed = speed
        self.counter = 0
        self.current_image = 0
        self.animation = load_image(path, scale=scale, animation=True, flip_x=flip_x, flip_y=flip_y, alpha=alpha)

    def update(self):
        self.counter += 1
        if self.counter >= self.speed:
            self.current_image += 1
            self.counter = 0
            self.current_image = self.current_image % len(self.animation)

    def get_current_image(self):
        return self.animation[self.current_image]


class Missile(pygame.sprite.Sprite):
    MISSILE_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'rocket')

    def __init__(self, pos, velocity):
        super().__init__()
        self.position = np.array(pos)
        self.velocity = np.array(velocity)

        self.animation = Animation(self.MISSILE_FILE_NAME, 4, GAME_SCALE)

    def tick(self):
        self.position += self.velocity
        self.animation.update()

    def blit(self, screen):
        screen.blit(self.animation.get_current_image(), self.position)

    @property
    def rect(self):
        rect = self.animation.get_current_image().get_rect()
        rect.x, rect.y = self.position
        return rect


class SpaceShip(pygame.sprite.Sprite):
    SPACE_SHIP_IS_LEFT = 1
    SPACE_SHIP_IS_RIGHT = 2
    SPRITE_LEFT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'red_ship_1.png')
    SPRITE_RIGHT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'blue_ship.png')
    DEFAULT_VELOCITY = 3
    MIDDLE_POS = DESIRED_RESOLUTION[0] / 2

    def __init__(self, position, space_ship_side, sprite_path):
        super().__init__()
        self.position = np.array(position)
        self.space_ship_side = space_ship_side
        self.sprite = load_image(sprite_path, GAME_SCALE)
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

    def missile_has_collided(self, missile):
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

    def __init__(self, screen, clock):
        self._screen = screen
        self._clock = clock
        self.player_left = SpaceShip((200, 360), SpaceShip.SPACE_SHIP_IS_LEFT, SpaceShip.SPRITE_LEFT_FILE_NAME)
        self.player_right = SpaceShip((1000, 360), SpaceShip.SPACE_SHIP_IS_RIGHT, SpaceShip.SPRITE_RIGHT_FILE_NAME)
        self.running = True
        self.last_frametime = 0

    def main(self):
        self.running = True
        self._clock.tick()

        while True:
            playevents = pygame.event.get()
            for e in playevents:
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.running = False
                    return
                else:
                    self.process_input(e)

            self.last_frametime += self._clock.tick()
            tick_count = int(self.last_frametime // TARGET_FRAMETIME_MS)
            self.last_frametime = self.last_frametime % TARGET_FRAMETIME_MS

            self.tick(tick_count)
            pygame.display.flip()

    def process_input(self, event):
        if not self.running:
            return

        if event.type in (pygame.KEYUP, pygame.KEYDOWN):
            print('key input not implemented')
        elif event.type in (pygame.JOYHATMOTION, pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN):
            if event.dict['joy'] == 0:
                self.player_left.process_input(event)
            elif event.dict['joy'] == 1:
                self.player_right.process_input(event)

    def tick(self, tick_count):
        if not self.running:
            return

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

        hit_left_player = pygame.sprite.spritecollideany(self.player_left, player_right_objects)
        if hit_left_player:
            print("Player Left hit")
            self.player_right.missile_has_collided(hit_left_player)
            self.player_left.damage_ship(health_percentage_div=10)

        hit_right_player = pygame.sprite.spritecollideany(self.player_right, player_left_objects)
        if pygame.sprite.spritecollideany(self.player_right, player_left_objects):
            print("Player Right hit")
            self.player_left.missile_has_collided(hit_right_player)
            self.player_right.damage_ship(health_percentage_div=10)


class GameMenu:
    def __init__(self, screen, clock):
        self._screen = screen
        self.game = SpaceBagels(self._screen, clock)

        def _main_menu_callback():
            self._screen.fill((40, 0, 40))

        def _resume_callback():
            self.menu.disable()
            self.game.main()

        def _new_game_callback():
            self.menu.disable()
            self.game = SpaceBagels(self._screen, clock)
            self.game.main()

        self.menu = pygameMenu.Menu(self._screen,
                                    bgfun=_main_menu_callback,
                                    enabled=True,
                                    font=pygameMenu.fonts.FONT_8BIT,
                                    menu_alpha=90,
                                    onclose=_resume_callback,
                                    title='BagelSpace',
                                    window_width=DESIRED_RESOLUTION[0],
                                    window_height=DESIRED_RESOLUTION[1])

        self.menu.add_option('New Game', _new_game_callback)
        self.menu.add_option('Exit', PYGAME_MENU_EXIT)

    def process_inputs(self, events):
        self.menu.enable()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.menu.mainloop(events)

    def select_input_method(self):
        pass


def main():
    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(DESIRED_RESOLUTION)
    pygame.display.set_caption('SpaceBagels')

    SPRITES[SpaceBagels.BACKGROUND_FILE_NAME] = load_image(SpaceBagels.BACKGROUND_FILE_NAME, GAME_SCALE)

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
