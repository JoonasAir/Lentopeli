from styles import styles
from mysql_connection import mysql_connection
from prettytable import PrettyTable

def leaderboard():
    
    sql = "SELECT screen_name, points FROM leaderboard ORDER BY points DESC;"
    kursori = mysql_connection.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    
    # Luodaan taulukko otsikoilla RANK, NAME & POINTS
    table = PrettyTable(["RANK", "NAME", "POINTS"])
    rank = 1
    for i in tulos[:10]:
        name, points = i
        table.add_row([rank, name, points])# Lisätään taulukkoon riveittäin muuttujat name&points
        table.add_divider() # Jaotellaan rivit viivalla
        rank += 1 # Lisätään sijoitukset
    
    result = table

    print(styles["output"] + f"{result}" + styles["reset"])

    input(styles["input"] + "\nPress enter to return to the main menu." + styles["reset"])


if __name__ == "__main__":
    leaderboard()