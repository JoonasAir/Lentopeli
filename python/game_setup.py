from criminal import criminal_headstart
from python.mysql_connection import mysql_connection


# game_setup() funktiossa käyttäjä valitsee pelin vaikeusasteen, pelinimen, sekä pelaajalle arvotaan aloituslentokenttä
# tiedot palautetaan sanakirjana

def game_setup(game_parameters:dict):
    
    # Screen_name input
    screen_name = str(input("Enter your game name: ")) 

    # Get parameters for game from game_parameters dictionary
    # user will be asked for a difficulty until valid inputs is given  
    while True:
        difficulty_input = str(input("\nChoose difficulty of the game:\n    'E' = Easy\n    'M' = Medium\n    'H' = Hard\n    'C' = Custom\nInput: "))

        if difficulty_input.upper() in game_parameters:
            game_dict = game_parameters[difficulty_input.upper()] # stores the parameters ​​of the difficulty selected by the user 
            break # break out from loop when valid input is given
        else:
            print("\nInvalid input. Try again.\n")

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