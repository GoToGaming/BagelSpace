import numpy as np
import os
import pygame

from src import Constants, Tools
from src.SpaceShip import SpaceShip
from src.Meteorite import MeteoriteController


class Main:
    BACKGROUND_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'background.png')

    def __init__(self, screen, clock):
        self._screen = screen
        self._clock = clock
        self.background_sprite = Tools.load_image(Main.BACKGROUND_FILE_NAME, Constants.GAME_SCALE)
        player_left_sprite = Tools.load_image(SpaceShip.SPRITE_LEFT_FILE_NAME, fixed_hight_pixels=Constants.SPACE_SHIP_HEIGHT)
        self.player_left = SpaceShip((200, 360), SpaceShip.SPACE_SHIP_IS_LEFT, player_left_sprite)
        player_right_sprite = Tools.load_image(SpaceShip.SPRITE_RIGHT_FILE_NAME, fixed_hight_pixels=Constants.SPACE_SHIP_HEIGHT)
        self.player_right = SpaceShip((1000, 360), SpaceShip.SPACE_SHIP_IS_RIGHT, player_right_sprite)
        self.meteorite_controller = MeteoriteController()
        self.running = True
        self.game_ended = ''
        self.game_ended_time = 0
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
                else:
                    self.process_input(e)

            if not self.running:
                return

            self.last_frametime += self._clock.tick()
            tick_count = int(self.last_frametime // Constants.TARGET_FRAMETIME_MS)
            self.last_frametime = self.last_frametime % Constants.TARGET_FRAMETIME_MS

            self.tick(tick_count)
            pygame.display.flip()

    def process_input(self, event):
        if not self.running:
            return

        if self.use_joystick:
            if event.type in (pygame.JOYHATMOTION, pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN):
                if event.type == pygame.JOYBUTTONDOWN and self.game_ended:
                    if self.game_ended_time + 2500 < pygame.time.get_ticks():
                        self.running = False
                        return

                if event.dict['joy'] == 0:
                    self.player_left.process_input(event, None)
                elif event.dict['joy'] == 1:
                    self.player_right.process_input(event, None)
        else:
            if event.type in (pygame.KEYUP, pygame.KEYDOWN):
                if event.type == pygame.KEYDOWN and self.game_ended:
                    if self.game_ended_time + 2500 < pygame.time.get_ticks():
                        self.running = False
                        return

                if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE):
                    self.player_left.process_input(event, Constants.KEYBOARD_MAPPING[event.key])
                elif event.key in (pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_RETURN):
                    self.player_right.process_input(event, Constants.KEYBOARD_MAPPING[event.key])

    def tick(self, tick_count):
        if not self.running:
            return

        for tick in range(tick_count):
            self.player_left.tick()
            self.player_right.tick()
            self.meteorite_controller.tick()
            if not self.game_ended:
                self._detect_collisions()
        self.blit()

    def draw_text_centered(self, string, size, x_middle, y_middle, color=Constants.YELLOW):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(string, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x_middle, y_middle)
        self._screen.blit(text_surface, text_rect)

    def draw_text_left_edge(self, string, size, x, y, color=Constants.YELLOW):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(string, True, color)
        self._screen.blit(text_surface, (x, y))

    def blit(self):
        self._screen.blit(self.background_sprite, (0, 0))
        self.meteorite_controller.blit(self._screen)

        if self.game_ended:
            self._blit_game_ended_screen()
        else:
            self.player_left.blit(self._screen)
            self.player_right.blit(self._screen)
            self._blit_status_bar()

    def _blit_game_ended_screen(self):
        res = np.array(Constants.DESIRED_RESOLUTION)
        rect = pygame.Rect(res/4, res/2)
        self._screen.fill((0, 0, 0), rect)
        winner = self.game_ended
        font_size = 80
        self.draw_text_centered('Game over!',
                                font_size,
                                Constants.DESIRED_RESOLUTION[0] / 2,
                                Constants.DESIRED_RESOLUTION[1] / 2 - font_size,
                                color=Constants.WHITE)
        self.draw_text_centered('Winner is {}'.format(winner),
                                font_size,
                                Constants.DESIRED_RESOLUTION[0] / 2,
                                Constants.DESIRED_RESOLUTION[1] / 2,
                                color=Constants.WHITE)
        if self.game_ended_time + 2500 < pygame.time.get_ticks():
            font_size = 40
            self.draw_text_centered('Press any key to return to menu.'.format(winner),
                                    font_size,
                                    Constants.DESIRED_RESOLUTION[0] / 2,
                                    Constants.DESIRED_RESOLUTION[1] / 2 + 3 * font_size,
                                    color=Constants.WHITE)

    def _blit_status_bar(self):
        self.draw_text_centered(f'{int(np.ceil(self.player_left.health_percentage))}%',
                                30,
                                Constants.DESIRED_RESOLUTION[0] / 4,
                                15,
                                color=Constants.RED)
        self.draw_text_centered(f'{int(np.ceil(self.player_right.health_percentage))}%',
                                30,
                                3 * Constants.DESIRED_RESOLUTION[0] / 4,
                                15,
                                color=Constants.LIGHT_BLUE)

    def _detect_collisions(self):
        self.compute_missile_ship_collisions()
        self.compute_meteorite_ship_collisions()
        self.compute_meteorite_missile_collisions()
        self.compute_missile_missile_collisions()

        if self.player_left.health_percentage == 0:
            self.game_ended = SpaceShip.SPACE_SHIP_IS_RIGHT
        elif self.player_right.health_percentage == 0:
            self.game_ended = SpaceShip.SPACE_SHIP_IS_LEFT
        if self.game_ended:
            self.game_ended_time = pygame.time.get_ticks()

    def compute_missile_ship_collisions(self):
        player_left_objects = self.player_left.get_objects()
        player_right_objects = self.player_right.get_objects()

        hit_left_player = pygame.sprite.spritecollideany(self.player_left, player_right_objects)
        if hit_left_player:
            self.player_right.missile_has_collided(hit_left_player)
            self.player_left.damage_ship(health_percentage_diff=10)

        hit_right_player = pygame.sprite.spritecollideany(self.player_right, player_left_objects)
        if pygame.sprite.spritecollideany(self.player_right, player_left_objects):
            self.player_left.missile_has_collided(hit_right_player)
            self.player_right.damage_ship(health_percentage_diff=10)

    def compute_meteorite_ship_collisions(self):
        meteorites = self.meteorite_controller.meteorites

        hit_left_player = pygame.sprite.spritecollideany(self.player_left, meteorites)
        if hit_left_player:
            self.player_left.damage_ship(health_percentage_diff=0.1)

        hit_right_player = pygame.sprite.spritecollideany(self.player_right, meteorites)
        if hit_right_player:
            self.player_right.damage_ship(health_percentage_diff=0.1)

    def compute_meteorite_missile_collisions(self):
        missiles_left = pygame.sprite.Group(missile for missile in self.player_left.missiles)
        missiles_right = pygame.sprite.Group(missile for missile in self.player_right.missiles)
        meteorites = pygame.sprite.Group(meteorite for meteorite in self.meteorite_controller.meteorites)

        collision_dict_left = pygame.sprite.groupcollide(meteorites, missiles_left, False, True)
        collision_dict_right = pygame.sprite.groupcollide(meteorites, missiles_right, False, True)

        for meteorite, missiles in collision_dict_left.items():
            if meteorite.damage_meteorite(50):
                self.meteorite_controller.meteorites.remove(meteorite)
        for meteorite, missiles in collision_dict_right.items():
            if meteorite.damage_meteorite(50):
                self.meteorite_controller.meteorites.remove(meteorite)

        self.player_left.missiles = [missile for missile in missiles_left]
        self.player_right.missiles = [missile for missile in missiles_right]

    def compute_missile_missile_collisions(self):
        missiles_left = pygame.sprite.Group(missile for missile in self.player_left.missiles)
        missiles_right = pygame.sprite.Group(missile for missile in self.player_right.missiles)

        pygame.sprite.groupcollide(missiles_left, missiles_right, True, True)

        self.player_left.missiles = [missile for missile in missiles_left]
        self.player_right.missiles = [missile for missile in missiles_right]

    def _set_input_method(self, use_joystick):
        self.use_joystick = use_joystick
