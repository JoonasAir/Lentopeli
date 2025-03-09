from colorama import Fore, Style
<<<<<<< HEAD:game_setup.py
from criminal import criminal_headstart
<<<<<<< HEAD
from config import mysql_connection
=======
from db.config import mysql_connection
>>>>>>> 23d876f1ffd08933d76517dedd4cc7982dd746ba
from settings import colors
=======
from src.utils.criminal import criminal_headstart
from db.config import mysql_connection
from src.config import colors
>>>>>>> 10a43b33d146b00ec35a7075def8caad9320c851:src/utils/game_setup.py



# game_setup() funktiossa käyttäjä valitsee pelin vaikeusasteen, pelinimen, sekä pelaajalle arvotaan aloituslentokenttä
# tiedot palautetaan sanakirjana

def game_setup(difficulty_settings):
    
    # Screen_name input
    screen_name = str(input(colors["input"] + "Enter your game name: " + Style.RESET_ALL)) 

    # Get parameters for game from difficulty_settings dictionary
    # user will be asked for a difficulty until valid inputs is given  
    while True:
        difficulty_input = str(input(colors["input"] + "\nChoose difficulty of the game:\n    'E' = Easy\n    'M' = Medium\n    'H' = Hard\n    'C' = Custom\nInput: " + Style.RESET_ALL))

        if difficulty_input.upper() in difficulty_settings:
            game_dict = difficulty_settings[difficulty_input.upper()] # stores the parameters ​​of the difficulty selected by the user 
            break # break out from loop when valid input is given
        else:
            print(colors["warning"] + "\nInvalid input. Try again.\n" + Style.RESET_ALL)

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