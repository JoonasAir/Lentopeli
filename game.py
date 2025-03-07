import threading
import time
from colorama import Style
from airport_menu import airport_menu
from background_story import background_story
from criminal import criminal_timer
from settings import colors
import multiprocessing
from questions import ask_category, get_questions


stop_event = threading.Event()

def game_timer(game_timeremaining, stop_event, game_dict):
    #global game_dict
    while game_timeremaining > 0:
        if stop_event.is_set():
            break
        min, sec = divmod(game_timeremaining, 60)
        game_dict["time_left_str"] = colors["time"] + f"Time remaining: {min:02d}:{sec:02d}" + Style.RESET_ALL
        time.sleep(1)
        game_timeremaining -= 1
    game_dict["time_left_bool"] = False


def new_game(game_dict):
    # Choosing category of quiz questions
    game_dict["quiz_category"] = ask_category()
    # Get quiz questions with right difficulty and category
    game_dict["quiz_questions"] = get_questions(game_dict["difficulty"], game_dict["quiz_category"])



    # background story of the game (Y/N) = (player can read or skip the story)
    background_story()


    #   Game starts

    # Defining and starting a background process for criminal_timer function
    # Using Manager to share state between processes (when we change criminal_timer_state to False in the main program, the loop in the background process will close)
    manager = multiprocessing.Manager()
    # Boolean value for the function loop. We have to use manager because we need this variable in both processes
    criminal_timer_state = manager.Value('b', True)
    # Define the process
    ProcessCriminalTimer = multiprocessing.Process(target=criminal_timer, args=(criminal_timer_state, game_dict['criminal_time']))
    # Start the process
    ProcessCriminalTimer.start()
    
    game_timer_thread = threading.Thread(target = game_timer, args = (game_dict["game_time"], stop_event, game_dict))
    game_timer_thread.daemon = True
    game_timer_thread.start()


    while not game_dict["criminal_caught"] and game_dict["game_money"] >= game_dict["flight_price"] and game_dict["time_left_bool"]:

        #TODO print country and airpot
        print(colors["location"] + f"\n\nYou're at: {game_dict["player_location"]}" + Style.RESET_ALL)
        
        
        # Player is at the airport_action() -function until the location changes
        game_dict = airport_menu(game_dict)

        if game_dict["first_airport"]:
            game_dict["first_airport"] = False
        


        # TODO check at the new airport if we are at the same airport as the criminal is (write function criminal_caught function that retuns True if we are and False if we aren't)
        #game_dict["criminal_caught"] = criminal_caught()


        # TODO if we gave right answer on the question = we are on right airpot now -> criminal-table: change visited to 1 on the first row with visited = 0
        if game_dict['previous_quiz_answer']: # boolean telling us if we got last quiz wrong or right
            pass #SQL here



        # reset airport_menu-helper parameters to default value before entering airport-menu on the new airport
        game_dict['talk_to_chief'] = False
        game_dict['criminal_caught'] = False
        game_dict['tried_luck'] = False
        game_dict['first_iteration'] = True
        game_dict['next_location'] = ""
        game_dict["clue_solved"] = bool
        game_dict['criminal_was_here'] = bool





    # Ending the loop running in the background process
    criminal_timer_state.value = False
    # Force the termination of the background process, as the process loop contains a sleep function 
    # (otherwise the player would have to wait until the criminal flies to the next airport)
    ProcessCriminalTimer.terminate()
    # Ensure the background process has ended before moving on
    ProcessCriminalTimer.join()
    stop_event.set()



# When the game ends:
#   1. Scores are calculated
#   2. The game statistics are printed (screen name, how many games played with this screen name, difficulty level, score, elapsed time, money at the start, money spent, number of flights, number of off-course flights)
#   3. Save game stats to the leaderboard table

# Return to the main menu








if __name__ == "__main__": 
    from game_setup import game_setup    
    # screen_name, starting location, and many other parameters are returned as a dictionary. Also criminal's headstart is added to database 
    game_dict = game_setup() # check the keys from game_setup.py's difficulty_settings -dictionary
    new_game(game_dict)
