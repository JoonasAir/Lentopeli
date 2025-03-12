from mysql_connection import mysql_connection
from styles import styles




def change_location(game_dict):
    cursor = mysql_connection.cursor()
    sql = "SELECT ident FROM airport WHERE name LIKE '%airport'"
    cursor.execute(sql)
    database = cursor.fetchall()
    game_dict["player_location"] = input(styles["input"] + "Give ICAO-code for the airport where you want to travel next: " + styles["reset"])
    ICA = []
    for row in database:
        ICA.append(row[0])
    while game_dict["player_location"] not in ICA:
        game_dict["player_location"] = input(styles["input"] + "ICAO-code not found! Try again: " + styles["reset"])


def print_location(icao):
    cursor = mysql_connection.cursor(dictionary=True)
    sql = f"SELECT country.name AS country, airport.name AS airport FROM airport, country WHERE country.iso_country = airport.iso_country AND airport.ident = '{icao}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    print(styles["output"] + f"\n\n\nLater you arrived to {result['airport']}, {result['country']}.\n\n" + styles["reset"])



if __name__ == "__main__":
    print_location("EFHK")