#from colorama import Style
from src.config import colors
from db.config import mysql_connection
from db.queries import queries
from prettytable import PrettyTable

def leaderboard():
    
    sql = queries.leaderboard_query
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

    print(colors["output"] + f"{result}" + colors["reset_color"])

    input(colors["input"] + "\nPress enter to return to the main menu." + colors["reset_color"])


leaderboard()