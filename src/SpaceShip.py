import os

import numpy as np
import pygame

from src import Constants
from src.Meteorite import Meteorite
from src.Weapons import MachineGun, MissileLauncher

from src.Tools import load_image
from src.Animation import Animation


class SpaceShip(pygame.sprite.Sprite):
    SPACE_SHIP_IS_LEFT = 'RED'
    SPACE_SHIP_IS_RIGHT = 'BLUE'
    SPRITE_LEFT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'red_ship_borderless.png')
    SPRITE_RIGHT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'blue_ship_borderless.png')
    EXPLOSION_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'big_explosion')
    DEFAULT_VELOCITY = Constants.SPACE_SHIP_VELOCITY
    MIDDLE_POS = Constants.DESIRED_RESOLUTION[0] / 2

    def __init__(self, position, space_ship_side, sprite, sound):
        super().__init__()
        self.position = np.array(position)
        self.space_ship_side = space_ship_side
        self.sprite = sprite
        self.sound = sound
        self.health_percentage = 100
        self.ship_destroyed = False
        self.rearming_reload_ticks = 0

        self.explosion = Animation(
            load_image(
                self.EXPLOSION_FILE_NAME,
                Constants.GAME_SCALE,
                True),
            7
        )

        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            self.space_ship_bound = np.array([[0, 0],
                                              np.array([Constants.DESIRED_RESOLUTION[0] / 2,
                                                        Constants.DESIRED_RESOLUTION[1]]) - self.sprite.get_size()])
        else:
            self.space_ship_bound = np.array([[Constants.DESIRED_RESOLUTION[0] / 2, 0],
                                              np.array(Constants.DESIRED_RESOLUTION) - self.sprite.get_size()])
        if any(self.space_ship_bound[0] > self.position) or any(self.position > self.space_ship_bound[1]):
            raise ValueError
        self.velocity = np.array([0, 0], dtype=float)
        self.target_velocity = np.array([0, 0])
        self.firing = False
        self.projectiles = []
        self.effects = []
        self.weapons = []
        self.weapons.append([MachineGun(self.space_ship_side == self.SPACE_SHIP_IS_RIGHT, Constants.SPACE_SHIP_HEIGHT/10, self.sound),
                             MachineGun(self.space_ship_side == self.SPACE_SHIP_IS_RIGHT, -Constants.SPACE_SHIP_HEIGHT/10, self.sound)])
        self.weapons.append([MissileLauncher(self.space_ship_side == self.SPACE_SHIP_IS_RIGHT, 0, self.sound)])
        self._active_weapon_idx = 0
        self.active_weapon = self.weapons[self._active_weapon_idx]
        self.bagel_mode = 0
        self.previous_move = ''

    def damage_ship(self, health_percentage_diff):
        self.health_percentage -= health_percentage_diff
        if self.health_percentage <= 0:
            self.health_percentage = 0
            self.ship_destroyed = True
            self.sound.ship_explosion.play()
        return self.ship_destroyed

    def increase_health_percentage(self, health_percentage_diff):
        new_health_percentage = self.health_percentage + int(health_percentage_diff)
        if new_health_percentage > 100:
            self.health_percentage = 100
        else:
            self.health_percentage = new_health_percentage

    def process_input(self, event, button):
        if event.type == pygame.JOYHATMOTION:
            if event.dict['hat'] == 0 and not self.ship_destroyed:
                self.target_velocity = self.DEFAULT_VELOCITY * np.array(event.dict['value'])
                self.target_velocity[1] *= -1
                if event.dict['value'] == (0, 0):
                    self.register_bagel_move()
                else:
                    if event.dict['value'] == (0, 1):
                        self.previous_move = 'up'
                    if event.dict['value'] == (0, -1):
                        self.previous_move = 'down'
                    if event.dict['value'] == (-1, 0):
                        self.previous_move = 'left'
                    if event.dict['value'] == (1, 0):
                        self.previous_move = 'right'
        elif event.type == pygame.JOYAXISMOTION:
            if event.dict['axis'] == 0:
                self.target_velocity[0] = self.DEFAULT_VELOCITY * event.dict['value']
        elif event.type == pygame.JOYBUTTONUP:
            if event.dict['button'] == 1:
                self.firing = False
            elif event.dict['button'] == 2:
                self._active_weapon_idx += 1
                self._active_weapon_idx %= len(self.weapons)
                self.active_weapon = self.weapons[self._active_weapon_idx]
            self.register_bagel_move()
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.dict['button'] == 0:
                self.previous_move = 'a'
            elif event.dict['button'] == 1:
                self.firing = True
                self.previous_move = 'b'
            elif event.dict['button'] == 6:
                self.previous_move = 'select'
            elif event.dict['button'] == 7:
                self.previous_move = 'start'
        elif event.type == pygame.KEYDOWN:
            if button == button.UP:
                self.target_velocity[1] = -self.DEFAULT_VELOCITY
            elif button == Constants.Button.DOWN:
                self.target_velocity[1] = self.DEFAULT_VELOCITY
            if button == Constants.Button.LEFT:
                self.target_velocity[0] = -self.DEFAULT_VELOCITY
            elif button == Constants.Button.RIGHT:
                self.target_velocity[0] = self.DEFAULT_VELOCITY
            if button == Constants.Button.FIRE:
                self.firing = True
            elif button == Constants.Button.SWITCH:
                self._active_weapon_idx += 1
                self._active_weapon_idx %= len(self.weapons)
                self.active_weapon = self.weapons[self._active_weapon_idx]
        elif event.type == pygame.KEYUP:
            if button in (Constants.Button.UP, Constants.Button.DOWN):
                self.target_velocity[1] = 0
            if button in (Constants.Button.LEFT, Constants.Button.RIGHT):
                self.target_velocity[0] = 0
            if button == Constants.Button.FIRE:
                self.firing = False

    def register_bagel_move(self):
        if (self.bagel_mode == 0 and self.previous_move == 'up') or \
                (self.bagel_mode == 1 and self.previous_move == 'up') or \
                (self.bagel_mode == 2 and self.previous_move == 'down') or \
                (self.bagel_mode == 3 and self.previous_move == 'down') or \
                (self.bagel_mode == 4 and self.previous_move == 'left') or \
                (self.bagel_mode == 5 and self.previous_move == 'right') or \
                (self.bagel_mode == 6 and self.previous_move == 'left') or \
                (self.bagel_mode == 7 and self.previous_move == 'right') or \
                (self.bagel_mode == 8 and self.previous_move == 'b') or \
                (self.bagel_mode == 9 and self.previous_move == 'a') or \
                (self.bagel_mode == 10 and self.previous_move == 'select') or \
                (self.bagel_mode == 11 and self.previous_move == 'start'):
            self.bagel_mode += 1
        if self.bagel_mode == 12:
            self.activate_bagel_mode()

    def activate_bagel_mode(self):
        Meteorite.METEORITE_FILE_NAMES = [os.path.join(os.path.dirname(Meteorite.METEORITE_FILE_NAMES[0]), 'bagel.png')]

    def calculate_projectile_start_pos(self):
        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            return self.position + np.array([self.sprite.get_size()[0], int(self.sprite.get_size()[1] / 2)])
        else:
            return self.position + np.array([0, int(self.sprite.get_size()[1] / 2)])

    def tick(self):
        self.velocity *= Constants.SPACE_SHIP_VELOCITY_INERTIA
        self.velocity += (1 - Constants.SPACE_SHIP_VELOCITY_INERTIA) * self.target_velocity
        new_position = self.position + self.velocity
        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            self.position = np.clip(new_position, [0, 0],
                                    np.array([self.MIDDLE_POS, Constants.DESIRED_RESOLUTION[1]]) - self.sprite.get_size())
        else:
            self.position = np.clip(new_position, [self.MIDDLE_POS, 0],
                                    np.array(Constants.DESIRED_RESOLUTION) - self.sprite.get_size())

        if self.ship_destroyed:
            self.explosion.update(False)

        for weapon_set in self.weapons:
            for weapon in weapon_set:
                weapon.tick()

        for weapon in self.active_weapon:

            if self.firing:
                projectile = weapon.fire(self.calculate_projectile_start_pos())
                if projectile:
                    self.projectiles.append(projectile)

        for projectile in self.projectiles.copy():
            projectile.tick()
            if 0 > projectile.position[0] or projectile.position[0] > Constants.DESIRED_RESOLUTION[0]:
                self.projectiles.remove(projectile)

        for effect in self.effects.copy():
            if effect.tick():
                self.effects.remove(effect)

    def projectile_has_collided(self, projectile, is_meteoroid_collision):
        self.effects.append(projectile.on_collision_effect(projectile.position, is_meteoroid_collision))
        self.projectiles.remove(projectile)

    def blit(self, screen):
        screen.blit(self.sprite, self.position)
        for projectile in self.projectiles:
            projectile.blit(screen)
        for effect in self.effects:
            effect.blit(screen)

    def blit_explosion(self, screen):
        screen.blit(self.explosion.get_current_image(), self.position)

    @property
    def rect(self):
        rect = self.sprite.get_rect()
        rect.x, rect.y = self.position
        diff = np.array(rect.size) * -0.1
        diff = diff.astype(int)
        rect = rect.inflate(*diff)
        return rect

    def get_objects(self):
        return [self, *self.projectiles]
