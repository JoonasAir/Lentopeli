import time
from colorama import Fore, Back, Style

# VIELÄ KESKEN

def game_timer(t):
    while t > 0:
        min, sec = divmod(t, 60)
        timer = f"{min:02d}:{sec:02d}"
        print(Fore.RED + timer, end = "\r")
        time.sleep(1)
        t -= 1

game_timer(3)       