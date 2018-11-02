import pygame
import pytest

from src import BagelSpace


def test_left_space_ship_initial_position():
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((-1,-1), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT)

def test_left_space_ship_should_not_move_left():
    space_ship = BagelSpace.SpaceShip((0,0), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event)
    space_ship.tick(1)
    assert all(space_ship.position == [0,0])

def test_right_space_ship_should_not_move_left():
    space_ship = BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS,0), BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event)
    space_ship.tick(1)
    assert all(space_ship.position == [BagelSpace.SpaceShip.MIDDLE_POS,0])

def test_left_space_ship_should_move_left():
    space_ship = BagelSpace.SpaceShip((BagelSpace.SpaceShip.DEFAULT_VELOCITY,0), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event)
    space_ship.tick(1)
    assert all(space_ship.position == [0,0])

def test_right_space_ship_should_move_left():
    space_ship = BagelSpace.SpaceShip(
        (BagelSpace.SpaceShip.MIDDLE_POS+BagelSpace.SpaceShip.DEFAULT_VELOCITY,0),
        BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event)
    space_ship.tick(1)
    assert all(space_ship.position == [BagelSpace.SpaceShip.MIDDLE_POS,0])
