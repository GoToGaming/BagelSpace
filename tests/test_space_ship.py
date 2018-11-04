import pygame
import pytest

import src.Constants
from src import Main
from src.SpaceShip import SpaceShip


@pytest.fixture(scope='session')
def test_sprite():
    return pygame.Surface([1, 1])


def test_left_space_ship_initial_position(test_sprite):
    with pytest.raises(ValueError) as e:
        SpaceShip((-1,0), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    with pytest.raises(ValueError) as e:
        SpaceShip((0,-1), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    with pytest.raises(ValueError) as e:
        SpaceShip((-1,-1), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)

    with pytest.raises(ValueError) as e:
        SpaceShip((SpaceShip.MIDDLE_POS,0), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    with pytest.raises(ValueError) as e:
        SpaceShip((0, src.Constants.DESIRED_RESOLUTION[1]), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    with pytest.raises(ValueError) as e:
        SpaceShip((SpaceShip.MIDDLE_POS, src.Constants.DESIRED_RESOLUTION[1]), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)


def test_right_space_ship_initial_position(test_sprite):
    with pytest.raises(ValueError) as e:
        SpaceShip((SpaceShip.MIDDLE_POS-1,0),
                             SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)
    with pytest.raises(ValueError) as e:
        SpaceShip((SpaceShip.MIDDLE_POS,-1),
                             SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)
    with pytest.raises(ValueError) as e:
        SpaceShip((SpaceShip.MIDDLE_POS-1,-1),
                             SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)

    with pytest.raises(ValueError) as e:
        SpaceShip((src.Constants.DESIRED_RESOLUTION[0], 0),
                  SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)
    with pytest.raises(ValueError) as e:
        SpaceShip((SpaceShip.MIDDLE_POS, src.Constants.DESIRED_RESOLUTION[1]),
                  SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)
    with pytest.raises(ValueError) as e:
        SpaceShip(src.Constants.DESIRED_RESOLUTION,
                  SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)


def test_left_space_ship_should_not_move_left(test_sprite):
    space_ship = SpaceShip((0,0), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event, None)
    space_ship.tick()
    assert all(space_ship.position == [0,0])


def test_right_space_ship_should_not_move_left(test_sprite):
    space_ship = SpaceShip((SpaceShip.MIDDLE_POS,0), SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)


def test_right_space_ship_should_not_move_left(test_sprite):
    space_ship = SpaceShip((SpaceShip.MIDDLE_POS, 0), SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event, None)
    space_ship.tick()
    assert all(space_ship.position == [SpaceShip.MIDDLE_POS,0])


def test_left_space_ship_should_not_move_right(test_sprite):
    pos = (SpaceShip.MIDDLE_POS - test_sprite.get_size()[0], 0)
    space_ship = SpaceShip(pos, SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)


def test_left_space_ship_should_not_move_right(test_sprite):
    pos = (SpaceShip.MIDDLE_POS - test_sprite.get_size()[0], 0)
    space_ship = SpaceShip(pos, SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    move_right_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (1, 0)})
    space_ship.process_input(move_right_event, None)
    space_ship.tick()
    assert all(space_ship.position == pos)


def test_right_space_ship_should_not_move_right(test_sprite):
    pos = (src.Constants.DESIRED_RESOLUTION[0] - test_sprite.get_size()[0], 0)
    space_ship = SpaceShip(pos, SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)


def test_right_space_ship_should_not_move_right(test_sprite):
    pos = (src.Constants.DESIRED_RESOLUTION[0] - test_sprite.get_size()[0], 0)
    space_ship = SpaceShip(pos, SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)
    move_right_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (1, 0)})
    space_ship.process_input(move_right_event, None)
    space_ship.tick()
    assert all(space_ship.position == pos)


def test_left_space_ship_should_move_left(test_sprite):
    space_ship = SpaceShip((SpaceShip.DEFAULT_VELOCITY,0),
                                      SpaceShip.SPACE_SHIP_IS_LEFT,
                                      test_sprite)


def test_left_space_ship_should_move_left(test_sprite):
    space_ship = SpaceShip((SpaceShip.DEFAULT_VELOCITY,0), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event, None)
    space_ship.tick()
    assert all(space_ship.position == [0,0])


def test_right_space_ship_should_move_left(test_sprite):
    space_ship = SpaceShip(
        (SpaceShip.MIDDLE_POS+SpaceShip.DEFAULT_VELOCITY,0),
        SpaceShip.SPACE_SHIP_IS_RIGHT,
        test_sprite)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event, None)
    space_ship.tick()
    assert all(space_ship.position == [SpaceShip.MIDDLE_POS,0])


def test_health_percentage_till_death(test_sprite):
    space_ship = SpaceShip(
        (SpaceShip.MIDDLE_POS + SpaceShip.DEFAULT_VELOCITY, 0),
        SpaceShip.SPACE_SHIP_IS_RIGHT,
        test_sprite)
    assert space_ship.health_percentage == 100

    assert space_ship.damage_ship(health_percentage_diff=50) is False
    assert space_ship.health_percentage == 50

    assert space_ship.damage_ship(health_percentage_diff=80) is True
    assert space_ship.health_percentage == 0


def test_health_increase(test_sprite):
    space_ship = SpaceShip(
        (SpaceShip.MIDDLE_POS + SpaceShip.DEFAULT_VELOCITY, 0),
        SpaceShip.SPACE_SHIP_IS_RIGHT,
        test_sprite)
    space_ship.health_percentage = 50

    space_ship.increase_health_percentage(health_percentage_diff=90)
    assert space_ship.health_percentage == 100
