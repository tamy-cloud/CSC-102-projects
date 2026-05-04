###########################################################################################
# Name: Dr. Jean Gourd
# Date: 2022-02-08
# Description: An example of how to play audio files (mp3) in Python using the PyGame
#              library.
###########################################################################################

# import libraries
import pygame
from time import sleep

# initialize pygame
pygame.init()

# load an audio file (mp3)
pygame.mixer.music.load("library.mp3")
# play the audio (-1 plays the audio forever; 1 plays the audio once, etc)
print("Playing library.mp3 forever...")
pygame.mixer.music.play(-1)

# do something for some amount of time
print("Sleeping 5s...")
# time's sleep() allows Ctrl+C to be detected immediately
sleep(5)

# fade out the audio (in 1.5s) if it's playing
if (pygame.mixer.music.get_busy()):
    print("Audio is playing; fading out...")
    pygame.mixer.music.fadeout(1500)

# load a new audio file (mp3)
pygame.mixer.music.load("treasure.mp3")
# play the audio (-1 plays the audio forever; 1 plays the audio once, etc)
print("Playing treasure.mp3 once...")
pygame.mixer.music.play(1)

# instead of sleeping, pygame can be used to wait for some time (5s)
print("Waiting 8s...")
# pygame's time.wait() must finish before Ctrl+C is detected
pygame.time.wait(8000)


