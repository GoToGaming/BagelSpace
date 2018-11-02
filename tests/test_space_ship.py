import pygame
import pytest

from src import BagelSpace


def test_left_space_ship_initial_position():
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((-1,0), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((0,-1), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((-1,-1), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT)

    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS,0), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((0,BagelSpace.DESIRED_RESOLUTION[1]), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS,BagelSpace.DESIRED_RESOLUTION[1]), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT)


def test_right_space_ship_initial_position():
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS-1,0),
                             BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS,-1),
                             BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS-1,-1),
                             BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT)

    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.DESIRED_RESOLUTION[0],0),
                             BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS,BagelSpace.DESIRED_RESOLUTION[1]),
                             BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip(BagelSpace.DESIRED_RESOLUTION,
                             BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT)


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

def test_left_space_ship_should_not_move_right():
    pos = (BagelSpace.SpaceShip.MIDDLE_POS - BagelSpace.SpaceShip.SPRITE_LEFT.get_size()[0], 0)
    space_ship = BagelSpace.SpaceShip(pos, BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT)
    move_right_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (1, 0)})
    space_ship.process_input(move_right_event)
    space_ship.tick(1)
    assert all(space_ship.position == pos)

def test_right_space_ship_should_not_move_right():
    pos = (BagelSpace.DESIRED_RESOLUTION[0] - BagelSpace.SpaceShip.SPRITE_RIGHT.get_size()[0], 0)
    space_ship = BagelSpace.SpaceShip(pos, BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT)
    move_right_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (1, 0)})
    space_ship.process_input(move_right_event)
    space_ship.tick(1)
    assert all(space_ship.position == pos)

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
