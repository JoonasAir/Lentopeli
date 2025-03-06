from criminal import criminal_headstart
from mysql_connection import mysql_connection


# game_setup() funktiossa käyttäjä valitsee pelin vaikeusasteen, pelinimen, sekä pelaajalle arvotaan aloituslentokenttä
# tiedot palautetaan sanakirjana

def game_setup():
    # parameters for each difficulty
    difficulty_settings = {
        'E': { # Easy
            'game_money': 5000,         # money at the beginning of the game
            'game_time': 60*10,         # time at the beginning of the game
            'eco_points': 100,          # eco points at the beginning of the game
            'flight_price':200,         # price of a flight ticket          
            'random_luck': 0.10,        # the possibility of benefiting from random functions
            'player_location':str,      # player's current location (ICAO)
            'screen_name':str,          # player's screen name
            'criminal_headstart': 2,    # the criminal's head start at the start of the game
            'criminal_time': 60,        # the time interval at which the criminal flies to the next location
            'difficulty': 'easy',       # difficulty for quiz questions
            'quiz_questions':list,      # questions of player's difficulty and category
            'previous_question':dict,   # previously asked question in case of player have to solve it again
            'clue_solved':bool,         # have we solved a clue at current airport?
            'tried_luck':False,         # have we tried our luck at this airport yet?
            'talk_to_chief': False,     # have we talked to security chief at current airport or not? True=yes, False=no
            'previous_quiz_answer':bool,# did we answer right or wrong on previous quiz question? True=right, False=wrong
            'next_location': "",        # have we solved a clue at current airport or got the next location otherwise? True=yes, False=no
            'criminal_was_here':bool,   # security chief tells us if the criminal has been at the air port or not. True=has been, False=has not been
            'criminal_caught':False,    # have we caught the criminal yet? True=yes, False=no
            'win':bool,                 # when conditions meet to end the game, this is turned to True if we won and False if we lost the game
            'first_airport':True        # are we at our first airport?
        },
        'M': { # Medium
            'game_money': 4000,         # money at the beginning of the game
            'game_time': 60*7,          # time at the beginning of the game
            'eco_points': 100,          # eco points at the beginning of the game
            'flight_price':200,         # price of a flight ticket          
            'random_luck': 0.05,        # the possibility of benefiting from random functions
            'player_location':str,      # player's current location (ICAO)
            'screen_name':str,          # player's screen name
            'criminal_headstart': 3,    # the criminal's head start at the start of the game
            'criminal_time': 45,        # the time interval at which the criminal flies to the next location
            'difficulty': 'medium',     # difficulty for quiz questions
            'quiz_questions':list,      # questions of player's difficulty and category
            'previous_question':dict,   # previously asked question in case of player have to solve it again
            'clue_solved':bool,         # have we solved a clue at current airport?
            'tried_luck':False,         # have we tried our luck at this airport yet?
            'talk_to_chief': False,     # have we talked to security chief at current airport or not? True=yes, False=no
            'previous_quiz_answer':bool,# did we answer right or wrong on previous quiz question? True=right, False=wrong
            'next_location': "",        # have we solved a clue at current airport or got the next location otherwise? True=yes, False=no
            'criminal_was_here':bool,   # security chief tells us if the criminal has been at the air port or not. True=has been, False=has not been
            'criminal_caught':False,    # have we caught the criminal yet? True=yes, False=no
            'win':bool,                 # when conditions meet to end the game, this is turned to True if we won and False if we lost the game
            'first_airport':True        # are we at our first airport?
        },
        'H': { # Hard
            'game_money': 3000,         # money at the beginning of the game
            'game_time': 60*5,          # time at the beginning of the game
            'eco_points': 100,          # eco points at the beginning of the game
            'flight_price':200,         # price of a flight ticket          
            'random_luck': 0.025,       # the possibility of benefiting from random functions
            'player_location':str,      # player's current location (ICAO)
            'screen_name':str,          # player's screen name
            'criminal_headstart': 4,    # the criminal's head start at the start of the game
            'criminal_time': 30,        # the time interval at which the criminal flies to the next location
            'difficulty': 'hard',       # difficulty for quiz questions
            'quiz_questions':list,      # questions of player's difficulty and category
            'previous_question':dict,   # previously asked question in case of player have to solve it again
            'clue_solved':bool,         # have we solved a clue at current airport?
            'tried_luck':False,         # have we tried our luck at this airport yet?
            'talk_to_chief': False,     # have we talked to security chief at current airport or not? True=yes, False=no
            'previous_quiz_answer':bool,# did we answer right or wrong on previous quiz question? True=right, False=wrong
            'next_location': "",        # have we solved a clue at current airport or got the next location otherwise? True=yes, False=no
            'criminal_was_here':bool,   # security chief tells us if the criminal has been at the air port or not. True=has been, False=has not been
            'criminal_caught':False,    # have we caught the criminal yet? True=yes, False=no
            'win':bool,                 # when conditions meet to end the game, this is turned to True if we won and False if we lost the game
            'first_airport':True        # are we at our first airport?
        },
        'X': { # For testing purposes. Feel free to adjust during testing. This will be removed from the actual game.
            'game_money': 5000,         # money at the beginning of the game
            'game_time': 60*5,          # time at the beginning of the game
            'eco_points': 100,          # eco points at the beginning of the game
            'flight_price':200,         # price of a flight ticket          
            'random_luck': 0.50,        # the possibility of benefiting from random functions
            'player_location':str,      # player's current location (ICAO)
            'screen_name':str,          # player's screen name
            'criminal_headstart': 4,    # the criminal's head start at the start of the game
            'criminal_time': 3,         # the time interval at which the criminal flies to the next location
            'difficulty': 'easy',       # difficulty for quiz questions
            'quiz_questions':list,      # questions of player's difficulty and category
            'previous_question':dict,   # previously asked question in case of player have to solve it again
            'clue_solved':bool,         # have we solved a clue at current airport?
            'tried_luck':False,         # have we tried our luck at this airport yet?
            'talk_to_chief': False,     # have we talked to security chief at current airport or not? True=yes, False=no
            'previous_quiz_answer':bool,# did we answer right or wrong on previous quiz question? True=right, False=wrong
            'next_location': "",        # have we solved a clue at current airport or got the next location otherwise? True=yes, False=no
            'criminal_was_here':bool,   # security chief tells us if the criminal has been at the air port or not. True=has been, False=has not been
            'criminal_caught':False,    # have we caught the criminal yet? True=yes, False=no
            'win':bool,                 # when conditions meet to end the game, this is turned to True if we won and False if we lost the game
            'first_airport':True,        # are we at our first airport?
            'running_time':""
        }
    }


    # Screen_name input
    screen_name = str(input("Enter your game name: ")) 

    # Get parameters for game from difficulty_settings dictionary
    # user will be asked for a difficulty until valid inputs is given
    while True:
        difficulty_input = str(input("Choose difficulty of the game: 'E' = Easy, 'M' = Medium, 'H' = Hard: "))

        if difficulty_input.upper() in difficulty_settings:
            game_dict = difficulty_settings[difficulty_input.upper()] # stores the parameters ​​of the difficulty selected by the user 
            break # break out from loop when valid input is given
        else:
            print("You entered an invalid input.")

    # clears criminal table and adds "criminal_headstart" amount of airports 
    criminal_headstart(game_dict["criminal_headstart"]) 

    # Starting location
    sql = "SELECT location FROM criminal WHERE id = 1;"
    cursor = mysql_connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchone()

    # add screen_name and location to dict
    game_dict["player_location"] = result["location"]
    game_dict["screen_name"] = screen_name




    return game_dict # return dictionary with parameters and screen name



# Main block for testing
if __name__ == "__main__":
    game_dict = game_setup()
    print(game_dict)
    print(f"You have {game_dict["game_money"]}€ in your bank account. ")
    print(f"Screen name: {game_dict["screen_name"]}")
    print(f"You're at an airport with ICAO code: {game_dict["player_location"]}")