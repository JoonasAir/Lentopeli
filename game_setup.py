from mysql_connection import mysql_connection

# game_setup() funktiossa käyttäjä valitsee pelin vaikeusasteen, pelinimen, sekä pelaajalle arvotaan aloituslentokenttä
# tiedot palautetaan sanakirjana

def game_setup():
    # parameters for each difficulty
    difficulty_settings = {
        'E': { # Easy
            'game_money': 5000,         # money at the beginning of the game
            'game_time': 60*5,          # time at the beginning of the game
            'random_luck': 0.05,        # the possibility of benefiting from random functions
            'criminal_headstart': 2,    # the criminal's head start at the start of the game
            'criminal_time': 60,        # the time interval at which the criminal flies to the next location
            'difficulty': 'easy'        # difficulty for quiz questions
        },
        'N': { # Normal
            'game_money': 3500,         # money at the beginning of the game
            'game_time': 60*4,          # time at the beginning of the game
            'random_luck': 0.025,       # the possibility of benefiting from random functions
            'criminal_headstart': 3,    # the criminal's head start at the start of the game
            'criminal_time': 45,        # the time interval at which the criminal flies to the next location
            'difficulty': 'medium'      # difficulty for quiz questions
        },
        'H': { # Hard
            'game_money': 2500,         # money at the beginning of the game
            'game_time': 60*3,          # time at the beginning of the game
            'random_luck': 0.01,        # the possibility of benefiting from random functions
            'criminal_headstart': 4,    # the criminal's head start at the start of the game
            'criminal_time': 30,        # the time interval at which the criminal flies to the next location
            'difficulty': 'hard'        # difficulty for quiz questions
        },
        'X': { # For testing purposes. Feel free to adjust during testing. This will be removed from actual game.
            'game_money': 5000,         # money at the beginning of the game
            'game_time': 60*5,          # time at the beginning of the game
            'random_luck': 0.05,        # the possibility of benefiting from random functions
            'criminal_headstart': 4,    # the criminal's head start at the start of the game
            'criminal_time': 3,         # the time interval at which the criminal flies to the next location
            'difficulty': 'easy'        # difficulty for quiz questions
        }
    }

    # Screen_name input
    screen_name = str(input("Enter your game name: ")) 

    # Starting location
    sql = "SELECT ident FROM airport WHERE continent = 'EU' AND type = 'large_airport' AND ident NOT IN (SELECT location FROM criminal) ORDER BY RAND() LIMIT 1;"
    cursor = mysql_connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchone()

    # Get parameters for game from difficulty_settings dictionary
    # user will be asked for a difficulty until valid inputs is given
    while True:
        difficulty_input = str(input("Choose difficulty of the game: 'E' = Easy, 'N' = Normal, 'H' = Hard: "))

        if difficulty_input.upper() in difficulty_settings:
            game_parameters = difficulty_settings[difficulty_input.upper()] # stores the parameters ​​of the difficulty selected by the user 
            break # break out from loop when valid input is given
        else:
            print("You entered an invalid input.")


    # Add screen_name and starting location to dictionary that is returned after
    game_parameters["screen_name"] = screen_name # adding player's name to dictionary
    game_parameters["player_location"] = result["ident"]
    
    return game_parameters # return dictionary with parameters and screen name



# Main block for testing
if __name__ == "__main__":
    game_parameters = game_setup()
    print(game_parameters)
    print(f"You have {game_parameters["game_money"]}€ in your bank account. ")
    print(f"Screen name: {game_parameters["screen_name"]}")
    print(f"You're at an airport with ICAO code: {game_parameters["player_location"]}")