from game import new_game

if __name__ == "__main__":

    user_input = int(input("\nMAIN MENU\n\nChoose from following options:\n    1 - Open tutorial\n    2 - Start a new game\n    3 - Open leaderboard\n    4 - Practice quiz questions\n    0 - Quit game\nInput: "))

    while user_input != 0:
    
        if user_input == 1 : # Tutorial
            pass
    
        elif user_input == 2: # New game
            new_game()
    
        elif user_input == 3: # Leaderboard
            pass
    
        elif user_input == 4: # Quiz practice
            pass
    

        user_input = int(input("\nMAIN MENU\n\nChoose from following options:\n    1 - Open tutorial\n    2 - Start a new game\n    3 - Open leaderboard\n    4 - Practice quiz questions\n    0 - Quit game\nInput: "))
        
