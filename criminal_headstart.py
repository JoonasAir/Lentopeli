from criminal_timer_multiprocessing import criminal_new_location
from mysql_connection import mysql_connection



def criminal_headstart(times:int):
    cursor = mysql_connection.cursor()
    sql = "DELETE FROM criminal;" # Empties criminal table
    cursor.execute(sql)
    sql = "ALTER TABLE criminal AUTO_INCREMENT = 1;" # Resets auto increment
    cursor.execute(sql)

    for i in range(times): # adds X amount of locations to criminal table (amt. specified by difficulty) 
        criminal_new_location()






if __name__ == "__main__":

    criminal_headstart(3)