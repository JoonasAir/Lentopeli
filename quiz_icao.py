import mysql.connector
from mysql_connection import mysql_connection

# take boolean as parameter:
#   True    ->    return right ICAO
#   False   ->    return random ICAO 


def quiz_icao(answer:bool):
    cursor = mysql_connection.cursor(dictionary=True)

    if answer == True:      # return right ICAO-code
        sql = "SELECT ident FROM airport WHERE continent = 'EU' AND type = 'large_airport' ORDER BY RAND() LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

    elif answer == False:   # return wrong ICAO-code
        sql = "SELECT ident FROM airport WHERE continent = 'EU' AND type = 'large_airport' ORDER BY RAND() LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result


if __name__ == "__main__":
    print(quiz_icao(True))
    print(quiz_icao(False))