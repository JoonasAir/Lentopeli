from time import sleep
from mysql_connection import mysql_connection
from geopy import distance

# tässä tiedostossa on määritetty neljä funktiota: 
#   1. criminal_new_location(), joka ei vaadi parametrejä. Funktio lisää criminal-tauluun uuden ICAO-koodin
#
#   2. criminal_timer(), joka on tarkoitettu ajettavaksi taustalla multiprocessing-kirjaston avulla. Funktio haluaa parametrit:
#       criminal_timer_state  =  funktion sisäiselle loopille pelin alussa True ja pelin lopussa tämä arvo muutetaan -> False
#       time  =  sekuntit jonka välein criminal-tauluun lisätään uusi ICAO-koodi criminal_new_location() -funktion avulla
#
#   3. criminal_headstart(), joka tyhjentää criminal-taulun edellisen pelin jäljiltä ja lisää rikolliselle etumatkaksi määritellyn luvun verran ICAO-koodeja
#      Funktio ottaa parametriksi: 
#       game_setup() -funktiossa määritellyn criminal_headstart -muuttujan.
#   
#   Nämä funktiot eivät palauta mitään.
#
#   4. criminal_caught(), joka tarkistaa olemmeko rikollisen kanssa samalla lentoasemalla.
#      Tämä funktio: 
#           ottaa parametriksi pelaajan sijainnin (game_dict["player_location"])
#           palauttaa boolean-arvon: 
#               True  = olemme samalla kentällä
#               False = emme ole samalla kentällä 
#


def criminal_new_location(boolean:bool):
    cursor = mysql_connection.cursor()
    sql = "INSERT INTO criminal (location, latitude, longitude) SELECT ident, latitude_deg, longitude_deg FROM airport WHERE continent = 'EU' AND type = 'large_airport' AND airport.name LIKE '%Airport' AND ident NOT IN (SELECT location FROM criminal) ORDER BY RAND() LIMIT 1;"
    cursor.execute(sql)
    if boolean:
        cursor = mysql_connection.cursor(dictionary=True)
        sql = "SELECT latitude, longitude FROM criminal ORDER BY ID DESC LIMIT 2;"
        cursor.execute(sql)
        coordinates = cursor.fetchall()

        coord1 = (coordinates[1]["latitude"], coordinates[1]["longitude"])
        coord2 = (coordinates[0]["latitude"], coordinates[0]["longitude"])

        distanceKM = round(distance.distance(coord1, coord2).km)
        co2 = round(distanceKM * 0.15) 

        sql = f"UPDATE criminal SET km = {distanceKM}, co2 = {co2} where id = (SELECT MAX(id) FROM criminal);"
        cursor.execute(sql)

    
def criminal_timer(time: int, stop_event):
    while not stop_event.is_set():
        sleep(time)

        cursor = mysql_connection.cursor()
        sql = "INSERT INTO criminal (location, latitude, longitude) SELECT ident, latitude_deg, longitude_deg FROM airport WHERE continent = 'EU' AND type = 'large_airport' AND airport.name LIKE '%Airport' AND ident NOT IN (SELECT location FROM criminal) ORDER BY RAND() LIMIT 1;"
        cursor.execute(sql)

        cursor = mysql_connection.cursor(dictionary=True)
        sql = "SELECT latitude, longitude FROM criminal ORDER BY ID DESC LIMIT 2;"
        cursor.execute(sql)
        coordinates = cursor.fetchall()

        coord1 = (coordinates[1]["latitude"], coordinates[1]["longitude"])
        coord2 = (coordinates[0]["latitude"], coordinates[0]["longitude"])
        distanceKM = round(distance.distance(coord1, coord2).km)
        co2 = round(distanceKM * 0.15) 

        sql = f"UPDATE criminal SET km = {distanceKM}, co2 = {co2} where id = (SELECT MAX(id) FROM criminal);"
        cursor.execute(sql)



def criminal_headstart(headstart:int):
    if not mysql_connection.is_connected():
        mysql_connection.reconnect()
    cursor = mysql_connection.cursor()
    sql = "DELETE FROM criminal;" # Clears criminal table
    cursor.execute(sql)
    sql = "ALTER TABLE criminal AUTO_INCREMENT = 1;" # Resets auto increment
    cursor.execute(sql)

    for i in range(headstart+1): # adds X amount of locations to criminal table (amt. specified by difficulty) 
        criminal_new_location(bool(i))


def criminal_caught(): # check at the new airport if we are at the same airport as the criminal is (write function criminal_caught function that retuns True if we are and False if we aren't)

    cursor = mysql_connection.cursor()
    sql1 = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
    cursor.execute(sql1)
    criminal_location = cursor.fetchone()

    if type(criminal_location) == tuple:
        return False
    else:
        return True



if __name__ == "__main__": # Main block
    from game_setup import game_setup
    import multiprocessing

    game_dict = game_setup() # Setting up game parameters (screen_name, difficulty)

    manager = multiprocessing.Manager() # Manager allows multiple processeses to modify a variable
    criminal_timer_state = manager.Value('b', True) # Shared boolean to control the loop. With this the main process can stop the loop that is ran by the other process
    # Defining and starting new process for criminal_timer function
    ProcessCriminalTimer = multiprocessing.Process(target=criminal_timer, args=(criminal_timer_state, game_dict['criminal_time']))
    ProcessCriminalTimer.start()


    state = True
    while state:
        state = input(f"\nA new location is added to criminal table every {game_dict['criminal_time']} seconds. \nPress enter to quit.")

    



    # Funktion loopin boolean-arvon vaihto --> False, jotta looppi ei jää "ikuiseksi"
    criminal_timer_state.value = False
    
    # Pakotetaan prosessin lopetus multiprocessing-kirjaston terminate():lla, koska criminal_timer()-funktiossa 
    # käytetään sleep-funktiota. Ilman prosessin lopetuksen pakotusta, ns. prosessin rauhallisella lopetuksella, join():illa, 
    # prosessin funktio ajetaan loppuun ennen prosessin sulkemista, eli jos tämä prosessi lopetettaisiin join():illa, 
    # pelaaja joutuisi odottamaan jopa minuutin, kunnes rikollinen lentää seuraavalle kentälle.
    # terminate() sulkee prosessin välittömästi
    # join() odottaa prosessin päättymisen, jonka jälkeen vasta jatketaan seuraavalle riville 
    # ajamme myös joinin, jolla varmistamme että taustaprosessi sulkeutui oikein
    ProcessCriminalTimer.terminate()
    ProcessCriminalTimer.join()
    
    

    # Pelin alkaessa siis määritetään criminal_timer() -funktio ajettavaksi kirjaston avulla taustaprosessina
    # Pelin lopussa pysäytetään funktion looppi ja suljetaan taustaprosessi