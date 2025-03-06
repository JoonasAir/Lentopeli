from game import new_game
from questions import practice_quiz
from tutorial import tutorial

if __name__ == "__main__":

    while True:
        try:
            user_input = int(input("\nMAIN MENU\n\nChoose from following options:\n    1 - Open tutorial\n    2 - Start a new game\n    3 - Open leaderboard\n    4 - Practice quiz questions\n    0 - Quit game\nInput: "))
            if user_input in range(5):
                break
            else:
                print("Invalid input, try again.")
        except ValueError:
            print("Invalid input, try again.")



    while user_input != 0:
    
        if user_input == 1 : # Tutorial
            tutorial()
    
        elif user_input == 2: # New game
            new_game()
    
        elif user_input == 3: # Leaderboard
            pass
    
        elif user_input == 4: # Quiz practice
            practice_quiz()
    

        while True:
            try:
                user_input = int(input("\nMAIN MENU\n\nChoose from following options:\n    1 - Open tutorial\n    2 - Start a new game\n    3 - Open leaderboard\n    4 - Practice quiz questions\n    0 - Quit game\nInput: "))
                if user_input in range(5):
                    break
                else:
                    print("Invalid input, try again.")
            except ValueError:
                print("Invalid input, try again.")
        
