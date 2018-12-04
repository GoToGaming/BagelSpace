from enum import Enum

import pygame

DESIRED_RESOLUTION = (1280, 720)
TARGET_FPS = 60
TARGET_FRAMETIME_MS = 1000. / TARGET_FPS
MENU_WIDTH = 900
MENU_HEIGHT = 500
BUTTON_HEIGHT = 50

# ############## game play calibration #######################

GAME_SCALE = 2
SPACE_SHIP_VELOCITY = 4
SPACE_SHIP_VELOCITY_INERTIA = 0.95
SPACE_SHIP_HEIGHT = 80

METEORITE_TARGET_COUNT = 10
METEORITE_HEIGHT = 60
METEORITE_HEALTH_BETA = 0.65
MAX_METEORITE_HEALTH = 1000
MIN_METEORITE_SPRITE_ALPHA = 0
MAX_METEORITE_SPRITE_ALPHA = 192
MIN_METEORITE_SPEED = 1
MAX_METEORITE_SPEED = 4

MISSILE_LAUNCHER_FIRE_RATE = 40
MISSILE_VELOCITY = 5
MISSILE_RELOAD_TIME_SEC = 0.4
MISSILE_DAMAGE = 34

MACHINE_GUN_PROJECTILE_SPEED = 20
MACHINE_GUN_FIRE_RATE = 10
MACHINE_GUN_PROJECTILE_DAMAGE = 2

POWERUP_REGULAR_SPAWN_INTERVAL = 300
POWERUP_HEALTH = 20
POWERUP_X_SPEED = 2


class Button(Enum):
    UP = 0,
    DOWN = 1,
    LEFT = 2,
    RIGHT = 3,
    FIRE = 4,
    SWITCH = 5


KEYBOARD_MAPPING = {pygame.K_UP: Button.UP,
                    pygame.K_w: Button.UP,
                    pygame.K_DOWN: Button.DOWN,
                    pygame.K_s: Button.DOWN,
                    pygame.K_LEFT: Button.LEFT,
                    pygame.K_a: Button.LEFT,
                    pygame.K_RIGHT: Button.RIGHT,
                    pygame.K_d: Button.RIGHT,
                    pygame.K_SPACE: Button.FIRE,
                    pygame.K_RETURN: Button.FIRE,
                    pygame.K_LALT: Button.SWITCH,
                    pygame.K_DELETE: Button.SWITCH}
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (50, 240, 255)
YELLOW = (255, 255, 0)
