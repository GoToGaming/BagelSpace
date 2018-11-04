import pygame
import pytest

import src.Constants
from src import Main
from src.SpaceShip import SpaceShip


@pytest.fixture(scope='session')
def test_sprite():
    return pygame.Surface([1, 1])


@pytest.fixture(scope='function')
def mock_image(monkeypatch):
    def transform_mock(*args):
        return FakeImage()

    class FakeImage(object):
        def convert_alpha(self):
            return self

        def get_size(self):
            return [0,0]

    class FakeImageLoader(object):
        def __init__(self):
            self.image_count = 1
            self.current_image = 0

        def mock_image_load(self, path):
            if self.current_image < self.image_count:
                self.current_image += 1
                return FakeImage()
            else:
                self.current_image = 0
                raise pygame.error()

    fake_image_loader = FakeImageLoader()
    monkeypatch.setattr(pygame.image, 'load', fake_image_loader.mock_image_load)
    monkeypatch.setattr(pygame.transform, 'scale', transform_mock)
    monkeypatch.setattr(pygame.transform, 'flip', transform_mock)


@pytest.fixture(scope='function')
def mock_inertia(request):
    initial = src.Constants.SPACE_SHIP_VELOCITY_INERTIA
    src.Constants.SPACE_SHIP_VELOCITY_INERTIA = 0

    def reset():
        src.Constants.SPACE_SHIP_VELOCITY_INERTIA = initial
    request.addfinalizer(reset)


def test_left_space_ship_initial_position(test_sprite, mock_image):
    with pytest.raises(ValueError) as e:
        SpaceShip((-1,0), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite, None)
    with pytest.raises(ValueError) as e:
        SpaceShip((0,-1), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite, None)
    with pytest.raises(ValueError) as e:
        SpaceShip((-1,-1), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite, None)

    with pytest.raises(ValueError) as e:
        SpaceShip((SpaceShip.MIDDLE_POS,0), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite, None)
    with pytest.raises(ValueError) as e:
        SpaceShip((0, src.Constants.DESIRED_RESOLUTION[1]), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite, None)
    with pytest.raises(ValueError) as e:
        SpaceShip((SpaceShip.MIDDLE_POS, src.Constants.DESIRED_RESOLUTION[1]), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite, None)


def test_right_space_ship_initial_position(test_sprite, mock_image):
    with pytest.raises(ValueError) as e:
        SpaceShip((SpaceShip.MIDDLE_POS-1,0),
                             SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite, None)
    with pytest.raises(ValueError) as e:
        SpaceShip((SpaceShip.MIDDLE_POS,-1),
                             SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite, None)
    with pytest.raises(ValueError) as e:
        SpaceShip((SpaceShip.MIDDLE_POS-1,-1),
                             SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite, None)

    with pytest.raises(ValueError) as e:
        SpaceShip((src.Constants.DESIRED_RESOLUTION[0], 0),
                  SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite, None)
    with pytest.raises(ValueError) as e:
        SpaceShip((SpaceShip.MIDDLE_POS, src.Constants.DESIRED_RESOLUTION[1]),
                  SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite, None)
    with pytest.raises(ValueError) as e:
        SpaceShip(src.Constants.DESIRED_RESOLUTION,
                  SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite, None)


def test_left_space_ship_should_not_move_left(test_sprite, mock_image):
    space_ship = SpaceShip((0,0), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite, None)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event, None)
    space_ship.tick()
    assert all(space_ship.position == [0,0])


def test_right_space_ship_should_not_move_left(test_sprite, mock_image):
    space_ship = SpaceShip((SpaceShip.MIDDLE_POS, 0), SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite, None)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event, None)
    space_ship.tick()
    assert all(space_ship.position == [SpaceShip.MIDDLE_POS,0])


def test_left_space_ship_should_not_move_right(test_sprite, mock_image):
    pos = (SpaceShip.MIDDLE_POS - test_sprite.get_size()[0], 0)
    space_ship = SpaceShip(pos, SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite, None)
    move_right_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (1, 0)})
    space_ship.process_input(move_right_event, None)
    space_ship.tick()
    assert all(space_ship.position == pos)


def test_right_space_ship_should_not_move_right(test_sprite, mock_image):
    pos = (src.Constants.DESIRED_RESOLUTION[0] - test_sprite.get_size()[0], 0)
    space_ship = SpaceShip(pos, SpaceShip.SPACE_SHIP_IS_RIGHT, test_sprite, None)
    move_right_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (1, 0)})
    space_ship.process_input(move_right_event, None)
    space_ship.tick()
    assert all(space_ship.position == pos)


def test_left_space_ship_should_move_left(test_sprite, mock_inertia, mock_image):
    space_ship = SpaceShip((SpaceShip.DEFAULT_VELOCITY,0), SpaceShip.SPACE_SHIP_IS_LEFT, test_sprite, None)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event, None)
    space_ship.tick()
    assert all(space_ship.position == [0,0])


def test_right_space_ship_should_move_left(test_sprite, mock_inertia, mock_image):
    space_ship = SpaceShip(
        (SpaceShip.MIDDLE_POS+SpaceShip.DEFAULT_VELOCITY,0),
        SpaceShip.SPACE_SHIP_IS_RIGHT,
        test_sprite, None)
    move_left_event = pygame.event.Event(pygame.JOYHATMOTION, {'joy': 0, 'hat': 0, 'value': (-1, 0)})
    space_ship.process_input(move_left_event, None)
    space_ship.tick()
    assert all(space_ship.position == [SpaceShip.MIDDLE_POS,0])


def test_health_percentage_till_death(test_sprite, mock_image):
    space_ship = SpaceShip(
        (SpaceShip.MIDDLE_POS + SpaceShip.DEFAULT_VELOCITY, 0),
        SpaceShip.SPACE_SHIP_IS_RIGHT,
        test_sprite, None)
    assert space_ship.health_percentage == 100

    assert space_ship.damage_ship(health_percentage_diff=50) is False
    assert space_ship.health_percentage == 50

    assert space_ship.damage_ship(health_percentage_diff=80) is True
    assert space_ship.health_percentage == 0


def test_health_increase(test_sprite, mock_image):
    space_ship = SpaceShip(
        (SpaceShip.MIDDLE_POS + SpaceShip.DEFAULT_VELOCITY, 0),
        SpaceShip.SPACE_SHIP_IS_RIGHT,
        test_sprite, None)
    space_ship.health_percentage = 50

    space_ship.increase_health_percentage(health_percentage_diff=90)
    assert space_ship.health_percentage == 100
