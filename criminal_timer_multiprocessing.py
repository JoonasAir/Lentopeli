from time import sleep
from difficulty import difficulty
import multiprocessing


# Määritämme tässä funktion, jolle annetaan argumenteiksi: 
#       funktion while-loopille boolean-muuttuja, jonka avulla pelin lopussa saadaan pysäytettyä looppi
#       sleep-funktiolle sekuntit integerinä, jolla määritämme, kuinka kauan rikollisella kestää tehdä tuhotyöt ja lentää seuraavaan paikkaan
# Funktio muuttaa tietokannan criminal-taulua x ajan välein
def criminal_timer(criminal_timer_state:bool, time:int):
    while criminal_timer_state.value:
        sleep(time)
        if criminal_timer_state.value:
            pass # TIETOKANNAN CRIMINAL-TAULUN MUOKKAUSKOMENTO


# Käyttäessämme multiprocessing-kirjastoa kirjoitamme koodin main blockkiin, sillä käytämme multiprocessing-kirjastoa. 
# (Importit ja funktioiden määritykset tehdään ennen main blockia)
# Aina uuden multiprocessing-prosessin käynnistyessä tämä uusi prosessi suorittaa koodin ensimmäisestä rivistä lähtien, 
# jotta saa tarvittavat importit ja funktiot muistiinsa. Jotta vältymme ylimääräisiltä, esim. tulostuksilta, 
# kirjoitamme print-funktion main-blockin sisään ja näin tämä tulostus tapahtuu vain pääprosessin toimesta. 
# (multiprocessing-prosessin __name__ on "__mp_main__") 
if __name__ == "__main__":
    # Määritetään sekuntit, jonka välein rikollinen lentää seuraavalle asemalle (vaikeustason mukaan)
    game_money, game_time, mistakes_allowed, random_luck, criminal_head_start, criminal_time = difficulty()
    # Managerin avulla saamme tiedon liikkumaan prosessien välillä (kun pääohjelmasta muutamme criminal_timer_state -> False niin taustaprosessin looppi sulkeutuu)
    manager = multiprocessing.Manager()
    # Funktion loopin boolean-arvo. Edellisessä kommentissa kerrottu miksei voida käyttää helpompaa "criminal_timer_state = True" -tapaa tämän määrittämiseen
    criminal_timer_state = manager.Value('b', True)
    # Prosessin määrittely
    ProcessCriminalTimer = multiprocessing.Process(target=criminal_timer, args=(criminal_timer_state, criminal_time))
    # Prosessin käynnistys
    ProcessCriminalTimer.start()

    # Tässä kohdassa voimme ajaa mitä vain koodia samaan aikaan, kun taustaprosessina criminal_timer() -funktion looppi vuorotellen: 
    #       odottaa 5 sekuntia
    #       lennättää rikollisen seuraavalle lentokentälle






    # Funktion loopin boolean-arvon vaihto --> False, jotta looppi ei jää "ikuiseksi"
    criminal_timer_state.value = False
    
    # Pakotetaan prosessin lopetus multiprocessing-kirjaston terminate():lla, koska kyseisen prosessin ajamassa criminal_timer()-funktiossa 
    # käytetään sleep-funktiota. Ilman prosessin lopetuksen pakotusta, ns. prosessin rauhallisella lopetuksella, join():illa, 
    # prosessin funktio ajetaan loppuun ennen prosessin sulkemista, eli jos kyseinen prosessi lopetettaisiin join():illa, 
    # pelaaja voisi joutua odottamaan jopa minuutin niin, ettei voi tehdä pelissä mitään. 
    # terminate() sulkee prosessin välittömästi
    # join() odottaa prosessin päättymisen, jonka jälkeen vasta jatketaan seuraavalle riville 
    # ajamme myös joinin, jolla varmistamme että taustaprosessi sulkeutui 
    ProcessCriminalTimer.terminate()
    ProcessCriminalTimer.join()
    

    # Pelin alkaessa siis importataan multiprocessing-kirjasto ja määritetään criminal_timer() -funktio ajettavaksi kirjaston avulla taustaprosessina
    # Pelin lopussa pysäytetään funktion looppi ja suljetaan taustaprosessi 

    # Täytyy miettiä yhdessä, että kun saavumme lentokentälle, jossa rikollinen on, voiko hän enää lentää seuraavalle kentälle sillä aikaa, kun käymme kysymässä turvallisuuspäälliköltä rikollisesta 

