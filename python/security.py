from mysql_connection import mysql_connection

def talk_to_security(game_dict:dict):
    if not mysql_connection.is_connected():
        mysql_connection.reconnect()
    cursor = mysql_connection.cursor()
    game_dict["game_output"] = []

    if game_dict["talk_to_chief"] == False: # If we haven't talked to the security chief yet at current airport
        game_dict["talk_to_chief"] = True # change state to True = we have talked to security at this airport
        sql = f"SELECT location FROM criminal WHERE Location = '{game_dict['player_location']}';" # Check if our location is found in criminal-table
        cursor.execute(sql)
        result = cursor.fetchone()
        if type(result) == tuple: # If result is tupole, our location is found on criminal's table
            game_dict["game_output"].append(f"\nSecurity chief's monitows were down due to the criminal's attack.\nStill he had a clue about criminal for you. Try to solve it\n")
            game_dict["criminal_was_here"] = True

        else:
            game_dict["game_output"].append(f"\nSecurity chief told you the criminal haven't been at the airport. Try to solve last clue again.\n")
            game_dict["criminal_was_here"] = False

    elif game_dict["random_luck_bool"] and game_dict["criminal_was_here"] and not game_dict["tried_luck"]: # If criminal have been here AND we got lucky AND we haven't tried our luck yet at the current airport
        game_dict["tried_luck"] = True
        sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchone()
        if type(result) == tuple:
            game_dict["next_location_bool"] = True
            game_dict["next_location"] = result[0]
            game_dict["game_output"].append(f"\nThe chief had just found the country where the criminal headed from here!")
            
    else:
        game_dict["game_output"].append(f"\nThe chief had nothing new to tell you. He was still on a mission to recover his monitors from the attack of the criminal.")


    return game_dict


if __name__ == "__main__":
    from questions import ask_category, ask_question, get_questions
    from game_setup import game_setup
    from game_parameters import game_parameters
    from random import randint

    game_dict = game_setup(game_parameters)
    game_dict["random_luck_bool"] = bool(randint(0,1000000)/1000000 <= game_dict["random_luck"])
    # game_dict["quiz_category"] = ask_category()
    # game_dict["quiz_questions"] = get_questions(game_dict["difficulty"], game_dict["quiz_category"])

    game_dict = talk_to_security(game_dict)