from game import play_game
from game_setup import game_setup
from leaderboard import leaderboard
from questions import practice_quiz
from settings import settings
from game_parameters import game_parameters
from tutorial import tutorial
from styles import styles



def main_menu():

    while True: # infinite loop that breaks when valid input is given
        try:
            user_input = int(input(styles["menu"] + "\nM A I N   M E N U\n\n"+ styles["input"] +  "Choose from following options:\n    1 - Open tutorial\n    2 - Start a new game\n    3 - Open leaderboard\n    4 - Practice quiz questions\n    5 - Settings\n    0 - Quit game\nInput: " + styles["reset"]))
            if user_input in range(6):
                break
            else:
                print(styles["warning"] + "Invalid input, try again." + styles["reset"])
        except ValueError:
            print(styles["warning"] + "Invalid input, try again." + styles["reset"])


    while user_input != 0:
    
        if user_input == 1 : # Tutorial
            print(styles["menu"] + "\nT U T O R I A L\n\n"+ styles["reset"])
            tutorial()
    
        elif user_input == 2: # New game
            print(styles["menu"] + "\nN E W   G A M E\n\n"+ styles["reset"])
            game_dict = game_setup(game_parameters)
            play_game(game_dict)
    
        elif user_input == 3: # Leaderboard
            print(styles["menu"] + "\nL E A D E R B O A R D\n\n"+ styles["reset"])
            leaderboard()

    
        elif user_input == 4: # Quiz practice
            print(styles["menu"] + "\nQ U I Z   P R A C T I C E\n\n"+ styles["reset"])
            practice_quiz()
    

        elif user_input == 5: # Settings

            settings(game_parameters["C"], styles)

        
        while True: # infinite loop that breaks when valid input is given
            try:
                user_input = int(input(styles["menu"] + "\nM A I N   M E N U\n\n"+ styles["input"] +  "Choose from following options:\n    1 - Open tutorial\n    2 - Start a new game\n    3 - Open leaderboard\n    4 - Practice quiz questions\n    5 - Settings\n    0 - Quit game\nInput: " + styles["reset"]))
                if user_input in range(6):
                    break
                else:
                    print(styles["warning"] + "Invalid input, try again." + styles["reset"])
            except ValueError:
                print(styles["warning"] + "Invalid input, try again." + styles["reset"])
                
    print(styles["menu"] + "\nQ U I T   G A M E\n\n"+ styles["reset"])