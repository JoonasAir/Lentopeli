def game_setup():
    # parameters for each difficulty
    difficulty_settings = {
        'E': { # Easy
            'game_money': 5000,         # money at the beginning of the game
            'game_time': 60*5,          # money at the beginning of the game
            'mistakes_allowed': 3,      # allowed amount of mistakes during a game
            'random_luck': 0.05,        # the possibility of benefiting from random functions
            'criminal_headstart': 2,    # the criminal's head start at the start of the game
            'criminal_time': 60,        # the time interval at which the criminal flies to the next location
            'difficulty': 'Easy'        # difficulty for quiz questions
        },
        'N': { # Normal
            'game_money': 3500,         # money at the beginning of the game
            'game_time': 60*4,          # time at the beginning of the game
            'mistakes_allowed': 2,      # allowed amount of mistakes during a game
            'random_luck': 0.025,       # the possibility of benefiting from random functions
            'criminal_headstart': 3,    # the criminal's head start at the start of the game
            'criminal_time': 45,        # the time interval at which the criminal flies to the next location
            'difficulty': 'Normal'      # difficulty for quiz questions
        },
        'H': { # Hard
            'game_money': 2500,         # money at the beginning of the game
            'game_time': 60*3,          # money at the beginning of the game
            'mistakes_allowed': 0,      # allowed amount of mistakes during a game
            'random_luck': 0.01,        # the possibility of benefiting from random functions
            'criminal_headstart': 4,    # the criminal's head start at the start of the game
            'criminal_time': 30,        # the time interval at which the criminal flies to the next location
            'difficulty': 'Hard'        # difficulty for quiz questions
        },
        'X': { # For testing purposes. Feel free to adjust during testing. This will be removed from actual game.
            'game_money': 5000,         # money at the beginning of the game
            'game_time': 60*5,          # money at the beginning of the game
            'mistakes_allowed': 3,      # allowed amount of mistakes during a game
            'random_luck': 0.05,        # the possibility of benefiting from random functions
            'criminal_headstart': 4,    # the criminal's head start at the start of the game
            'criminal_time': 3,         # the time interval at which the criminal flies to the next location
            'difficulty': 'Easy'        # difficulty for quiz questions
        }
    }

    screen_name = str(input("Enter your game name: ")) 

    state = True # user will be asked for a difficulty until one of the defined inputs is given
    while state:
        difficulty_input = str(input("Choose difficulty of the game: 'E' = Easy, 'N' = Normal, 'H' = Hard: "))

        if difficulty_input.upper() in difficulty_settings:
            game_parameters = difficulty_settings[difficulty_input.upper()] # stores the parameters ​​of the difficulty selected by the user 
            state = False
        else:
            print("You entered an invalid input.")

    game_parameters["screen_name"] = screen_name # adding player's name to dictionary
    
    return game_parameters # return dictionary with parameters and screen name



# Main block for testing
if __name__ == "__main__":
    game_parameters = game_setup()
    print(game_parameters)
    print(game_parameters["game_money"])
    print(game_parameters["screen_name"])