import os

import numpy as np
import pygame

import src.Constants as Constants
from src.Animation import Animation
from src.Tools import load_image

import src.Sound as sound


class MachineGun:
    def __init__(self, is_right_player, offset):
        self.fire_rate = Constants.MACHINE_GUN_FIRE_RATE
        self.cooldown = self.fire_rate
        self.projectile_speed = Constants.MACHINE_GUN_PROJECTILE_SPEED
        self.is_right_player = is_right_player
        self.offset = offset

    def fire(self, position):
        if self.cooldown == 0:
            sound.machine_gun_shot.play()
            velocity_x = self.projectile_speed
            if self.is_right_player:
                velocity_x = -velocity_x
            position[1] -= self.offset
            projectile = MachineGunProjectile(position, (velocity_x, 0), is_player_right=self.is_right_player)
            self.cooldown = self.fire_rate
            return projectile
        return None

    def tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1


class MachineGunProjectile(pygame.sprite.Sprite):
    MACHINE_GUN_PROJECTILE_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'machine_gun_bullet')

    def __init__(self, position, velocity, is_player_right):
        super().__init__()

        self.animation = Animation(load_image(self.MACHINE_GUN_PROJECTILE_FILE_NAME, Constants.GAME_SCALE,
                                              animation=True, flip_x=is_player_right), 10)
        self.position = position
        self.velocity = velocity

        self.damage = Constants.MACHINE_GUN_PROJECTILE_DAMAGE

        self.on_collision_effect = MachineGunImpactEffect

    def tick(self):
        self.position += self.velocity
        self.animation.update()

    def blit(self, screen):
        screen.blit(self.animation.get_current_image(), self.position)

    @property
    def rect(self):
        rect = self.animation.get_current_image().get_rect()
        rect.x, rect.y = self.position
        diff = np.array(rect.size) * -0.1
        diff = diff.astype(int)
        rect = rect.inflate(*diff)
        return rect


class MachineGunImpactEffect(pygame.sprite.Sprite):
    MACHINE_GUN_IMPACT_EFFECT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'mg_impact')
    MACHINE_GUN_IMPACT_METEOROID_EFFECT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'mg_impact_met')

    def __init__(self, position, is_meteoroid_collision):
        super().__init__()

        self.effect_speed = 2
        if is_meteoroid_collision:
            self.animation = Animation(
                load_image(self.MACHINE_GUN_IMPACT_METEOROID_EFFECT_FILE_NAME, Constants.GAME_SCALE,
                           animation=True), self.effect_speed)
        else:
            self.animation = Animation(
                load_image(self.MACHINE_GUN_IMPACT_EFFECT_FILE_NAME, Constants.GAME_SCALE,
                           animation=True), self.effect_speed)

        self.effect_counter = self.effect_speed * len(self.animation.animation)
        self.position = position

    def tick(self):
        self.effect_counter -= 1
        if self.effect_counter <= 0:
            return True
        self.animation.update()

    def blit(self, screen):
        screen.blit(self.animation.get_current_image(), self.position)
