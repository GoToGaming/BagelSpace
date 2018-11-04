import pygame
import pygameMenu
from pygameMenu.locals import *
import sys

from src import Constants, SpaceBagels
import src.Sound as sound


class GameMenu:
    def __init__(self, screen, clock):
        self._screen = screen
        if pygame.joystick.get_count() < 2:
            self.use_joystick = False
        else:
            self.use_joystick = True
        self.game = SpaceBagels.SpaceBagels(self._screen, clock)
        self.game._set_input_method(self.use_joystick)

        def _main_menu_callback():
            self._screen.fill((40, 0, 40))

        def _resume_callback():
            self.menu.disable()
            self.game.main()
            self.game._set_input_method(self.use_joystick)

        def _new_game_callback():
            self.menu.disable()
            self.game = SpaceBagels.SpaceBagels(self._screen, clock)
            self.game._set_input_method(self.use_joystick)
            self.game.main()

        self.menu = pygameMenu.Menu(self._screen,
                                    bgfun=_main_menu_callback,
                                    enabled=True,
                                    font=pygameMenu.fonts.FONT_8BIT,
                                    menu_alpha=90,
                                    onclose=_resume_callback,
                                    title='SpaceBagels',
                                    menu_width=Constants.MENU_WIDTH,
                                    menu_height=Constants.MENU_HEIGHT,
                                    window_width=Constants.DESIRED_RESOLUTION[0],
                                    window_height=Constants.DESIRED_RESOLUTION[1])

        settings_menu = pygameMenu.Menu(self._screen,
                                        bgfun=_main_menu_callback,
                                        font=pygameMenu.fonts.FONT_8BIT,
                                        menu_alpha=90,
                                        onclose=PYGAME_MENU_BACK,
                                        title='Settings',
                                        menu_width=Constants.MENU_WIDTH,
                                        menu_height=Constants.MENU_HEIGHT,
                                        window_width=Constants.DESIRED_RESOLUTION[0],
                                        window_height=Constants.DESIRED_RESOLUTION[1])

        def _select_input_method(method):
            if method == 'Keyboard':
                self.use_joystick = False
            elif method == 'Joystick':
                self.use_joystick = True
            else:
                raise ValueError
            self.game._set_input_method(self.use_joystick)

        if pygame.joystick.get_count() < 2:
            options = [('Keyboard', 'Keyboard')]
        else:
            options = [('Joystick', 'Joystick'), ('Keyboard', 'Keyboard')]
        settings_menu.add_selector('Input',
                                   options,
                                   onreturn=None,
                                   onchange=_select_input_method)

        self.menu.add_option('New Game', _new_game_callback)
        self.menu.add_option('Settings', settings_menu)
        self.menu.add_option('Exit', PYGAME_MENU_EXIT)

    def process_inputs(self, events):
        sound.start_menu_background_music()
        self.menu.enable()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.menu.mainloop(events)
