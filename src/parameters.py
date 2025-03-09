from colorama import Fore, Style

default_colors = {
    "input":Fore.CYAN,
    "warning":Fore.RED,
    "time":Fore.LIGHTBLUE_EX,
    "location":Fore.LIGHTYELLOW_EX,
    "menu":Fore.LIGHTMAGENTA_EX,
    "output":Fore.GREEN,
    "reset_color":Style.RESET_ALL
}
colors = default_colors.copy()

difficulty_settings = {
    'E': { # Easy
        'game_money': 5000,         # money at the beginning of the game
        'game_time': 60*10,         # time at the beginning of the game
        'eco_points': 100,          # eco points at the beginning of the game
        'random_luck': 0.10,        # the possibility of benefiting from random functions
        'criminal_headstart': 2,    # the criminal's head start at the start of the game
        'criminal_time': 60,        # the time interval at which the criminal flies to the next location
        'difficulty': 'easy'        # difficulty for quiz questions
    },
    'M': { # Medium
        'game_money': 4000,         # money at the beginning of the game
        'game_time': 60*7,          # time at the beginning of the game
        'eco_points': 100,          # eco points at the beginning of the game
        'random_luck': 0.05,        # the possibility of benefiting from random functions
        'criminal_headstart': 3,    # the criminal's head start at the start of the game
        'criminal_time': 45,        # the time interval at which the criminal flies to the next location
        'difficulty': 'medium'      # difficulty for quiz questions
    },
    'H': { # Hard
        'game_money': 3000,         # money at the beginning of the game
        'game_time': 60*5,          # time at the beginning of the game
        'eco_points': 100,          # eco points at the beginning of the game
        'random_luck': 0.025,       # the possibility of benefiting from random functions
        'criminal_headstart': 4,    # the criminal's head start at the start of the game
        'criminal_time': 30,        # the time interval at which the criminal flies to the next location
        'difficulty': 'hard'        # difficulty for quiz questions

    },
    'C': { # For testing purposes. Feel free to adjust during testing. This will be removed from the actual game.
        'game_money': 5000,         # money at the beginning of the game
        'game_time': 60*5,          # time at the beginning of the game
        'eco_points': 100,          # eco points at the beginning of the game
        'random_luck': 0.50,        # the possibility of benefiting from random functions
        'criminal_headstart': 4,    # the criminal's head start at the start of the game
        'criminal_time': 3,         # the time interval at which the criminal flies to the next location
        'difficulty': 'easy'        # difficulty for quiz questions

    }
}

common_settings = {
        'flight_price':200,         # price of a flight ticket          
        'player_location':str,      # player's current location (ICAO)
        'screen_name':str,          # player's screen name
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
        'first_airport':True,       # are we at our first airport?
        'time_left_str':"",         # time left at the game: Formatted string telling minutes and seconds
        'time_left_bool':True,      # time left at the game: True/False
        'first_iteration':True,     # is this first iteration of the loop at current airport? 
        'random_index_airport':0    # random index that defines random action we can do at current airport
}




"""'C': { # For testing purposes. Feel free to adjust during testing. This will be removed from the actual game.
        'game_money': 5000,         # money at the beginning of the game
        'game_time': 60*5,          # time at the beginning of the game
        'eco_points': 100,          # eco points at the beginning of the game
        'random_luck': 0.50,        # the possibility of benefiting from random functions
        'criminal_headstart': 4,    # the criminal's head start at the start of the game
        'criminal_time': 3,         # the time interval at which the criminal flies to the next location
        'difficulty': 'easy'        # difficulty for quiz questions
        'flight_price':200,         # price of a flight ticket          """



def settings(difficulty_settings, colors):

    while True:
        print(colors["menu"] + "\nS E T T I N G S\n\n"+ Style.RESET_ALL)

        option_number = 1
        menu = "Select from following options:\n"

        menu += f"    {option_number} - Custom difficulty's settings\n"
        option_number += 1

        menu += f"    {option_number} - Appearance settings\n"

        menu += f"    0 - Back to main menu\n"
        menu += "Input: "

        while True: # Asks input until valid one is given
            try:
                user_input = int(input(colors['input'] + menu + Style.RESET_ALL))
                if user_input in range(option_number+1):
                    break
                else:
                    print(colors["warning"] + "Invalid input. Try again." + Style.RESET_ALL)
            except ValueError:
                print(colors["warning"] + "Invalid input. Try again." + Style.RESET_ALL)


        if user_input == 1: # Custom difficulty's settings
            while True:

                print(colors["menu"] + "\nS E T T I N G S   -   C U S T O M   D I F F I C U L T Y\n\n"+ Style.RESET_ALL)
    
                option_number = 1
                menu = "Select from following options:\n"
    
                menu += f"    {option_number} - amount of money at the beginning of the game\n"
                option_number += 1
                menu += f"    {option_number} - price of a flight ticket\n"
                option_number += 1
                menu += f"    {option_number} - time to catch the criminal\n"
                option_number += 1
                menu += f"    {option_number} - criminal's head start at the start of the game\n"
                option_number += 1
                menu += f"    {option_number} - time interval at which the criminal flies to the next location\n"
                option_number += 1
                menu += f"    {option_number} - difficulty for quiz questions\n"
                option_number += 1
                menu += f"    {option_number} - possibility of gaining random benefits\n"
                menu += f"    0 - Back to settings menu\n"
                menu += "Input: "

                while True: # Asks input until valid one is given
                    try:
                        user_input = int(input(colors['input'] + menu + Style.RESET_ALL))
                        if user_input in range(option_number+1):
                            break
                        else:
                            print(colors["warning"] + "Invalid input. Try again." + Style.RESET_ALL)
                    except ValueError:
                        print(colors["warning"] + "Invalid input. Try again." + Style.RESET_ALL)


                if user_input == 1:
                    user_input = int(input(colors['input'] + "Give amount of money you would like to have in the beginning of the game: ") + Style.RESET_ALL)
                    #        'game_money': 5000,         # money at the beginning of the game
                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)

                if user_input == 2:
                    user_input = int(input(colors['input'] + ": ") + Style.RESET_ALL)
                    #        'flight_price':200,         # price of a flight ticket          """
                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)

                if user_input == 3:
                    user_input = int(input(colors['input'] + ": ") + Style.RESET_ALL)
                    #        'game_time': 60*5,          # time at the beginning of the game
                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)

                if user_input == 4:
                    user_input = int(input(colors['input'] + ": ") + Style.RESET_ALL)
                    #        'criminal_headstart': 4,    # the criminal's head start at the start of the game
                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)

                if user_input == 5:
                    user_input = int(input(colors['input'] + ": ") + Style.RESET_ALL)
                    #        'criminal_time': 3,         # the time interval at which the criminal flies to the next location
                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)

                if user_input == 6:
                    user_input = int(input(colors['input'] + ": ") + Style.RESET_ALL)
                    #        'difficulty': 'easy'        # difficulty for quiz questions
                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)

                if user_input == 7:
                    user_input = int(input(colors['input'] + ": ") + Style.RESET_ALL)
                    #        'random_luck': 0.50,        # the possibility of benefiting from random functions
                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)

                if user_input == 0:
                    break



        elif user_input == 2: # Appereance settings
            while True:

                print(colors["menu"] + "\nS E T T I N G S   -   A P P E A R A N C E\n\n"+ Style.RESET_ALL)
    
                option_number = 1
                menu = "Change color of:\n"
    
                menu += f"    {option_number} - input prints\n"
                option_number += 1
                menu += f"    {option_number} - warning prints\n"
                option_number += 1
                menu += f"    {option_number} - output prints\n"
                option_number += 1
                menu += f"    {option_number} - menu location prints ('S E T T I N G S' etc.)\n"
                option_number += 1
                menu += f"    {option_number} - in-game location prints ('You're in aiport/country X')\n"
                option_number += 1
                menu += f"    {option_number} - in-game time prints (You have min:sec time left)\n"
                menu += f"    0 - Back to settings menu\n"
                menu += "Input: "

                while True: # Asks input until valid one is given
                    try:
                        user_input = int(input(colors['input'] + menu + Style.RESET_ALL))
                        if user_input in range(option_number+1):
                            break
                        else:
                            print(colors["warning"] + "Invalid input. Try again." + Style.RESET_ALL)
                    except ValueError:
                        print(colors["warning"] + "Invalid input. Try again." + Style.RESET_ALL)




                if user_input == 1: # input prints
                    user_input = int(input(colors['input'] + "Select color for input prints: ") + Style.RESET_ALL)
                    # "input":Fore.CYAN

                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)



                if user_input == 2: # warning prints
                    user_input = int(input(colors['input'] + ": ") + Style.RESET_ALL)
                    # "warning":Fore.RED

                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)



                if user_input == 3: # output prints
                    user_input = int(input(colors['input'] + ": ") + Style.RESET_ALL)
                    # "output":Fore.LIGHTYELLOW_EX

                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)



                if user_input == 4: # menu location prints ('S E T T I N G S' etc.)
                    user_input = int(input(colors['input'] + ": ") + Style.RESET_ALL)
                    # "menu":Fore.LIGHTMAGENTA_EX

                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)



                if user_input == 5: # in-game location prints ('You're in aiport/country X')
                    user_input = int(input(colors['input'] + ": ") + Style.RESET_ALL)
                    # "location":Fore.LIGHTGREEN_EX

                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)



                if user_input == 6: # in-game time prints (You have min:sec time left)
                    user_input = int(input(colors['input'] + ": ") + Style.RESET_ALL)
                    # "time":Fore.LIGHTBLUE_EX

                    print(colors['warning'] + "NOT WORKING YET!" + Style.RESET_ALL)



                if user_input == 0: # Back to settings menu
                    break



        elif user_input == 0: # Back to main menu
            break


