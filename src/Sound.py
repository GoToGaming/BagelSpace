import os
import time
import pygame
from pygame import mixer

sound_folder_path = os.path.join(os.path.dirname(os.getcwd()), 'sounds')


mixer.init()

machine_gun_shot = mixer.Sound(os.path.join(sound_folder_path, 'machinegun-single-shot-9db.wav'))


menu_music_is_playing = False


def start_menu_background_music():
    global menu_music_is_playing
    if not menu_music_is_playing:
        file = 'Incoming_Transition.mp3'
        mixer.music.stop()
        mixer.music.load(os.path.join(sound_folder_path, "background", file))
        mixer.music.play()
        menu_music_is_playing = True


def start_game_background_music():
    global menu_music_is_playing
    file = 'Ether_Oar.mp3'
    mixer.music.stop()
    mixer.music.load(os.path.join(sound_folder_path, "background", file))
    mixer.music.play()
    if not menu_music_is_playing:
        menu_music_is_playing = False



