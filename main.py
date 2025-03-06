from game import new_game
from leaderboard import leaderboard
from questions import practice_quiz
from tutorial import tutorial
from game_setup import game_setup, colors
from colorama import Style


if __name__ == "__main__":

    
    while True: # infinite loop that breaks when valid input is given
        try:
            user_input = int(input(colors["location"] + "\nM A I N   M E N U\n\n"+ colors["input"] +  "Choose from following options:\n    1 - Open tutorial\n    2 - Start a new game\n    3 - Open leaderboard\n    4 - Practice quiz questions\n    0 - Quit game\nInput: " + Style.RESET_ALL))
            if user_input in range(5):
                break
            else:
                print(colors["warning"] + "Invalid input, try again." + Style.RESET_ALL)
        except ValueError:
            print(colors["warning"] + "Invalid input, try again." + Style.RESET_ALL)



    while user_input != 0:
    
        if user_input == 1 : # Tutorial
            print(colors["location"] + "\nT U T O R I A L\n\n"+ Style.RESET_ALL)
            tutorial()
    
        elif user_input == 2: # New game
            print(colors["location"] + "\nN E W   G A M E\n\n"+ Style.RESET_ALL)
            new_game(game_setup())
    
        elif user_input == 3: # Leaderboard
            print(colors["location"] + "\nL E A D E R B O A R D\n\n"+ Style.RESET_ALL)
            leaderboard()

    
        elif user_input == 4: # Quiz practice
            print(colors["location"] + "\nQ U I Z   P R A C T I C E\n\n"+ Style.RESET_ALL)
            practice_quiz()
    

        
        while True: # infinite loop that breaks when valid input is given
            try:
                user_input = int(input(colors["location"] + "\nM A I N   M E N U\n\n"+ colors["input"] +  "Choose from following options:\n    1 - Open tutorial\n    2 - Start a new game\n    3 - Open leaderboard\n    4 - Practice quiz questions\n    0 - Quit game\nInput: " + Style.RESET_ALL))
                if user_input in range(5):
                    break
                else:
                    print(colors["warning"] + "Invalid input, try again." + Style.RESET_ALL)
            except ValueError:
                print(colors["warning"] + "Invalid input, try again." + Style.RESET_ALL)
                
    print(colors["location"] + "\nQ U I T   G A M E\n\n"+ Style.RESET_ALL)