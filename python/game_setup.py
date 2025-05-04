from criminal import criminal_headstart
from mysql_connection import mysql_connection


# game_setup() funktiossa käyttäjä valitsee pelin vaikeusasteen, pelinimen, sekä pelaajalle arvotaan aloituslentokenttä
# tiedot palautetaan sanakirjana

def game_setup(game_parameters:dict, data:dict):

    difficulty_input = data["difficulty_input"] 

    if difficulty_input in game_parameters:
        game_dict = game_parameters[difficulty_input]
    else:
        print("\nINVALID DIFFICULTY.\n")

    # clears criminal table and adds "criminal_headstart" amount of airports 
    km_co2 = criminal_headstart(game_dict["criminal_headstart"]) 

    # Starting location
    sql = "SELECT location FROM criminal WHERE id = 1;"
    cursor = mysql_connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchone()

    # add screen_name, category and location to dict
    game_dict["quiz_category"] = data["category_input"]
    game_dict["screen_name"] = data["name_input"]
    game_dict["player_location"] = result["location"]
    game_dict["KM_criminal"] =+ km_co2[0]
    game_dict["CO2_criminal"] =+ km_co2[1]



    return game_dict # return dictionary with parameters and screen name



# Main block for testing
if __name__ == "__main__":
    game_dict = game_setup()
    print(game_dict)
    print(f"You have {game_dict["game_money"]}€ in your bank account. ")
    print(f"Screen name: {game_dict["screen_name"]}")
    print(f"You're at an airport with ICAO code: {game_dict["player_location"]}")