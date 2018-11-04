import pygame
import pygameMenu
from pygameMenu.locals import *
import sys

from src import Constants, SpaceBagels


class GameMenu:
    def __init__(self, screen, sound, clock):
        self._screen = screen
        self._sound = sound
        if pygame.joystick.get_count() < 2:
            self.use_joystick = False
        else:
            self.use_joystick = True
        self.game = SpaceBagels.SpaceBagels(self._screen, clock, self._sound)
        self.game._set_input_method(self.use_joystick)

        def _main_menu_callback():
            self._screen.fill((40, 0, 40))

        def _resume_callback():
            self.menu.disable()
            self.game.main()
            self.game._set_input_method(self.use_joystick)

        def _new_game_callback():
            self.menu.disable()
            self.game = SpaceBagels.SpaceBagels(self._screen, clock, self._sound)
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

        def _select_difficulty(method):
            if method == 'Easy':
                Constants.TARGET_FPS = 30
            elif method == 'Medium':
                Constants.TARGET_FPS = 60
            elif method == 'Hard':
                Constants.TARGET_FPS = 90
            elif method == 'Insane':
                Constants.TARGET_FPS = 120
            else:
                raise ValueError
            Constants.TARGET_FRAMETIME_MS = 1000. / Constants.TARGET_FPS

        difficulty_options = [('Medium', 'Medium'), ('Hard', 'Hard'), ('Insane', 'Insane'), ('Easy', 'Easy')]
        settings_menu.add_selector('Difficulty',
                                   difficulty_options,
                                   onreturn=None,
                                   onchange=_select_difficulty)

        def _select_input_method(method):
            if method == 'Keyboard':
                self.use_joystick = False
            elif method == 'Joystick':
                self.use_joystick = True
            else:
                raise ValueError
            self.game._set_input_method(self.use_joystick)

        if pygame.joystick.get_count() < 2:
            input_options = [('Keyboard', 'Keyboard')]
        else:
            input_options = [('Joystick', 'Joystick'), ('Keyboard', 'Keyboard')]
        settings_menu.add_selector('Input',
                                   input_options,
                                   onreturn=None,
                                   onchange=_select_input_method)

        def _select_graphics(method):
            if method == 'Windowed':
                screen = pygame.display.set_mode(Constants.DESIRED_RESOLUTION)
                self = GameMenu(screen, sound, clock)
            elif method == 'Fullscreen':
                screen = pygame.display.set_mode(Constants.DESIRED_RESOLUTION, pygame.FULLSCREEN)
                self = GameMenu(screen, sound, clock)
            else:
                raise ValueError

        graphics_options = [('Windowed', 'Windowed'), ('Fullscreen', 'Fullscreen')]
        settings_menu.add_selector('Graphics',
                                   graphics_options,
                                   onreturn=None,
                                   onchange=_select_graphics)

        self.menu.add_option('New Game', _new_game_callback)
        self.menu.add_option('Settings', settings_menu)
        self.menu.add_option('Exit', PYGAME_MENU_EXIT)

    def process_inputs(self, events):
        self.menu.enable()
        self._sound.start_menu_background_music()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.menu.mainloop(events)
