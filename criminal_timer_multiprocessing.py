from time import sleep
from game_setup import game_setup
import multiprocessing
import mysql.connector

# Setting up a connection to our database
connection = mysql.connector.connect(
    collation = "utf8mb4_general_ci",
    host = '127.0.0.1',
    port = 3306,
    database = "flight_game",
    user = "python",
    password = "koulu123",
    autocommit = True
)


# Here we define a function that adds a new airport to the criminal table in the database at intervals of X time
# Thwe function takes the following arguments:
#       1. criminal_timer_state - a boolean variable for the function's while-loop, which allows us to stop the loop at the end of the game
#       2. time - seconds for the sleep function, which determines how long the criminal stays at the airport before flying to the next one
def criminal_new_location():
    sql = "INSERT INTO criminal (location) SELECT ident FROM airport WHERE continent = 'EU' AND type = 'large_airport' AND ident NOT IN (SELECT location FROM criminal) ORDER BY RAND() LIMIT 1;"
    cursor = connection.cursor()
    cursor.execute(sql)
    
def criminal_timer(criminal_timer_state: bool, time: int):
#    sql = "INSERT INTO criminal (location) SELECT ident FROM airport WHERE continent = 'EU' AND type = 'large_airport' AND ident NOT IN (SELECT location FROM criminal) ORDER BY RAND() LIMIT 1;"
#    cursor = connection.cursor()
    while criminal_timer_state.value:
        sleep(time)
        if criminal_timer_state.value:
            criminal_new_location()
#            cursor.execute(sql)



# When using the multiprocessing library, we write the code inside the main block
#   (excluding imports and function definitions, which are done before the main block).
# Every time a new multiprocessing process starts, this new process executes,
#   our file from the first line to get the necessary variables, imports and functions into it's memory.
# To avoid confusion (so that all lines are not executed by all processes),
#   we write the code execution inside the main block and
#   only imports and function definitions before the main block.
# The __name__ of the multiprocessing process is "__mp_main__"
#   for this reason, the following if statement (main block) is not executed by the subprocesses.

if __name__ == "__main__": # Main block
    game_dict = game_setup() # Setting up game parameters (screen_name, difficulty)

    manager = multiprocessing.Manager() # Manager allows multiple processeses to modify a variable
    criminal_timer_state = manager.Value('b', True) # Shared boolean to control the loop. With this the main process can stop the loop that is ran by the other process
    # Defining and starting new process for criminal_timer function
    ProcessCriminalTimer = multiprocessing.Process(target=criminal_timer, args=(criminal_timer_state, game_dict['criminal_time']))
    ProcessCriminalTimer.start()


    state = True
    while state:
        state = input(": ")




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