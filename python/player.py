from python.mysql_connection import mysql_connection




def change_location(game_dict):
    cursor = mysql_connection.cursor()
    sql = "SELECT ident FROM airport WHERE name LIKE '%airport'"
    cursor.execute(sql)
    database = cursor.fetchall()
    game_dict["player_location"] = input("Give ICAO-code for the airport where you want to travel next: ").upper()
    ICA = []
    for row in database:
        ICA.append(row[0])
    while game_dict["player_location"] not in ICA:
        game_dict["player_location"] = input("ICAO-code not found! Try again: ").upper()


def print_location(icao):
    cursor = mysql_connection.cursor(dictionary=True)
    sql = f"SELECT country.name AS country, airport.name AS airport FROM airport, country WHERE country.iso_country = airport.iso_country AND airport.ident = '{icao}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    print(f"\n\n\nLater you arrived to {result['airport']}, {result['country']}.\n\n")



if __name__ == "__main__":
    print_location("EFHK")