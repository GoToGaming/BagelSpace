from enum import Enum

import pygame

DESIRED_RESOLUTION = (1280, 720)
TARGET_FPS = 60
TARGET_FRAMETIME_MS = 1000. / TARGET_FPS
GAME_SCALE = 2
SPACE_SHIP_VELOCITY = 4
SPACE_SHIP_HEIGHT = 80
METEORITE_TARGET_COUNT = 10
METEORITE_HEIGHT = 60
MIN_METEORITE_SPEED = 1
MAX_METEORITE_SPEED = 4

MISSILE_VELOCITY = 5
MISSILE_RELOAD_TIME_SEC = 0.4


class Button(Enum):
    UP = 0,
    DOWN = 1,
    LEFT = 2,
    RIGHT = 3,
    FIRE = 4


KEYBOARD_MAPPING = {pygame.K_UP: Button.UP,
                    pygame.K_w: Button.UP,
                    pygame.K_DOWN: Button.DOWN,
                    pygame.K_s: Button.DOWN,
                    pygame.K_LEFT: Button.LEFT,
                    pygame.K_a: Button.LEFT,
                    pygame.K_RIGHT: Button.RIGHT,
                    pygame.K_d: Button.RIGHT,
                    pygame.K_SPACE: Button.FIRE,
                    pygame.K_RETURN: Button.FIRE}
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
