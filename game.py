import threading
import time
from mysql_connection import mysql_connection
from tkinter import N
from airport_menu import airport_menu
from background_story import background_story
from criminal import criminal_timer, criminal_caught
from player import print_location
from stop_game import stop_game
from styles import styles
import multiprocessing
from questions import ask_category, get_questions


stop_timer = threading.Event()

def game_timer(game_dict:dict, stop_timer:threading.Event):
    #global game_dict
    while game_dict["game_time"] >= 0:
        if stop_timer.is_set():
            break
        min, sec = divmod(game_dict["game_time"], 60)
        game_dict["time_left_str"] = styles["time"] + f"Time remaining: {min:02d}:{sec:02d}" + styles["reset"]
        time.sleep(1)
        game_dict["game_time"] -= 1
    game_dict["time_left_str"] = styles["warning"] + f"Time is running up, you have time to take only one more flight!" + styles["reset"]
    game_dict["time_left_bool"] = False
#   pelin koodi



def new_game(game_dict:dict):
    # Choosing category of quiz questions
    game_dict["quiz_category"] = ask_category()
    # Get quiz questions with right difficulty and category
    game_dict["quiz_questions"] = get_questions(game_dict["difficulty"], game_dict["quiz_category"])


    # background story of the game (Y/N) = (player can read or skip the story)
    background_story(game_dict["screen_name"])



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
    
    game_timer_thread = threading.Thread(target = game_timer, args = (game_dict, stop_timer))
    game_timer_thread.daemon = True
    game_timer_thread.start()


    while True:

        if stop_game(game_dict):
            break
        
        
        # Player is at the airport_menu() -function until a flight ticket is bought
        game_dict = airport_menu(game_dict)

        print_location(game_dict["player_location"])

        if game_dict["first_airport"]:
            game_dict["first_airport"] = False
        

    
        # check at the new airport if we are at the same airport as the criminal is (write function criminal_caught function that retuns True if we are and False if we aren't)
        game_dict["criminal_caught"] = criminal_caught()


        # if we gave right answer on the question = we are on right airpot now -> criminal-table: change visited to 1 on the first row with visited = 0
        if game_dict['previous_quiz_answer']: # boolean telling us if we got last quiz wrong or right
            cursor = mysql_connection.cursor()
            # sql = "UPDATE criminal SET visited = 1 WHERE visited = 0 LIMIT 1;"
            sql = f"UPDATE criminal SET visited = 1 WHERE id = (SELECT id FROM criminal WHERE visited = 0 LIMIT 1) AND location = '{game_dict["player_location"]}';"
            cursor.execute(sql)



        # reset airport_menu-helper parameters to default value before entering airport-menu on the new airport
        game_dict['talk_to_chief'] = False
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
    stop_timer.set()



# TODO When the game ends:
#   1. Scores are calculated

def point_calculator(game_dict):
    mode = 0
    time = game_dict["game_time"]
    if game_dict["difficulty"] == "easy":
        mode = 1
    if game_dict["difficulty"] == "medium":
        mode = 1.5
    elif game_dict["difficulty"] == "hard":
        mode = 2.5

    score = time * mode
    print(score)
    
    return score


#   2. The game statistics are printed (screen name, how many games played with this screen name, difficulty level, score, elapsed time, money at the start, money spent, number of flights, number of off-course flights)

#   3. Save game stats to the leaderboard table
def leaderboard_update():
    screen_name = game_dict["screen_name"]
    points = point_calculator()
    cursor = mysql_connection.cursor()
    sql = f"INSERT into leaderboard (screen_name, points) values({screen_name} ,{points})"
    cursor.execute(sql)

# Return to the main menu








if __name__ == "__main__": 
    from game_setup import game_setup
    from game_parameters import game_parameters
    game_dict = game_setup(game_parameters)
    new_game(game_dict)
