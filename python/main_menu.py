from game import play_game
from game_setup import game_setup
#from leaderboard import leaderboard
from questions import practice_quiz
from game_parameters import game_parameters
from tutorial import tutorial



def main_menu():

    while True: # infinite loop that breaks when valid input is given
        try:
            user_input = int(input("\nM A I N   M E N U\n\n"+  "Choose from following options:\n    1 - Open tutorial\n    2 - Start a new game\n    3 - Open leaderboard\n    4 - Practice quiz questions\n    0 - Quit game\nInput: "))
            if user_input in range(5):
                break
            else:
                print("Invalid input, try again.")
        except ValueError:
            print("Invalid input, try again.")


    while user_input != 0:
    
        if user_input == 1 : # Tutorial
            print("\nT U T O R I A L\n\n")
            tutorial()
    
        elif user_input == 2: # New game
            print("\nN E W   G A M E\n\n")
            game_dict = game_setup(game_parameters)
            play_game(game_dict)
    
        elif user_input == 3: # Leaderboard
            print("\nL E A D E R B O A R D\n\n")
            # leaderboard()

    
        elif user_input == 4: # Quiz practice
            print("\nQ U I Z   P R A C T I C E\n\n")
            practice_quiz()
                
    print("\nQ U I T   G A M E\n\n")