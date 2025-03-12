from logging import warning
from mysql_connection import mysql_connection
from styles import styles

def talk_to_security(game_dict:dict, luck_bool:bool):

    cursor = mysql_connection.cursor()


    if game_dict["talk_to_chief"] == False: # If we haven't talked to the security chief yet at current airport
        game_dict["talk_to_chief"] = True # change state to True = we have talked to security at this airport
        sql = f"SELECT location FROM criminal WHERE Location = '{game_dict["player_location"]}';" # Check if our location is found in criminal-table
        cursor.execute(sql)
        result = cursor.fetchone()
        if type(result) == tuple:
            if game_dict["player_location"] in result: # If our location equals to the last of the visited locations in criminal-table
                print(styles["output"] + f"\nSecurity chief's monitows were down due to the criminal's attack.\nStill he had a clue about criminal for you. Try to solve it\n" + styles["reset"])
                game_dict["criminal_was_here"] = True

            else:
                print(styles["output"] + f"\nSecurity chief told you the criminal haven't been at the airport. Try to solve last clue again.\n" + styles["reset"])
                game_dict["criminal_was_here"] = False
        else:
            print(styles["warning"] + "No result from sql query" + styles["reset"])

    elif luck_bool and game_dict["criminal_was_here"]: # If criminal have been here and we got luck_booly
        game_dict["got_location"] = True
        sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchone()
        if type(result) == tuple:
            result = result[0][0]
            print(styles["output"] + f"\n{result}" + styles["reset"])
            print(styles["output"] + f"\nThe chief had just found the country where the criminal headed from here!" + styles["reset"])
            print(styles["output"] + f"\nThe fight ICAO-code is: {result}" + styles["reset"])
        else:
            print(styles["warning"] + "No result from sql query" + styles["reset"])
    elif game_dict["criminal_was_here"]:
        pass

    else:
        print(styles["output"] + f"\nThe chief had nothing new to tell you. He was still on a mission to recover his monitors from the attack of the criminal." + styles["reset"])


    return game_dict


if __name__ == "__main__":
    from questions import ask_category, ask_question, get_questions
    from game_setup import game_setup
    from game_parameters import game_parameters
    from random import randint

    game_dict = game_setup(game_parameters)
    luck_bool = bool(randint(0,1000000)/1000000 <= game_dict["random_luck"])
    # game_dict["quiz_category"] = ask_category()
    # game_dict["quiz_questions"] = get_questions(game_dict["difficulty"], game_dict["quiz_category"])

    game_dict = talk_to_security(game_dict, luck_bool)