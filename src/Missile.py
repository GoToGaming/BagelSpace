import numpy as np
import pygame
import os

from src import Animation, Constants, Tools


class Missile(pygame.sprite.Sprite):
    MISSILE_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'rocket')
    RELOAD_TIME_SEC = Constants.MISSILE_RELOAD_TIME_SEC

    def __init__(self, pos, velocity, is_right_player):
        super().__init__()
        self.position = np.array(pos)
        self.velocity = np.array(velocity)

        self.animation = Animation.Animation(Tools.load_image(self.MISSILE_FILE_NAME, Constants.GAME_SCALE, animation=True, flip_x=is_right_player), 4)

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
