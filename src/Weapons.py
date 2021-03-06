import os

import numpy as np
import pygame

import src.Constants as Constants
from src.Animation import Animation
from src.Tools import load_image


class MachineGun:
    def __init__(self, is_right_player, offset, sound):
        self.sound = sound
        self.fire_rate = Constants.MACHINE_GUN_FIRE_RATE
        self.cooldown = self.fire_rate
        self.projectile_speed = Constants.MACHINE_GUN_PROJECTILE_SPEED
        self.is_right_player = is_right_player
        self.offset = offset
        machine_gun_projectile_image_path = os.path.join(os.path.dirname(__file__), '..', 'img', 'machine_gun_bullet')
        self.machine_gun_projectile_image = load_image(machine_gun_projectile_image_path, Constants.GAME_SCALE, animation=True, flip_x=self.is_right_player)

    def fire(self, position):
        if self.cooldown == 0:
            self.sound.machine_gun_shot.play()
            velocity_x = self.projectile_speed
            if self.is_right_player:
                velocity_x = -velocity_x
            position[1] -= self.offset
            projectile = MachineGunProjectile(position, (velocity_x, 0), self.machine_gun_projectile_image)
            self.cooldown = self.fire_rate
            return projectile
        return None

    def tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1


class MachineGunProjectile(pygame.sprite.Sprite):

    def __init__(self, position, velocity, machine_gun_projectile_image):
        super().__init__()
        self.animation = Animation(machine_gun_projectile_image, 10)
        self.position = np.array(position)
        self.position[1] -= int(self.animation.get_current_image().get_height() / 2)
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
    machine_gun_ship_impact_image = None
    MACHINE_GUN_IMPACT_METEOROID_EFFECT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'mg_impact_met')
    machine_gun_meteoroid_impact_image = None

    def __init__(self, position, is_meteoroid_collision):
        super().__init__()

        self.effect_speed = 2
        if is_meteoroid_collision:
            if not MachineGunImpactEffect.machine_gun_meteoroid_impact_image:
                MachineGunImpactEffect.machine_gun_meteoroid_impact_image = load_image(self.MACHINE_GUN_IMPACT_METEOROID_EFFECT_FILE_NAME,
                                                                                       Constants.GAME_SCALE, animation=True)
            self.animation = Animation(MachineGunImpactEffect.machine_gun_meteoroid_impact_image, self.effect_speed)
        else:
            if not MachineGunImpactEffect.machine_gun_ship_impact_image:
                MachineGunImpactEffect.machine_gun_ship_impact_image = load_image(self.MACHINE_GUN_IMPACT_EFFECT_FILE_NAME,
                                                                                  Constants.GAME_SCALE, animation=True)
            self.animation = Animation(MachineGunImpactEffect.machine_gun_ship_impact_image, self.effect_speed)

        self.effect_counter = self.effect_speed * len(self.animation.animation)
        self.position = position

    def tick(self):
        self.effect_counter -= 1
        if self.effect_counter <= 0:
            return True
        self.animation.update()

    def blit(self, screen):
        screen.blit(self.animation.get_current_image(), self.position)


class MissileLauncher:
    def __init__(self, is_right_player, offset, sound):
        self.sound = sound
        self.fire_rate = Constants.MISSILE_LAUNCHER_FIRE_RATE
        self.cooldown = self.fire_rate
        self.missile_speed = Constants.MACHINE_GUN_PROJECTILE_SPEED
        self.is_right_player = is_right_player
        self.offset = offset
        missile_image_path = os.path.join(os.path.dirname(__file__), '..', 'img', 'rocket')
        self.missile_image = load_image(missile_image_path, Constants.GAME_SCALE, animation=True, flip_x=self.is_right_player)

    def fire(self, position):
        if self.cooldown == 0:
            self.sound.missile_shot.play()
            velocity_x = self.missile_speed
            if self.is_right_player:
                velocity_x = -velocity_x
            position[1] -= self.offset
            projectile = Missile(position, (velocity_x, 0), self.missile_image)
            self.cooldown = self.fire_rate
            return projectile
        return None

    def tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1


class Missile(pygame.sprite.Sprite):

    def __init__(self, pos, velocity, missile_image):
        super().__init__()
        self.animation = Animation(missile_image, 4)

        self.position = np.array(pos)
        self.position[1] -= int(self.animation.get_current_image().get_height() / 2)
        self.velocity = np.array(velocity)

        self.damage = Constants.MISSILE_DAMAGE

        self.on_collision_effect = MissileImpact

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


class MissileImpact(pygame.sprite.Sprite):
    MISSILE_IMPACT_EFFECT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'mg_impact')
    missile_ship_impact_image = None
    MISSILE_IMPACT_METEOROID_EFFECT_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'mg_impact_met')
    missile_meteoroid_impact_image = None

    def __init__(self, position, is_meteoroid_collision):
        super().__init__()

        self.effect_speed = 2
        if is_meteoroid_collision:
            if not MissileImpact.missile_meteoroid_impact_image:
                MissileImpact.missile_meteoroid_impact_image = load_image(self.MISSILE_IMPACT_METEOROID_EFFECT_FILE_NAME,
                                                                          Constants.GAME_SCALE, animation=True)
            self.animation = Animation(MissileImpact.missile_meteoroid_impact_image, self.effect_speed)
        else:
            if not MissileImpact.missile_ship_impact_image:
                MissileImpact.missile_ship_impact_image = load_image(self.MISSILE_IMPACT_EFFECT_FILE_NAME,
                                                                     Constants.GAME_SCALE, animation=True)
            self.animation = Animation(MissileImpact.missile_ship_impact_image, self.effect_speed)

        self.effect_counter = self.effect_speed * len(self.animation.animation)
        self.position = position

    def tick(self):
        self.effect_counter -= 1
        if self.effect_counter <= 0:
            return True
        self.animation.update()

    def blit(self, screen):
        screen.blit(self.animation.get_current_image(), self.position)
