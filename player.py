from mysql_connection import mysql_connection
from styles import styles




def change_location(game_dict):
    game_dict["player_location"] = game_dict["next_location"]
    game_dict["next_location"] = ""

def print_location(icao):
    cursor = mysql_connection.cursor(dictionary=True)
    sql = f"SELECT country.name AS country, airport.name AS airport FROM airport, country WHERE country.iso_country = airport.iso_country AND airport.ident = '{icao}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    print(styles["output"] + f"\n\n\nLater you arrived to {result['airport']}, {result['country']}.\n\n" + styles["reset"])



if __name__ == "__main__":
    print_location("EFHK")