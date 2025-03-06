import time
import threading
from colorama import Fore, Back, Style
from game_setup import game_setup

# NÄILLÄ KÄYNNISTETÄÄN LASKURIN THREADING
# game_timer_thread = threading.Thread(target = game_timer.game_timer, args = (game_dict["game_time"], game_timer.stop_event))
# game_timer_thread.start()

# TÄLLÄ LOPETETAAN LASKURI
# game_timer.stop_event.set()

stop_event = threading.Event()

def game_timer(game_timeremaining, stop_event):
    global game_dict
    while game_timeremaining > 0:
        if stop_event.is_set():
            break
        min, sec = divmod(game_timeremaining, 60)
        game_dict["running_time"] = Fore.RED + f"Time remaining: {min:02d}:{sec:02d}" + Style.RESET_ALL
        #print(Fore.RED + timer, end = "\r")
        time.sleep(1)
        game_timeremaining -= 1
    game_dict["time_left_bool"] = False

if __name__ == "__main__": 
    game_dict = game_setup()
    game_timer_thread = threading.Thread(target = game_timer, args = (game_dict["game_time"], stop_event))
    game_timer_thread.start()
    print(game_dict["running_time"])
    time.sleep(5)
    print(game_dict["running_time"])
    stop_event.set()