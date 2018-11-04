import os
import time
import pygame
from pygame import mixer

sound_folder_path = os.path.join(os.path.dirname(os.getcwd()), 'sounds')

file = 'After_All.mp3'
mixer.init()

machine_gun_shot = mixer.Sound(os.path.join(sound_folder_path, 'machine-gun-double-shot.wav'))



# mixer.music cna only play one stream at a time so it is probably right for background music
# mixer.music.load(os.path.join(sound_folder_path, "background", file))
# mixer.music.play()