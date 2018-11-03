import numpy as np
import pygame
import os
import random as rand

from src import Constants, Tools


class MeteoriteController:
    METEORITE_TARGET_COUNT = Constants.METEORITE_TARGET_COUNT
    meteorites = []

    def tick(self):
        if len(self.meteorites) < self.METEORITE_TARGET_COUNT:
            self.spawn_meteorite()

        for meteorite in self.meteorites:
            meteorite.tick()
            if 0 > meteorite.position[0] or meteorite.position[0] > Constants.DESIRED_RESOLUTION[0]:
                self.meteorites.remove(meteorite)

    def spawn_meteorite(self):
        x = Constants.DESIRED_RESOLUTION[0] / 2
        y = rand.randint(0, Constants.DESIRED_RESOLUTION[1])
        direction = rand.choice([-1, 1])
        meteorite_speed_range = Constants.MAX_METEORITE_SPEED - Constants.MIN_METEORITE_SPEED
        speed = (rand.random() * meteorite_speed_range) + Constants.MIN_METEORITE_SPEED
        meteorite = Meteorite((x, y), (speed*direction, 0))
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
        self.health = 100.

        self.sprite = Tools.load_image(self.METEORITE_FILE_NAME, fixed_hight_pixels=Constants.METEORITE_HEIGHT)

    def tick(self):
        self.position += self.velocity

    def blit(self, screen):
        screen.blit(self.sprite, self.position)

    @property
    def rect(self):
        rect = self.sprite.get_rect()
        rect.x, rect.y = self.position
        return rect

    def damage_meteorite(self, diff):
        self.health -= diff
        if self.health <= 0:
            self.health = 0
            return True
        return False
