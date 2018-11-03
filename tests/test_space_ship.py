import pygame
import pytest

from src import BagelSpace


@pytest.fixture(scope='session')
def test_sprite():
    return pygame.Surface([1, 1])


def test_left_space_ship_initial_position(test_sprite):
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((-1,0), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((0,-1), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((-1,-1), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)

    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS,0), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((0,BagelSpace.DESIRED_RESOLUTION[1]), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS,BagelSpace.DESIRED_RESOLUTION[1]), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)


def test_right_space_ship_initial_position(test_sprite):
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS-1,0),
                             BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS,-1),
                             BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS-1,-1),
                             BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)

    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.DESIRED_RESOLUTION[0],0),
                             BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS,BagelSpace.DESIRED_RESOLUTION[1]),
                             BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)
    with pytest.raises(ValueError) as e:
        BagelSpace.SpaceShip(BagelSpace.DESIRED_RESOLUTION,
                             BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)


def test_left_space_ship_should_not_move_left(test_sprite):
    space_ship = BagelSpace.SpaceShip((0,0), BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event)
    space_ship.tick()
    assert all(space_ship.position == [0,0])

def test_right_space_ship_should_not_move_left(test_sprite):
    space_ship = BagelSpace.SpaceShip((BagelSpace.SpaceShip.MIDDLE_POS,0), BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event)
    space_ship.tick()
    assert all(space_ship.position == [BagelSpace.SpaceShip.MIDDLE_POS,0])

def test_left_space_ship_should_not_move_right(test_sprite):
    pos = (BagelSpace.SpaceShip.MIDDLE_POS - test_sprite.get_size()[0], 0)
    space_ship = BagelSpace.SpaceShip(pos, BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite)
    move_right_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (1, 0)})
    space_ship.process_input(move_right_event)
    space_ship.tick()
    assert all(space_ship.position == pos)

def test_right_space_ship_should_not_move_right(test_sprite):
    pos = (BagelSpace.DESIRED_RESOLUTION[0] - test_sprite.get_size()[0], 0)
    space_ship = BagelSpace.SpaceShip(pos, BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite)
    move_right_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (1, 0)})
    space_ship.process_input(move_right_event)
    space_ship.tick()
    assert all(space_ship.position == pos)

def test_left_space_ship_should_move_left(test_sprite):
    space_ship = BagelSpace.SpaceShip((BagelSpace.SpaceShip.DEFAULT_VELOCITY,0),
                                      BagelSpace.SpaceShip.SPACE_SHIP_IS_LEFT,
                                      test_sprite)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event)
    space_ship.tick()
    assert all(space_ship.position == [0,0])

def test_right_space_ship_should_move_left(test_sprite):
    space_ship = BagelSpace.SpaceShip(
        (BagelSpace.SpaceShip.MIDDLE_POS+BagelSpace.SpaceShip.DEFAULT_VELOCITY,0),
        BagelSpace.SpaceShip.SPACE_SHIP_IS_RIGHT,
        test_sprite)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event)
    space_ship.tick()
    assert all(space_ship.position == [BagelSpace.SpaceShip.MIDDLE_POS,0])
