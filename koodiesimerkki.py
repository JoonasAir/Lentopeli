from multiprocessing import Process
from time import sleep
from mysql_connection import mysql_connection


def criminal_new_location():
    cursor = mysql_connection.cursor()
    sql = "INSERT INTO criminal (location) SELECT ident FROM airport WHERE continent = 'EU' AND type = 'large_airport' AND airport.name LIKE '%Airport' AND ident NOT IN (SELECT location FROM criminal) ORDER BY RAND() LIMIT 1;"
    cursor.execute(sql)

def criminal_timer(time_interval: int):
    while True:
        sleep(time_interval)
        criminal_new_location()
        print(" New location added")


if __name__ == "__main__":
    time_interval = 5

    # prosessin määrittely
    process_criminal_timer = Process(target=criminal_timer, args=(time_interval,))


# PELI ALKAA ################################################################
    # prosessin käynnistys
    process_criminal_timer.start()


    lista = [1,2]
    intti = int(1)


    x = input("Input: ")
    print(x)




    # prosessin välitön pysäytys
    process_criminal_timer.terminate()

    # varmistetaan, että pääohjelma odottaa prosessin täydellistä päättymistä ja siivousta ennen jatkamista 
    process_criminal_timer.join()
# PELI PÄÄTTYY ##############################################################

