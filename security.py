from mysql_connection import mysql_connection
from styles import styles

def security(game_dict, luck):

    cursor = mysql_connection.cursor()


    if game_dict["talk_to_chief"] == False: # If we haven't talked to the security chief yet at current airport
        game_dict["talk_to_chief"] = True # change state to True = we have talked to security at this airport
        sql = f"SELECT location FROM criminal WHERE Location = '{game_dict["player_location"]} ';" # Check if our location is found in criminal-table
        cursor.execute(sql)
        result = str(cursor.fetchone())

        if game_dict["player_location"] == result: # If our location equals to the last of the visited locations in criminal-table
            print(styles["output"] + f"\nSecurity chief's monitows were down due to the criminal's attack.\nStill he had a clue about criminal for you. Try to solve it\n" + styles["reset"])
            game_dict["criminal_was_here"] = True

        else:
            print(styles["output"] + f"\nSecurity chief told you the criminal haven't been at the airport. Try to solve last clue again.\n" + styles["reset"])
            game_dict["criminal_was_here"] = False


    elif luck and game_dict["criminal_was_here"]: # If criminal have been here and we got lucky
        game_dict["got_location"] = True
        sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchone()
        result = result[0][0]
        print(styles["output"] + f"\n{result}" + styles["reset"])
        print(styles["output"] + f"\nThe chief had just found the country where the criminal headed from here!" + styles["reset"])
        print(styles["output"] + f"\nThe fight ICAO-code is: {result}" + styles["reset"])

    elif game_dict["criminal_was_here"]:
        pass

    else:
        print(styles["output"] + f"\nThe chief had nothing new to tell you. He was still on a mission to recover his monitors from the attack of the criminal." + styles["reset"])


    return game_dict