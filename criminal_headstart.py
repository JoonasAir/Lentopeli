from criminal_timer_multiprocessing import criminal_new_location
from mysql_connection import mysql_connection

# criminal_headstart() -funktio ottaa parametriksi game_setup() -funktiossa määritellyn criminal_headstart -muuttujan.
# funktio tyhjentää criminal-taulun edellisen pelin jäljiltä ja lisää rikolliselle etumatkaksi määritellyn luvun verran ICAO-koodeja
# funktio ei palauta mitään

def criminal_headstart(headstart:int):
    cursor = mysql_connection.cursor()
    sql = "DELETE FROM criminal;" # Empties criminal table
    cursor.execute(sql)
    sql = "ALTER TABLE criminal AUTO_INCREMENT = 1;" # Resets auto increment
    cursor.execute(sql)

    for i in range(headstart): # adds X amount of locations to criminal table (amt. specified by difficulty) 
        criminal_new_location()






if __name__ == "__main__":

    criminal_headstart(3)