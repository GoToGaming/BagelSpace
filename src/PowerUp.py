import os
import random as rand
from math import sin
import numpy as np
import pygame

from src.Animation import Animation
from src.Tools import load_image

from src import Constants, Tools


class PowerUpController:
    POWERUP_REGULAR_SPAWN_INTERVAL = Constants.POWERUP_REGULAR_SPAWN_INTERVAL
    powerups = []
    ticks_since_last_powerup = 0

    def __init__(self):
        self.switch = rand.choice([-1,1])

    def tick(self):
        self.ticks_since_last_powerup += 1

        if self.ticks_since_last_powerup >= self.POWERUP_REGULAR_SPAWN_INTERVAL:
            self.ticks_since_last_powerup = 0
            self.spawn_power_up()

        for powerup in self.powerups:
            powerup.tick()
            if 0 > powerup.position[0] or powerup.position[0] > Constants.DESIRED_RESOLUTION[0]:
                self.powerups.remove(powerup)

    def spawn_power_up(self):
        x = (Constants.DESIRED_RESOLUTION[0] / 2)
        y = rand.randint(100, Constants.DESIRED_RESOLUTION[1]-100)
        direction = self.switch * Constants.POWERUP_X_SPEED
        self.switch *= -1
        powerup = PowerUp((x, y), direction)
        powerup.position = np.array((powerup.position[0]-powerup.animation.get_current_image().get_size()[0], y))
        self.powerups.append(powerup)

    def blit(self, screen):
        for powerup in self.powerups:
            powerup.blit(screen)

    def remove_powerup(self, powerup):
        self.powerups.remove(powerup)


class PowerUp(pygame.sprite.Sprite):
    POWERUP_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'blue_powerup')

    def __init__(self, position, direction):
        super().__init__()

        self.animation = Animation(load_image(self.POWERUP_FILE_NAME, Constants.GAME_SCALE, animation=True), 5)

        self.position = position
        self.velocity = np.array((direction, 0))
        self.timer = 0

    def tick(self):
        self.timer += 0.1
        y = sin(self.timer)*2
        self.velocity = np.array((self.velocity[0],y))
        self.position += self.velocity

        self.animation.update()

    def blit(self, screen):
        sprite = self.animation.get_current_image()
        screen.blit(sprite, self.position)

    @property
    def rect(self):
        sprite = self.animation.get_current_image()
        rect = sprite.get_rect()
        rect.x, rect.y = self.position
        diff = np.array(rect.size) * -0.1
        diff = diff.astype(int)
        rect = rect.inflate(*diff)
        return rect

    def collected(self, player):
        player.increase_health_percentage(Constants.POWERUP_HEALTH)
