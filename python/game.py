import threading
from time import sleep
from mysql_connection import mysql_connection
from tkinter import N
from airport_menu import airport_menu
from background_story import background_story
from criminal import criminal_timer, criminal_caught
from player import print_location
from stop_game import stop_game
from multiprocessing import Process
from questions import ask_category, get_questions


stop_timer = threading.Event()

def game_timer(game_dict:dict, stop_timer:threading.Event):
    while game_dict["game_time"] >= 0:
        if stop_timer.is_set():
            break
        min, sec = divmod(game_dict["game_time"], 60)
        game_dict["time_left_str"] = f"Time remaining: {min:02d}:{sec:02d}"
        sleep(1)
        game_dict["game_time"] -= 1
    game_dict["time_left_str"] = f"Time is running up, you have time to take only one more flight!"
    game_dict["time_left_bool"] = False



def play_game(game_dict:dict):
    # Choosing category of quiz questions
    game_dict["quiz_category"] = ask_category()
    # Get quiz questions with right difficulty and category
    game_dict["quiz_questions"] = get_questions(game_dict["difficulty"], game_dict["quiz_category"])


    # background story of the game (Y/N) = (player can read or skip the story)
    background_story(game_dict["screen_name"])




    # Defining a background process that runs criminal_timer -function
    ProcessCriminalTimer = Process(target=criminal_timer, args=(game_dict['criminal_time'],))
    # Start the process
    ProcessCriminalTimer.start()
    
    game_timer_thread = threading.Thread(target = game_timer, args = (game_dict, stop_timer))
    game_timer_thread.daemon = True
    game_timer_thread.start()


    while True:
        # check if the game should end or not
        if stop_game(game_dict):
            break
        
        # reset airport_menu-helper parameters to default value before entering airport-menu on the new airport
        game_dict['talk_to_chief'] = False
        game_dict['tried_luck'] = False
        game_dict['first_iteration'] = True
        game_dict['next_location_bool'] = False
        game_dict["clue_solved"] = bool
        game_dict['criminal_was_here'] = bool

        # Player is at the airport_menu() -function until a flight ticket is bought
        game_dict = airport_menu(game_dict)

        print_location(game_dict["player_location"])

        if game_dict["first_airport"]:
            game_dict["first_airport"] = False
    

        # if we gave right answer on the question = we are on right airpot now -> criminal-table: change visited to 1 on the first row with visited = 0
        if game_dict['previous_quiz_answer']: # boolean telling us if we got last quiz wrong or right
            cursor = mysql_connection.cursor()
            # sql = "UPDATE criminal SET visited = 1 WHERE visited = 0 LIMIT 1;"
            sql = f"UPDATE criminal SET visited = 1 WHERE id = (SELECT id FROM criminal WHERE visited = 0 LIMIT 1) AND location = '{game_dict['player_location']}';"
            cursor.execute(sql)


        # check at the new airport if we are at the same airport as the criminal is (write function criminal_caught function that retuns True if we are and False if we aren't)
        game_dict["criminal_caught"] = criminal_caught()


    if game_dict["win_game"]: # If we won the game
        leaderboard_update(game_dict)




    # Terminate the criminal_timer -background process
    ProcessCriminalTimer.terminate()
    # Ensures that the main program waits for the terminated process to clean up properly before continuing
    ProcessCriminalTimer.join()

    # end threading
    stop_timer.set()



def point_calculator(game_dict:dict):
    mode = 0
    time = game_dict["game_time"]
    if game_dict["difficulty"] == "easy":
        mode = 1
    if game_dict["difficulty"] == "medium":
        mode = 1.5
    elif game_dict["difficulty"] == "hard":
        mode = 2.5

    score = time * mode * 150
    
    
    return score


def leaderboard_update(game_dict:dict):
    screen_name = game_dict["screen_name"]
    points = point_calculator(game_dict)
    cursor = mysql_connection.cursor()

    sql = f"SELECT screen_name, points FROM leaderboard WHERE screen_name = '{screen_name}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if type(result) == tuple: # screen_name is found in leaderboard
        if result[1] < points: # update points if new personal highscore
            sql = f"UPDATE leaderboard SET points = '{points}' WHERE screen_name = '{screen_name}';"
            cursor.execute(sql)
            print(f"\nYou got a new highscore: {points} \nYour previous highscore: {result[1]}".upper())

        else:
            print(f"\nYour score: {points} \nYou didn't beat your highscore: {result[1]}".upper())
    else: # screen_name is found in leaderboard
        sql = f"INSERT into leaderboard (screen_name, points) values('{screen_name}' ,{points});"
        cursor.execute(sql)
        print(f"\nYour score: {points} ".upper())


# Return to the main menu


if __name__ == "__main__": 
    from game_setup import game_setup
    from game_parameters import game_parameters
    game_dict = game_setup(game_parameters)
    play_game(game_dict)
