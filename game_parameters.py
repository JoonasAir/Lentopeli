# difficulty specified parameters
from copy import deepcopy


DIFFICULTY_game_parameters = {
    'E': { # Easy
        'game_money': 5000,         # money at the beginning of the game
        'flight_price':200,         # price of a flight ticket          
        'game_time': 60*10,         # time at the beginning of the game
        'criminal_headstart': 2,    # the criminal's head start at the start of the game
        'criminal_time': 60,        # the time interval at which the criminal flies to the next location
        'difficulty': 'easy',       # difficulty for quiz questions
        'random_luck': 0.10,        # the possibility of benefiting from random functions
        'eco_points': 100,          # eco points at the beginning of the game
    },
    'M': { # Medium
        'game_money': 4000,         # money at the beginning of the game
        'flight_price':200,         # price of a flight ticket          
        'game_time': 60*7,          # time at the beginning of the game
        'criminal_headstart': 3,    # the criminal's head start at the start of the game
        'criminal_time': 45,        # the time interval at which the criminal flies to the next location
        'difficulty': 'medium',     # difficulty for quiz questions
        'random_luck': 0.05,        # the possibility of benefiting from random functions
        'eco_points': 100,          # eco points at the beginning of the game
    },
    'H': { # Hard
        'game_money': 3000,         # money at the beginning of the game
        'flight_price':200,         # price of a flight ticket          
        'game_time': 60*5,          # time at the beginning of the game
        'criminal_headstart': 4,    # the criminal's head start at the start of the game
        'criminal_time': 30,        # the time interval at which the criminal flies to the next location
        'difficulty': 'hard',       # difficulty for quiz questions
        'random_luck': 0.025,       # the possibility of benefiting from random functions
        'eco_points': 100,          # eco points at the beginning of the game

    },
    'C': { # Custom (played can modify these from main menu -> settings -> custom difficulty's settings)
        'game_money': 5000,         # money at the beginning of the game
        'flight_price':200,         # price of a flight ticket          
        'game_time': 100,          # time at the beginning of the game
        'criminal_headstart': 2,    # the criminal's head start at the start of the game
        'criminal_time': 30,         # the time interval at which the criminal flies to the next location
        'difficulty': 'easy',       # difficulty for quiz questions
        'random_luck': 1,        # the possibility of benefiting from random functions
        'eco_points': 100,          # eco points at the beginning of the game

    }
}


# Helper parameters for the game. These are combined with difficulty parameters to be one dictionary "game_dict"
COMMON_game_parameters = {
        'player_location':str,      # player's current location (ICAO)
        "win_game":bool,            # did we win the game? True = Yes, False = No
        'screen_name':str,          # player's screen name
        'quiz_questions':list,      # questions of player's difficulty and category
        'previous_question':dict,   # previously asked question in case of player have to solve it again
        'clue_solved':bool,         # have we solved a clue at current airport?
        'tried_luck':False,         # have we tried our luck at this airport yet?
        'talk_to_chief': False,     # have we talked to security chief at current airport or not? True=yes, False=no
        'previous_quiz_answer':bool,# did we answer right or wrong on previous quiz question? True=right, False=wrong
        'next_location_bool':False,        # have we solved a clue at current airport or got the next location otherwise? True=yes, False=no
        'criminal_was_here':bool,   # security chief tells us if the criminal has been at the air port or not. True=has been, False=has not been
        'criminal_caught':False,    # have we caught the criminal yet? True=yes, False=no
        'win':bool,                 # when conditions meet to end the game, this is turned to True if we won and False if we lost the game
        'first_airport':True,       # are we at our first airport?
        'time_left_str':"",         # time left at the game: Formatted string telling minutes and seconds
        'time_left_bool':True,      # time left at the game: True/False
        'first_iteration':True,     # is this first iteration of the loop at current airport? 
        'random_index_airport':0,   # random index that defines random action we can do at current airport
        'previous_question':list,   # list of previously asked question
}


# adding common parameters dictionary to each difficulty's (Easy, Mesium, Hard, Custom) dictionary in difficulty dictionary
for difficulty in DIFFICULTY_game_parameters:
    DIFFICULTY_game_parameters[difficulty].update(COMMON_game_parameters)


# Create two copys of the updated difficulty dictionary. Other is used in game and other is used to reset default-settings
game_parameters = deepcopy(DIFFICULTY_game_parameters)
game_parameters_DEFAULT = deepcopy(DIFFICULTY_game_parameters)

