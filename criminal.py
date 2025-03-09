from time import sleep
<<<<<<< HEAD
from config import mysql_connection
=======
from db.config import mysql_connection
>>>>>>> 23d876f1ffd08933d76517dedd4cc7982dd746ba

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


def criminal_new_location():
    sql = "INSERT INTO criminal (location) SELECT ident FROM airport WHERE continent = 'EU' AND type = 'large_airport' AND ident NOT IN (SELECT location FROM criminal) ORDER BY RAND() LIMIT 1;"
    cursor = mysql_connection.cursor()
    cursor.execute(sql)
    
    
def criminal_timer(criminal_timer_state: bool, time: int):
    while criminal_timer_state.value:
        sleep(time)
        if criminal_timer_state.value:
            criminal_new_location()


def criminal_headstart(headstart:int):
    cursor = mysql_connection.cursor()
    sql = "DELETE FROM criminal;" # Clears criminal table
    cursor.execute(sql)
    sql = "ALTER TABLE criminal AUTO_INCREMENT = 1;" # Resets auto increment
    cursor.execute(sql)

    for i in range(headstart+1): # adds X amount of locations to criminal table (amt. specified by difficulty) 
        criminal_new_location()


def criminal_caught(player_location):
    pass


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
        state = input(f"\nA new location is added to criminal table every {game_dict["criminal_time"]} seconds. \nPress enter to quit.")

    



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