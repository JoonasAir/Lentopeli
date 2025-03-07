from colorama import Style
from game import new_game
from game_setup import game_setup
from leaderboard import leaderboard
from questions import practice_quiz
from settings import settings, difficulty_settings, common_settings, colors
from tutorial import tutorial



if __name__ == "__main__":

    
    while True: # infinite loop that breaks when valid input is given
        try:
            user_input = int(input(colors["menu"] + "\nM A I N   M E N U\n\n"+ colors["input"] +  "Choose from following options:\n    1 - Open tutorial\n    2 - Start a new game\n    3 - Open leaderboard\n    4 - Practice quiz questions\n    5 - Settings\n    0 - Quit game\nInput: " + Style.RESET_ALL))
            if user_input in range(6):
                break
            else:
                print(colors["warning"] + "Invalid input, try again." + Style.RESET_ALL)
        except ValueError:
            print(colors["warning"] + "Invalid input, try again." + Style.RESET_ALL)

    # join "common settings" -dict to each difficulty's own dict (dictionaries defined in settings.py)
    for difficulty in difficulty_settings:
        difficulty_settings[difficulty].update(common_settings)



    while user_input != 0:
    
        if user_input == 1 : # Tutorial
            print(colors["menu"] + "\nT U T O R I A L\n\n"+ Style.RESET_ALL)
            tutorial()
    
        elif user_input == 2: # New game
            print(colors["menu"] + "\nN E W   G A M E\n\n"+ Style.RESET_ALL)
            game_dict = game_setup(difficulty_settings)
            new_game(game_dict)
    
        elif user_input == 3: # Leaderboard
            print(colors["menu"] + "\nL E A D E R B O A R D\n\n"+ Style.RESET_ALL)
            leaderboard()

    
        elif user_input == 4: # Quiz practice
            print(colors["menu"] + "\nQ U I Z   P R A C T I C E\n\n"+ Style.RESET_ALL)
            practice_quiz()
    

        elif user_input == 5: # Settings
            settings(difficulty_settings, colors)

        
        while True: # infinite loop that breaks when valid input is given
            try:
                user_input = int(input(colors["menu"] + "\nM A I N   M E N U\n\n"+ colors["input"] +  "Choose from following options:\n    1 - Open tutorial\n    2 - Start a new game\n    3 - Open leaderboard\n    4 - Practice quiz questions\n    5 - Settings\n    0 - Quit game\nInput: " + Style.RESET_ALL))
                if user_input in range(6):
                    break
                else:
                    print(colors["warning"] + "Invalid input, try again." + Style.RESET_ALL)
            except ValueError:
                print(colors["warning"] + "Invalid input, try again." + Style.RESET_ALL)
                
    print(colors["menu"] + "\nQ U I T   G A M E\n\n"+ Style.RESET_ALL)