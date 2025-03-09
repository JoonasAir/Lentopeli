from colorama import Style
<<<<<<< HEAD
from config import mysql_connection
=======
from db.config import mysql_connection
>>>>>>> 23d876f1ffd08933d76517dedd4cc7982dd746ba
from settings import colors


def security(game_dict, luck):

    cursor = mysql_connection.cursor()


    if game_dict["talk_to_chief"] == False: # If we haven't talked to the security chief yet at current airport
        game_dict["talk_to_chief"] = True # change state to True = we have talked to security at this airport
        sql = f"SELECT location FROM criminal WHERE Location = '{game_dict["player_location"]} ';" # Check if our location is found in criminal-table
        cursor.execute(sql)
        result = str(cursor.fetchone())

        if game_dict["player_location"] == result: # If our location equals to the last of the visited locations in criminal-table
            print(colors["output"] + f"\nSecurity chief's monitows were down due to the criminal's attack.\nStill he had a clue about criminal for you. Try to solve it\n" + Style.RESET_ALL)
            game_dict["criminal_was_here"] = True

        else:
            print(colors["output"] + f"\nSecurity chief told you the criminal haven't been at the airport. Try to solve last clue again.\n" + Style.RESET_ALL)
            game_dict["criminal_was_here"] = False


    elif luck and game_dict["criminal_was_here"]: # If criminal have been here and we got lucky
        game_dict["got_location"] = True
        sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchone()
        result = result[0][0]
        print(colors["output"] + f"\n{result}" + Style.RESET_ALL)
        print(colors["output"] + f"\nThe chief had just found the country where the criminal headed from here!" + Style.RESET_ALL)
        print(colors["output"] + f"\nThe fight ICAO-code is: {result}" + Style.RESET_ALL)

    elif game_dict["criminal_was_here"]:
        pass

    else:
        print(colors["output"] + f"\nThe chief had nothing new to tell you. He was still on a mission to recover his monitors from the attack of the criminal." + Style.RESET_ALL)


    return game_dict