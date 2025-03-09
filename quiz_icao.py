from db.config import mysql_connection

# takes following parameters:
#   1. boolean (from ask_question() -function)
#       True    ->    return ICAO for the next location in the criminal-table the player has not visited yet 
#       False   ->    return random ICAO (not player's current location and not found in criminal-table)
#   2. Player's current location (ICAO-code)


def quiz_icao(answer:bool, player_location):
    cursor = mysql_connection.cursor()

    if answer == True:      # return right ICAO-code
        sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0]

    elif answer == False:   # return wrong ICAO-code
        sql = f"SELECT ident FROM airport WHERE continent = 'EU' AND type = 'large_airport' AND ident NOT IN (SELECT location FROM criminal) AND ident != '{player_location}' ORDER BY RAND() LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result[0]


if __name__ == "__main__": # Test code
    print(quiz_icao(True, "EFHK"))
    print(quiz_icao(False, "EFHK"))