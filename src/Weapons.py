import os
from src.BagelSpace import Animation, load_image


class MachineGun:

    def __init__(self, fire_rate, projectile_speed, is_right_player):
        self.fire_rate = fire_rate
        self.cooldown = fire_rate
        self.projectile_speed = projectile_speed
        self.projectiles = []
        self.is_right_player = is_right_player

    def fire(self, position):
        if self.cooldown == 0:
            velocity_x = self.projectile_speed
            if self.is_right_player:
                velocity_x = -velocity_x
            projectile = MachineGunProjectile(position, (velocity_x, 0))
            self.projectiles.append(projectile)
            self.cooldown = self.fire_rate

    def tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        for projectile in self.projectiles:
            projectile.tick()


class MachineGunProjectile:

    MACHINE_GUN_PROJECTILE_FILE_NAME = os.path.join(os.path.dirname(__file__), '..', 'img', 'machine_gun_bullet')

    def __init__(self, position, velocity):
        self.animation = Animation(load_image(self.MACHINE_GUN_PROJECTILE_FILE_NAME, 2, animation=True))
        self.position = position
        self.velocity = velocity

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