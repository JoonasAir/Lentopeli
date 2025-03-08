from colorama import Style
from settings import colors
import mysql.connector
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
    for i in tulos:
        name, points = i
        table.add_row([rank, name, points])# Lisätään taulukkoon riveittäin muuttujat name&points
        table.add_divider() # Jaotellaan rivit viivalla
        rank += 1 # Lisätään sijoitukset
    
    result = table

    print(colors["output"] + f"{result}" + Style.RESET_ALL)

    input(colors["input"] + "\nPress enter to return to the main menu." + Style.RESET_ALL)



leaderboard()