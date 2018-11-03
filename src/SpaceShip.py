import numpy as np
import os
import pygame

from src import Constants
from src.Missile import Missile


class SpaceShip(pygame.sprite.Sprite):
    SPACE_SHIP_IS_LEFT = 'RED'
    SPACE_SHIP_IS_RIGHT = 'BLUE'
    SPRITE_LEFT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'red_ship_1.png')
    SPRITE_RIGHT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'blue_ship.png')
    DEFAULT_VELOCITY = Constants.SPACE_SHIP_VELOCITY
    MIDDLE_POS = Constants.DESIRED_RESOLUTION[0] / 2

    def __init__(self, position, space_ship_side, sprite):
        super().__init__()
        self.position = np.array(position)
        self.space_ship_side = space_ship_side
        self.sprite = sprite
        self.health_percentage = 100
        self.ship_destroyed = False
        self.rearming_reload_ticks = 0
        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            self.space_ship_bound = np.array([[0, 0],
                                              np.array([Constants.DESIRED_RESOLUTION[0] / 2,
                                                        Constants.DESIRED_RESOLUTION[1]]) - self.sprite.get_size()])
        else:
            self.space_ship_bound = np.array([[Constants.DESIRED_RESOLUTION[0] / 2, 0],
                                              np.array(Constants.DESIRED_RESOLUTION) - self.sprite.get_size()])
        if any(self.space_ship_bound[0] > self.position) or any(self.position > self.space_ship_bound[1]):
            raise ValueError
        self.velocity = np.array([0, 0])
        self.firing = False
        self.missiles = []

    def damage_ship(self, health_percentage_diff):
        self.health_percentage -= health_percentage_diff
        if self.health_percentage <= 0:
            self.health_percentage = 0
            self.ship_destroyed = True
        return self.ship_destroyed

    def increase_health_percentage(self, health_percentage_diff):
        new_health_percentage = self.health_percentage + int(health_percentage_diff)
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
            elif button == Constants.Button.DOWN:
                self.velocity[1] = self.DEFAULT_VELOCITY
            if button == Constants.Button.LEFT:
                self.velocity[0] = -self.DEFAULT_VELOCITY
            elif button == Constants.Button.RIGHT:
                self.velocity[0] = self.DEFAULT_VELOCITY
            if button == Constants.Button.FIRE:
                self.firing = True
        elif event.type == pygame.KEYUP:
            if button in (Constants.Button.UP, Constants.Button.DOWN):
                self.velocity[1] = 0
            if button in (Constants.Button.LEFT, Constants.Button.RIGHT):
                self.velocity[0] = 0
            if button == Constants.Button.FIRE:
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
                                    np.array([self.MIDDLE_POS, Constants.DESIRED_RESOLUTION[1]]) - self.sprite.get_size())
            missile_velocity = (Constants.MISSILE_VELOCITY, 0)
        else:
            self.position = np.clip(new_position, [self.MIDDLE_POS, 0],
                                    np.array(Constants.DESIRED_RESOLUTION) - self.sprite.get_size())
            missile_velocity = (-Constants.MISSILE_VELOCITY, 0)

        if self.space_ship_side == self.SPACE_SHIP_IS_LEFT:
            is_right_player = False
        else:
            is_right_player = True

        if self.rearming_reload_ticks > 0:
            self.rearming_reload_ticks -= 1
        if self.firing and self.rearming_reload_ticks <= 0:
            self.missiles.append(Missile(self.calculate_missile_start_pos(), missile_velocity, is_right_player))
            self.rearming_reload_ticks = int(Missile.RELOAD_TIME_SEC * 60)
        for missile in self.missiles.copy():
            missile.tick()
            if 0 > missile.position[0] or missile.position[0] > Constants.DESIRED_RESOLUTION[0]:
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
