import os
from src.Animation import Animation
from src.Tools import load_image
from src.Constants import MACHINE_GUN_PROJECTILE_SPEED, MACHINE_GUN_FIRE_RATE, MACHINE_GUN_PROJECTILE_DAMAGE
import pygame

import src.Sound as sound


class MachineGun:

    def __init__(self, is_right_player, offset):
        self.fire_rate = MACHINE_GUN_FIRE_RATE
        self.cooldown = self.fire_rate
        self.projectile_speed = MACHINE_GUN_PROJECTILE_SPEED
        self.projectiles = []
        self.is_right_player = is_right_player
        self.offset = offset

    def fire(self, position):
        if self.cooldown == 0:
            velocity_x = self.projectile_speed
            if self.is_right_player:
                velocity_x = -velocity_x
            position[1] -= self.offset
            projectile = MachineGunProjectile(position, (velocity_x, 0), is_player_right=self.is_right_player)
            self.cooldown = self.fire_rate
            sound.machine_gun_shot.play()
            return projectile
        return None

    def tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def blit(self, screen):
        for projectile in self.projectiles:
            projectile.blit(screen)


class MachineGunProjectile(pygame.sprite.Sprite):

    MACHINE_GUN_PROJECTILE_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'machine_gun_bullet')

    def __init__(self, position, velocity, is_player_right):
        super().__init__()

        self.animation = Animation(load_image(self.MACHINE_GUN_PROJECTILE_FILE_NAME, 2, animation=True,
                                              flip_x=is_player_right), 10)
        self.position = position
        self.velocity = velocity

        self.damage = MACHINE_GUN_PROJECTILE_DAMAGE

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