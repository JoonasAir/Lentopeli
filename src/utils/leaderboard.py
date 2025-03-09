#from colorama import Style
<<<<<<< HEAD:leaderboard.py
from settings import colors
<<<<<<< HEAD
import mysql.connector
from config import mysql_connection
=======
=======
from src.config import colors
>>>>>>> 10a43b33d146b00ec35a7075def8caad9320c851:src/utils/leaderboard.py
from db.config import mysql_connection
from db.queries import queries
>>>>>>> 23d876f1ffd08933d76517dedd4cc7982dd746ba
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

<<<<<<< HEAD
=======
    input(colors["input"] + "\nPress enter to return to the main menu." + colors["reset_color"])


leaderboard()
>>>>>>> 23d876f1ffd08933d76517dedd4cc7982dd746ba
