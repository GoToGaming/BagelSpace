import os
import random as rand

import numpy as np
import pygame

from src import Constants, Tools


class MeteoriteController:
    METEORITE_TARGET_COUNT = Constants.METEORITE_TARGET_COUNT
    meteorites = []
    METEORITE_FILE_NAMES = [os.path.join(os.path.dirname(__file__), '..', 'img', 'meteorite.png'),
                            os.path.join(os.path.dirname(__file__), '..', 'img', 'meteorite1.png'),
                            os.path.join(os.path.dirname(__file__), '..', 'img', 'meteorite2.png')]

    def __init__(self):
        self.meteoroid_images = []
        for image_path in self.METEORITE_FILE_NAMES:
            self.meteoroid_images.append(Tools.load_image(image_path, fixed_hight_pixels=Constants.METEORITE_HEIGHT))

    def tick(self):
        if len(self.meteorites) < self.METEORITE_TARGET_COUNT:
            self.spawn_meteorite()

        for meteorite in self.meteorites:
            meteorite.tick()
            if 0 > meteorite.position[0] or meteorite.position[0] > Constants.DESIRED_RESOLUTION[0]:
                self.meteorites.remove(meteorite)

    def spawn_meteorite(self):
        direction = rand.choice([-1, 1])
        if direction == 1:
            x = Constants.DESIRED_RESOLUTION[0] / 2
        else:
            x = Constants.DESIRED_RESOLUTION[0] / 2 - Constants.METEORITE_HEIGHT  # not exact with would need to be subtracted
        y = rand.randint(0, Constants.DESIRED_RESOLUTION[1] - Constants.METEORITE_HEIGHT)
        meteorite_speed_range = Constants.MAX_METEORITE_SPEED - Constants.MIN_METEORITE_SPEED
        speed = (rand.random() * meteorite_speed_range) + Constants.MIN_METEORITE_SPEED
        health = np.min([10**(np.random.exponential(Constants.METEORITE_HEALTH_BETA) + 1), Constants.MAX_METEORITE_HEALTH])
        meteorite = Meteorite((x, y), (speed*direction, 0), health, self.meteoroid_images)
        self.meteorites.append(meteorite)

    def blit(self, screen):
        for meteorite in self.meteorites:
            meteorite.blit(screen)


class Meteorite(pygame.sprite.Sprite):

    def __init__(self, pos, velocity, health, meteoroid_images):
        super().__init__()
        self.position = np.array(pos)
        self.velocity = np.array(velocity)
        self.health = float(health)
        self.scrape_sound_played = False

        self.sprite = rand.choice(meteoroid_images).copy()
        alpha = np.log10(self.health)
        alpha = np.clip(alpha * 100, Constants.MIN_METEORITE_SPRITE_ALPHA, Constants.MAX_METEORITE_SPRITE_ALPHA)
        alpha = 255 - alpha
        self.sprite.fill((alpha, alpha, alpha, alpha), special_flags=pygame.BLEND_MULT)

    def tick(self):
        self.position += self.velocity

    def blit(self, screen):
        screen.blit(self.sprite, self.position)

    @property
    def rect(self):
        rect = self.sprite.get_rect()
        rect.x, rect.y = self.position
        diff = np.array(rect.size) * -0.1
        diff = diff.astype(int)
        rect = rect.inflate(*diff)
        return rect

    def damage_meteorite(self, diff):
        self.health -= diff
        if self.health <= 0:
            self.health = 0
            return True
        return False
