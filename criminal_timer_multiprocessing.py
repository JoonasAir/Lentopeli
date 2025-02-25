from time import sleep
from difficulty import difficulty
import multiprocessing


# Määritämme tässä funktion, jolle annetaan argumenteiksi: 
#       funktion while-loopille boolean-muuttuja, jonka avulla pelin lopussa saadaan pysäytettyä looppi
#       sleep-funktiolle sekuntit, jolla määritämme, kuinka kauan rikollinen viipyy lentoasemalla ennen kun lentää seuraavaan
# Funktio lisää tietokannan criminal-tauluun X ajan välein uuden lentoaseman


####################### MUOKKAUS KESKEN #############################
def criminal_timer(criminal_timer_state:bool, time:int, criminal_locations:list):
    while criminal_timer_state.value:
        sleep(time)
        if criminal_timer_state.value:
            ICAO = 0 # TIETOKANNAN AIRPORT-TAULUSTA ICAO-KOODI
            criminal_locations.append(ICAO)
    return criminal_locations


# Käyttäessämme multiprocessing-kirjastoa kirjoitamme koodin main blockkiin 
# (poislukien Importit ja funktioiden määritykset, jotka tehdään ennen main blockia)
# Aina uuden multiprocessing-prosessin käynnistyessä tämä uusi prosessi suorittaa
# tiedostomme ensimmäisestä rivistä lähtien, jotta saa tarvittavat importit ja funktiot muistiinsa. 
# Jotta vältymme sotkulta (siltä, että kaikki rivit suoritetaan kaikkien prosessien toimesta)
# kirjoitamme main-blockin sisään koodin suoritukset ja 
# ennen main-blockkia vain importit ja funktioiden määritykset
# multiprocessing-prosessin __name__ on "__mp_main__" 
# tästä syystä seuraavaa if-lauseketta (eli main blockia) ei suoriteta multiprosessien toimesta

if __name__ == "__main__": # Main block
    game_parameters = difficulty() # Pelin määrittely

    # Managerin avulla saamme tiedon liikkumaan prosessien välillä. Kun pääohjelmasta muutamme criminal_timer_state.value -> False niin taustaprosessin looppi sulkeutuu
    manager = multiprocessing.Manager()
    # Funktion loopin boolean-arvo. Edellisessä kommentissa kerrottu miksei voida käyttää helpompaa "criminal_timer_state = True" -tapaa tämän määrittämiseen
    criminal_timer_state = manager.Value('b', True)
    # Prosessin määrittely
    ProcessCriminalTimer = multiprocessing.Process(target=criminal_timer, args=(criminal_timer_state, game_parameters['criminal_time']))
    # Prosessin käynnistys
    ProcessCriminalTimer.start()



    # Tässä kohdassa voimme ajaa mitä vain koodia samaan aikaan, 
    # kun criminal_timer() -funktion looppi pyörii taustaprosessina 
    print(game_parameters)
    print(game_parameters['criminal_time'])



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