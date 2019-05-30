import pygame

class Speaker:

    def play_sound(self,sound_file):
        song = pygame.mixer.Sound(sound_file)
        song.play()
