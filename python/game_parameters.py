from copy import deepcopy


# difficulty specified parameters
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
    'C': { # Custom (played can modify these in: main menu -> settings -> custom difficulty's settings)
        'game_money': 5000,         # money at the beginning of the game
        'flight_price':200,         # price of a flight ticket          
        'game_time': 60*5,          # time at the beginning of the game
        'criminal_headstart': 2,    # the criminal's head start at the start of the game
        'criminal_time': 30,         # the time interval at which the criminal flies to the next location
        'difficulty': 'easy',       # difficulty for quiz questions
        'random_luck': 0.3,        # the possibility of benefiting from random functions
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

airport_random_actions = [
("Visit the restroom", 
"You overheard a conversation in the restroom about Shadow's next move! The individuals were discussing a recent sighting of Shadow boarding a flight. You decide to verify this information and find out it's true; you got his next location.", 
"You went to the restroom and now feel refreshed.", 
"You already went to the restroom. No need to go again."),

("Go to get a cup of coffee", 
"The barista, recognizing you as an Interpol agent, mentioned seeing someone suspicious matching Shadow's description. They saw him purchasing a ticket at the counter. You decide to follow up on this lead and confirm that Shadow was indeed spotted here recently; you got his next location.", 
"You went to get a large cup of coffee and now feel more energized.", 
"Maybe it's better not to get a second cup of coffee. You've had enough caffeine."),

("Go to get a meal", 
"A fellow diner, impressed by your Interpol badge, shared a rumor about Shadow's next move. They overheard Shadow talking on the phone about his next flight. You decide to verify this information and discover it's all true; you got his next location.", 
"You went to grab a hamburger meal and now feel satisfied.", 
"You already went to McDonald's. You're not hungry anymore."),

("Go to relax in a lounge", 
"You saw a live news report in the lounge hinting at Shadow's activities! The report mentioned increased security due to a recent sighting of Shadow. You decide to verify this information and find out that the report is accurate; you got his next location.", 
"You went to the lounge to rest for a moment and now feel rejuvenated.", 
"You already relaxed in the lounge. Time to get back to work."),

("Browse the duty-free shop", 
"A shop assistant, noticing your Interpol credentials, mentioned seeing someone suspicious. They saw Shadow making a purchase and then heading towards the gates. You decide to investigate further and confirm that the person was indeed acting suspiciously; you got his next location.", 
"You browsed the duty-free shop and found some interesting items.", 
"You already browsed the duty-free shop. No need to go again."),

("Check the flight information board", 
"You noticed some unusual activity on the flight information board. You decide to check it out and discover that Shadow has been tampering with the flight schedules. The tampering indicates his next move; you got his next location.", 
"You checked the flight information board and confirmed your flight details.", 
"You already checked the flight information board. No need to check again."),

("Talk to the information desk", 
"The staff at the information desk, eager to assist an Interpol agent, gave you a tip about Shadow's next move. They received a report from security about Shadow's recent activity. You decide to follow up on this lead and find out that the tip is credible; you got his next location.", 
"You talked to the information desk and got some useful travel information.", 
"You already talked to the information desk. No need to ask again."),

("Visit the airport bookstore", 
"You found a live news broadcast in the bookstore with an update on Shadow's activities! The broadcast mentioned a recent sighting of Shadow in the airport. You decide to verify this information and confirm that the broadcast is providing accurate updates; you got his next location.", 
"You visited the airport bookstore and found some interesting reads.", 
"You already visited the airport bookstore. No need to go again."),

("Take a walk around the terminal", 
"You overheard a conversation about Shadow's next move while walking. The individuals were discussing seeing Shadow near the boarding gates. You decide to investigate further and find out that the conversation was based on a real sighting; you got his next location.", 
"You took a walk around the terminal and stretched your legs.", 
"You already took a walk around the terminal. No need to walk again."),

("Charge your phone at a charging station", 
"You saw a suspicious person leaving a note at the charging station. The note mentioned Shadow's next flight. You decide to check it out and discover that the note contains valuable information about Shadow's plans; you got his next location.", 
"You charged your phone and now have a full battery.", 
"You already charged your phone. No need to charge again.")
]


# adding common parameters dictionary to each difficulty's (Easy, Mesium, Hard, Custom) dictionary in difficulty dictionary
for difficulty in DIFFICULTY_game_parameters:
    DIFFICULTY_game_parameters[difficulty].update(COMMON_game_parameters)


# Create two copys of the updated difficulty dictionary. Other is used in game and other is used to reset default-settings
game_parameters = deepcopy(DIFFICULTY_game_parameters)
game_parameters_DEFAULT = deepcopy(DIFFICULTY_game_parameters)

