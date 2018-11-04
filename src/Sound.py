import os
from pygame import mixer

sound_folder_path = os.path.join(os.path.dirname(__file__), '..', 'sounds')


class Sound:
    def __init__(self):
        self.menu_music_is_playing = False

        mixer.init()
        mixer.set_num_channels(20)
        self.machine_gun_shot = mixer.Sound(os.path.join(sound_folder_path, 'machinegun-single-shot-9db.wav'))
        self.missile_shot = mixer.Sound(os.path.join(sound_folder_path, 'missile-shot.wav'))
        self.heal = mixer.Sound(os.path.join(sound_folder_path, 'heal.wav'))
        self.scrape_asteroid = mixer.Sound(os.path.join(sound_folder_path, 'scrape-asteroid-short.wav'))

    def start_menu_background_music(self):
        if not self.menu_music_is_playing:
            print('menu sound set')
            file = 'Incoming_Transition.mp3'
            mixer.music.stop()
            mixer.music.load(os.path.join(sound_folder_path, "background", file))
            mixer.music.play(loops=100)
            self.menu_music_is_playing = True

    def start_game_background_music(self):
        if self.menu_music_is_playing:
            self.menu_music_is_playing = False
        file = 'Ether_Oar.mp3'
        mixer.music.stop()
        mixer.music.load(os.path.join(sound_folder_path, "background", file))
        mixer.music.play(loops=100)

    def play_machine_gun_shot(self):
        self.machine_gun_shot.play()

    def play_missile_shot(self):
        self.missile_shot.play()

    def play_heal(self):
        self.heal.play()

    def play_scrape_asteroid(self):
        self.scrape_asteroid.play()
