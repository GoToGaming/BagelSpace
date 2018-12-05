import numpy as np
import os
import pygame
from pygameMenu.fonts import FONT_8BIT

from src import Constants, Tools
from src.PowerUp import PowerUpController
from src.SpaceShip import SpaceShip
from src.Meteorite import MeteoriteController


class SpaceBagels:
    BACKGROUND_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'background.png')
    XBOX_X_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'Xbox_button_X.svg.png')
    XBOX_B_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'Xbox_button_B.svg.png')

    def __init__(self, screen, clock, sound):
        self._screen = screen
        self._clock = clock
        self._sound = sound
        self.background_sprite = Tools.load_image(SpaceBagels.BACKGROUND_FILE_NAME, Constants.GAME_SCALE)
        player_left_sprite = Tools.load_image(SpaceShip.SPRITE_LEFT_FILE_NAME, fixed_hight_pixels=Constants.SPACE_SHIP_HEIGHT)
        self.player_left = SpaceShip((200, 360), SpaceShip.SPACE_SHIP_IS_LEFT, player_left_sprite, sound)
        player_right_sprite = Tools.load_image(SpaceShip.SPRITE_RIGHT_FILE_NAME, fixed_hight_pixels=Constants.SPACE_SHIP_HEIGHT)
        self.player_right = SpaceShip((1000, 360), SpaceShip.SPACE_SHIP_IS_RIGHT, player_right_sprite, sound)
        self._xbox_x_sprite = Tools.load_image(self.XBOX_X_FILE_NAME, fixed_hight_pixels=Constants.BUTTON_HEIGHT)
        self._xbox_b_sprite = Tools.load_image(self.XBOX_B_FILE_NAME, fixed_hight_pixels=Constants.BUTTON_HEIGHT)
        self.meteorite_controller = MeteoriteController()
        self.powerup_controller = PowerUpController(sound)
        self.running = True
        self.game_ended = ''
        self.game_ended_time = 0
        self.last_frametime = 0
        self.use_joystick = False

    def main(self):
        self.running = True
        self._clock.tick()
        self._sound.start_game_background_music()

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
                    if self.game_ended_time + 5000 < pygame.time.get_ticks():
                        self.running = False
                        return

                if event.dict['joy'] == 0:
                    self.player_left.process_input(event, None)
                elif event.dict['joy'] == 1:
                    self.player_right.process_input(event, None)
        else:
            if event.type in (pygame.KEYUP, pygame.KEYDOWN):
                if event.type == pygame.KEYDOWN and self.game_ended:
                    if self.game_ended_time + 5000 < pygame.time.get_ticks():
                        self.running = False
                        return

                if event.key in Constants.KEYBOARD_MAPPING_LEFT.keys():
                    self.player_left.process_input(event, Constants.KEYBOARD_MAPPING_LEFT[event.key])
                elif event.key in Constants.KEYBOARD_MAPPING_RIGHT.keys():
                    self.player_right.process_input(event, Constants.KEYBOARD_MAPPING_RIGHT[event.key])

    def tick(self, tick_count):
        if not self.running:
            return

        for tick in range(tick_count):
            self.player_left.tick()
            self.player_right.tick()
            self.meteorite_controller.tick()
            self.powerup_controller.tick()
            if not self.game_ended:
                self._detect_collisions()
        self.blit()

    def draw_text_centered(self, string, size, x_middle, y_middle, color=Constants.YELLOW):
        font = pygame.font.Font(FONT_8BIT, size)
        text_surface = font.render(string, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x_middle, y_middle)
        self._screen.blit(text_surface, text_rect)

    def draw_text_left_edge(self, string, size, x, y, color=Constants.YELLOW):
        font = pygame.font.Font(FONT_8BIT, size)
        text_surface = font.render(string, True, color)
        self._screen.blit(text_surface, (x, y))

    def blit(self):
        self._screen.blit(self.background_sprite, (0, 0))
        self.powerup_controller.blit(self._screen)

        if self.game_ended:
            if self.game_ended_time + 2500 > pygame.time.get_ticks():
                if self.game_ended == SpaceShip.SPACE_SHIP_IS_RIGHT:
                    self.player_right.blit(self._screen)
                    self.meteorite_controller.blit(self._screen)
                    self.player_left.blit_explosion(self._screen)
                else:
                    self.player_left.blit(self._screen)
                    self.meteorite_controller.blit(self._screen)
                    self.player_right.blit_explosion(self._screen)
            else:
                self.meteorite_controller.blit(self._screen)
                self._blit_game_ended_screen()
                self._sound.start_menu_background_music()
        else:
            self.player_left.blit(self._screen)
            self.player_right.blit(self._screen)
            self.meteorite_controller.blit(self._screen)
            self._blit_status_bar()
            self._blit_buttons()

    def _blit_game_ended_screen(self):
        res = np.array(Constants.DESIRED_RESOLUTION)
        rect = pygame.Rect(res/8, res*(6/8))
        self._screen.fill((0, 0, 0), rect)
        winner = self.game_ended
        font_size = 60
        self.draw_text_centered('Game over',
                                font_size,
                                Constants.DESIRED_RESOLUTION[0] / 2,
                                Constants.DESIRED_RESOLUTION[1] / 2 - font_size,
                                color=Constants.WHITE)
        self.draw_text_centered('Winner is {}'.format(winner),
                                font_size,
                                Constants.DESIRED_RESOLUTION[0] / 2,
                                Constants.DESIRED_RESOLUTION[1] / 2,
                                color=Constants.WHITE)
        if self.game_ended_time + 5000 < pygame.time.get_ticks():
            font_size = 30
            self.draw_text_centered('Press any key to return to menu'.format(winner),
                                    font_size,
                                    Constants.DESIRED_RESOLUTION[0] / 2,
                                    Constants.DESIRED_RESOLUTION[1] / 2 + 3 * font_size,
                                    color=Constants.WHITE)

    def _blit_status_bar(self):
        self.draw_text_centered(f'{int(np.ceil(self.player_left.health_percentage))} HP',
                                30,
                                Constants.DESIRED_RESOLUTION[0] / 4,
                                15,
                                color=Constants.RED)
        self.draw_text_centered(f'{int(np.ceil(self.player_right.health_percentage))} HP',
                                30,
                                3 * Constants.DESIRED_RESOLUTION[0] / 4,
                                15,
                                color=Constants.LIGHT_BLUE)

    def _blit_buttons(self):
        font_size = 25
        if self.use_joystick:
            x_pos = (75,
                     Constants.DESIRED_RESOLUTION[1] - 50 - self._xbox_x_sprite.get_height())
            self._screen.blit(self._xbox_x_sprite, x_pos)
            self.draw_text_centered('Change', font_size, x_pos[0] + self._xbox_x_sprite.get_width() / 2, x_pos[1] + self._xbox_x_sprite.get_height() + font_size, color=Constants.BLUE)
            b_pos = (x_pos[0] + self._xbox_x_sprite.get_width() + 100,
                     Constants.DESIRED_RESOLUTION[1] - 50 - self._xbox_b_sprite.get_height())
            self._screen.blit(self._xbox_b_sprite, b_pos)
            self.draw_text_centered('Fire', font_size, b_pos[0] + self._xbox_x_sprite.get_width() / 2, b_pos[1] + self._xbox_x_sprite.get_height() + font_size, color=Constants.RED)

            b_pos = (Constants.DESIRED_RESOLUTION[0] - self._xbox_b_sprite.get_width() - 50,
                     Constants.DESIRED_RESOLUTION[1] - 50 - self._xbox_b_sprite.get_height())
            self._screen.blit(self._xbox_b_sprite, b_pos)
            self.draw_text_centered('Fire', font_size, b_pos[0] + self._xbox_x_sprite.get_width() / 2, b_pos[1] + self._xbox_x_sprite.get_height() + font_size, color=Constants.RED)
            x_pos = (b_pos[0] - 100 - self._xbox_x_sprite.get_width(),
                     Constants.DESIRED_RESOLUTION[1] - 50 - self._xbox_x_sprite.get_height())
            self._screen.blit(self._xbox_x_sprite, x_pos)
            self.draw_text_centered('Change', font_size, x_pos[0] + self._xbox_x_sprite.get_width() / 2, x_pos[1] + self._xbox_x_sprite.get_height() + font_size, color=Constants.BLUE)
        else:
            key_font_size = 30
            x_pos = (100,
                     Constants.DESIRED_RESOLUTION[1] - 75)
            self.draw_text_centered('L ALT', key_font_size, x_pos[0], x_pos[1], color=Constants.BLUE)
            self.draw_text_centered('Change', font_size, x_pos[0], x_pos[1] + 25 + font_size, color=Constants.BLUE)
            b_pos = (x_pos[0] + 165,
                     Constants.DESIRED_RESOLUTION[1] - 75)
            self.draw_text_centered('SPACE', key_font_size, b_pos[0], b_pos[1], color=Constants.RED)
            self.draw_text_centered('Fire', font_size, b_pos[0], b_pos[1] + 25 + font_size, color=Constants.RED)

            b_pos = (Constants.DESIRED_RESOLUTION[0] - 100,
                     Constants.DESIRED_RESOLUTION[1] - 75)
            self.draw_text_centered('ENTER', key_font_size, b_pos[0], b_pos[1], color=Constants.RED)
            self.draw_text_centered('Fire', font_size, b_pos[0], b_pos[1] + 25 + font_size, color=Constants.RED)
            x_pos = (b_pos[0] - 175,
                     Constants.DESIRED_RESOLUTION[1] - 75)
            self.draw_text_centered('DELETE', key_font_size, x_pos[0], x_pos[1], color=Constants.BLUE)
            self.draw_text_centered('Change', font_size, x_pos[0], x_pos[1] + 25 + font_size, color=Constants.BLUE)

    def _detect_collisions(self):
        self.compute_projectile_ship_collisions()
        self.compute_meteorite_ship_collisions()
        self.compute_meteorite_projectile_collisions()
        self.compute_projectile_projectile_collisions()
        self.compute_powerup_ship_collisions()

        if self.player_left.health_percentage == 0:
            self.game_ended = SpaceShip.SPACE_SHIP_IS_RIGHT
        elif self.player_right.health_percentage == 0:
            self.game_ended = SpaceShip.SPACE_SHIP_IS_LEFT
        if self.game_ended:
            self.game_ended_time = pygame.time.get_ticks()

    def compute_projectile_ship_collisions(self):
        player_left_objects = self.player_left.get_objects()
        player_right_objects = self.player_right.get_objects()

        collisions = pygame.sprite.spritecollide(self.player_left, player_right_objects, False)
        for collision in collisions:
            self.player_right.projectile_has_collided(collision, False)
            self.player_left.damage_ship(health_percentage_diff=collision.damage)

        collisions = pygame.sprite.spritecollide(self.player_right, player_left_objects, False)
        for collision in collisions:
            self.player_left.projectile_has_collided(collision, False)
            self.player_right.damage_ship(health_percentage_diff=collision.damage)

    def compute_meteorite_ship_collisions(self):
        meteorites = pygame.sprite.Group(meteorite for meteorite in self.meteorite_controller.meteorites)

        collisions = pygame.sprite.spritecollide(self.player_left, meteorites, False)
        for collision in collisions:
            self.player_left.damage_ship(health_percentage_diff=0.1)
            if not collision.scrape_sound_played:
                self._sound.scrape_asteroid.play()
                collision.scrape_sound_played = True
                self.player_left.velocity /= 6
                collision.velocity /= 3

        collisions = pygame.sprite.spritecollide(self.player_right, meteorites, False)
        for collision in collisions:
            self.player_right.damage_ship(health_percentage_diff=0.1)
            if not collision.scrape_sound_played:
                self._sound.scrape_asteroid.play()
                collision.scrape_sound_played = True
                self.player_right.velocity /= 6
                collision.velocity /= 3

    def compute_meteorite_projectile_collisions(self):
        projectiles_left = pygame.sprite.Group(projectile for projectile in self.player_left.projectiles)
        projectiles_right = pygame.sprite.Group(projectile for projectile in self.player_right.projectiles)
        meteorites = pygame.sprite.Group(meteorite for meteorite in self.meteorite_controller.meteorites)

        collision_dict_left = pygame.sprite.groupcollide(meteorites, projectiles_left, False, True)
        collision_dict_right = pygame.sprite.groupcollide(meteorites, projectiles_right, False, True)

        for meteorite, projectiles in collision_dict_left.items():
            for projectile in projectiles:
                meteorite.damage_meteorite(projectile.damage)
        for meteorite, projectiles in collision_dict_right.items():
            for projectile in projectiles:
                meteorite.damage_meteorite(projectile.damage)

        for meteorite in self.meteorite_controller.meteorites.copy():
            if meteorite.health == 0:
                self.meteorite_controller.meteorites.remove(meteorite)

        for projectiles in collision_dict_left.values():
            for projectile in projectiles:
                self.player_left.projectile_has_collided(projectile, True)
        for projectiles in collision_dict_right.values():
            for projectile in projectiles:
                self.player_right.projectile_has_collided(projectile, True)

    def compute_projectile_projectile_collisions(self):
        projectiles_left = pygame.sprite.Group(projectile for projectile in self.player_left.projectiles)
        projectiles_right = pygame.sprite.Group(projectile for projectile in self.player_right.projectiles)

        pygame.sprite.groupcollide(projectiles_left, projectiles_right, True, True)

        self.player_left.projectiles = [projectile for projectile in projectiles_left]
        self.player_right.projectiles = [projectile for projectile in projectiles_right]

    def compute_powerup_ship_collisions(self):
        powerups = pygame.sprite.Group(powerup for powerup in self.powerup_controller.powerups)

        collisions = pygame.sprite.spritecollide(self.player_left, powerups, True)
        for collided_powerup in collisions:
            collided_powerup.collected(self.player_left)
            self.powerup_controller.remove_powerup(collided_powerup)

        collisions = pygame.sprite.spritecollide(self.player_right, powerups, True)
        for collided_powerup in collisions:
            collided_powerup.collected(self.player_right)
            self.powerup_controller.remove_powerup(collided_powerup)

    def _set_input_method(self, use_joystick):
        self.use_joystick = use_joystick
