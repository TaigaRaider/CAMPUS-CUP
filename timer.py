import time
from rich.progress import track
import pygame
import sys


def run_timer(run_time):
    pygame.mixer.init()
    pygame.mixer.music.load(sys.argv[1])
    pygame.mixer.music.play()
    for i in track(range(run_time), description="Waiting..."):
        time.sleep(1)
    print("The Wait is Over")


run_timer(5)
