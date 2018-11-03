import os
import sys
from enum import Enum

import numpy as np
import random as rand
import pygame
import pygameMenu
from pygameMenu.locals import *

DESIRED_RESOLUTION = (1280, 720)
GAME_SCALE = 2
TARGET_FPS = 60
TARGET_FRAMETIME_MS = 1000. / TARGET_FPS
SPRITES = {}


class Button(Enum):
    UP = 0,
    DOWN = 1,
    LEFT = 2,
    RIGHT = 3,
    FIRE = 4


KEYBOARD_MAPPING = {pygame.K_UP: Button.UP,
                    pygame.K_w: Button.UP,
                    pygame.K_DOWN: Button.DOWN,
                    pygame.K_s: Button.DOWN,
                    pygame.K_LEFT: Button.LEFT,
                    pygame.K_a: Button.LEFT,
                    pygame.K_RIGHT: Button.RIGHT,
                    pygame.K_d: Button.RIGHT,
                    pygame.K_SPACE: Button.FIRE,
                    pygame.K_RETURN: Button.FIRE}

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

    def __init__(self, path, speed, scale=1, flip_x=False, flip_y=False, alpha=True):
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
    reload_time_sec = 0.5

    def __init__(self, pos, velocity, is_right_player):
        super().__init__()
        self.position = np.array(pos)
        self.velocity = np.array(velocity)

        self.animation = Animation(self.MISSILE_FILE_NAME, 4, GAME_SCALE, flip_x=is_right_player)

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


class MeteoriteController:
    METEORITE_TARGET_COUNT = 15
    meteorites = []

    def tick(self):
        if len(self.meteorites) < self.METEORITE_TARGET_COUNT:
            self.spawn_meteorite()

        for meteorite in self.meteorites:
            meteorite.tick()
            if 0 > meteorite.position[0] or meteorite.position[0] > DESIRED_RESOLUTION[0]:
                self.meteorites.remove(meteorite)

    def spawn_meteorite(self):
        x = DESIRED_RESOLUTION[0] / 2
        y = rand.randint(0, DESIRED_RESOLUTION[1])
        direction = rand.choice([-1,1])
        speed = (rand.random()*2)+1
        meteorite = Meteorite((x, y), (speed*direction, 0));
        self.meteorites.append(meteorite)

    def blit(self, screen):
        for meteorite in self.meteorites:
            meteorite.blit(screen)


class Meteorite(pygame.sprite.Sprite):
    METEORITE_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'meteorite.png')

    def __init__(self, pos, velocity):
        super().__init__()
        self.position = np.array(pos)
        self.velocity = np.array(velocity)

        self.sprite = load_image(self.METEORITE_FILE_NAME)

    def tick(self):
        self.position += self.velocity

    def blit(self, screen):
        screen.blit(self.sprite, self.position)

    @property
    def rect(self):
        rect = self.sprite.get_rect()
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
        self.sprite = sprite
        self.health_percentage = 100
        self.ship_destroyed = False
        self.reaming_reload_ticks = 0
        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            self.space_ship_bound = np.array([[0, 0],
                                              np.array([DESIRED_RESOLUTION[0] / 2,
                                                        DESIRED_RESOLUTION[1]]) - self.sprite.get_size()])
        else:
            self.space_ship_bound = np.array([[DESIRED_RESOLUTION[0] / 2, 0],
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

    def process_input(self, event, button):
        if event.type == pygame.JOYHATMOTION:
            if event.dict['hat'] == 0:
                self.velocity = self.DEFAULT_VELOCITY * np.array(event.dict['value'])
                self.velocity[1] *= -1
        elif event.type == pygame.JOYBUTTONUP:
            self.firing = False
        elif event.type == pygame.JOYBUTTONDOWN:
            self.firing = True
        elif event.type == pygame.KEYDOWN:
            if button == button.UP:
                self.velocity[1] = -self.DEFAULT_VELOCITY
            elif button == Button.DOWN:
                self.velocity[1] = self.DEFAULT_VELOCITY
            if button == Button.LEFT:
                self.velocity[0] = -self.DEFAULT_VELOCITY
            elif button == Button.RIGHT:
                self.velocity[0] = self.DEFAULT_VELOCITY
            if button == Button.FIRE:
                self.firing = True
        elif event.type == pygame.KEYUP:
            if button in (Button.UP, Button.DOWN):
                self.velocity[1] = 0
            if button in (Button.LEFT, Button.RIGHT):
                self.velocity[0] = 0
            if button == Button.FIRE:
                self.firing = False

    def calculate_missile_start_pos(self):
        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            return self.position + np.array([self.sprite.get_size()[0], int(self.sprite.get_size()[1] / 2)])
        else:
            return self.position + np.array([0, int(self.sprite.get_size()[1] / 2)])

    def tick(self):
        new_position = self.position + self.velocity
        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            self.position = np.clip(new_position, [0, 0],
                                    np.array([self.MIDDLE_POS, DESIRED_RESOLUTION[1]]) - self.sprite.get_size())
            missile_velocity = (3, 0)
        else:
            self.position = np.clip(new_position, [self.MIDDLE_POS, 0],
                                    np.array(DESIRED_RESOLUTION) - self.sprite.get_size())
            missile_velocity = (-3, 0)

        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            is_right_player = False
        else:
            is_right_player = True

        if self.reaming_reload_ticks > 0:
            self.reaming_reload_ticks -= 1
        if self.firing and self.reaming_reload_ticks <= 0:
            self.missiles.append(Missile(self.calculate_missile_start_pos(), missile_velocity, is_right_player))
            self.reaming_reload_ticks = int(Missile.reload_time_sec * 60)
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
        player_left_sprite = load_image(SpaceShip.SPRITE_LEFT_FILE_NAME, GAME_SCALE)
        self.player_left = SpaceShip((200, 360), SpaceShip.SPACE_SHIP_IS_LEFT, player_left_sprite)
        player_right_sprite = load_image(SpaceShip.SPRITE_RIGHT_FILE_NAME, GAME_SCALE)
        self.player_right = SpaceShip((1000, 360), SpaceShip.SPACE_SHIP_IS_RIGHT, player_right_sprite)
        self.meteorite_controller = MeteoriteController()
        self.running = True
        self.last_frametime = 0
        self.use_joystick = False

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

        if self.use_joystick:
            if event.type in (pygame.JOYHATMOTION, pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN):
                if event.dict['joy'] == 0:
                    self.player_left.process_input(event, None)
                elif event.dict['joy'] == 1:
                    self.player_right.process_input(event, None)
        else:
            if event.type in (pygame.KEYUP, pygame.KEYDOWN):
                if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE):
                    self.player_left.process_input(event, KEYBOARD_MAPPING[event.key])
                elif event.key in (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_RETURN):
                    self.player_right.process_input(event, KEYBOARD_MAPPING[event.key])

    def tick(self, tick_count):
        if not self.running:
            return

        for tick in range(tick_count):
            self.player_left.tick()
            self.player_right.tick()
            self.meteorite_controller.tick()
            self.detect_collisions()
        self.blit()

    def draw_text(self, string, size, x_middle, y_middle, color=yellow):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(string, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x_middle, y_middle)
        self._screen.blit(text_surface, text_rect)

    def draw_text2(self, string, size, x, y, color=yellow):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(string, True, color)
        self._screen.blit(text_surface, (x, y))

    def blit_status_bar(self):
        self.draw_text2(f'{self.player_left.health_percentage}%', size=30, x=0, y=0, color=red)

        self.draw_text2(f'{self.player_right.health_percentage}%', size=30, x=1000, y=0, color=blue)

    def blit(self):
        self._screen.blit(SPRITES[self.BACKGROUND_FILE_NAME], (0, 0))
        self.player_left.blit(self._screen)
        self.player_right.blit(self._screen)
        self.blit_status_bar()
        self.meteorite_controller.blit(self._screen)

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

    def _set_input_method(self, use_joystick):
        self.use_joystick = use_joystick


class GameMenu:
    def __init__(self, screen, clock):
        self._screen = screen
        if pygame.joystick.get_count() < 2:
            self.use_joystick = False
        else:
            self.use_joystick = True
        self.game = SpaceBagels(self._screen, clock)
        self.game._set_input_method(self.use_joystick)

        def _main_menu_callback():
            self._screen.fill((40, 0, 40))

        def _resume_callback():
            self.menu.disable()
            self.game.main()
            self.game._set_input_method(self.use_joystick)

        def _new_game_callback():
            self.menu.disable()
            self.game = SpaceBagels(self._screen, clock)
            self.game._set_input_method(self.use_joystick)
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

        settings_menu = pygameMenu.Menu(self._screen,
                                        bgfun=_main_menu_callback,
                                        font=pygameMenu.fonts.FONT_8BIT,
                                        menu_alpha=90,
                                        onclose=PYGAME_MENU_BACK,
                                        title='Settings',
                                        window_width=DESIRED_RESOLUTION[0],
                                        window_height=DESIRED_RESOLUTION[1])

        def _select_input_method(method):
            if method == 'Keyboard':
                self.use_joystick = False
            elif method == 'Joystick':
                self.use_joystick = True
            else:
                raise ValueError
            self.game._set_input_method(self.use_joystick)

        if pygame.joystick.get_count() < 2:
            options = [('Keyboard', 'Keyboard')]
        else:
            options = [('Joystick', 'Joystick'), ('Keyboard', 'Keyboard')]
        settings_menu.add_selector('Input',
                                   options,
                                   onreturn=None,
                                   onchange=_select_input_method)

        self.menu.add_option('New Game', _new_game_callback)
        self.menu.add_option('Settings', settings_menu)
        self.menu.add_option('Exit', PYGAME_MENU_EXIT)

    def process_inputs(self, events):
        self.menu.enable()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.menu.mainloop(events)


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
