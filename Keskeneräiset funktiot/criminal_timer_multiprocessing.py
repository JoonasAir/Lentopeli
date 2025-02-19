from time import sleep
import multiprocessing

# Käytämme: 
#       multiprocessing-kirjastoa, jonka avulla saamme rikollisen ajastimen juoksemaan taustalla
#       sleep-funktiota time-kirjastosta, jolla saamme



# Tässä esimerkissä pelin alussa rikollinen on kolme lentokenttää pelaajaa edellä ja viiden sekunnin välein rikollinen edistyy yhden kentän eteenpäin.
# Sanakirjan päivittäminen voidaan korvata myöhemmin tietokannan päivittämisellä, jossa on tiedot rikollisen edistymisestä.
# Tämän esimerkin mukaan: 
#       pelin alussa tietokannan rikollinen-tauluun lisätään kolme riviä 
#       viiden sekunnin välein tietokantaan lisätään uusi rivi
# Tietokannan rikollinen-taulu sisältää ainakin seuraavat tiedot:
#       ID --> ensimmäinen rivi tietokannassa = rikollisen ensimäinen lentoasema = ID 1
#       ICAO-koodi --> arvotaan airport-taulusta euroopan isoista lentoasemista

# Määritämme tässä funktion, jolle annetaan argumenteiksi: 
#       funktion while-loopille boolean-arvo, jonka avulla pelin lopussa saadaan pysäytettyä looppi
#       sanakirja, johon päivitetään rikollisen edistyminen pelissä. 
#       sleep-funktiolle sekuntit integerinä, jolla määritämme, kuinka kauan rikollisella kestää tehdä tuhotyöt ja lentää seuraavaan paikkaan
def criminal_timer(state:bool, criminal_db:dict, time:int):
    while state.value:
        sleep(time)
        if state.value:
            criminal_db["Airport"] += 1
            # Tulostetaan jokaisen muutoksen jälkeen rikollisen edistyminen
            print("\nTulostus criminal_timer() -funktion loopista: Rikollisen edistyminen: ", criminal_db["Airport"])

# Käyttäessämme multiprocessing-kirjastoa, täytyy se tehdä main-blockin sisältä, en tiedä miksi, selvitän tämän
if __name__ == "__main__":
    # Määritetään sekuntit, jonka välein rikollinen lentää aina seuraavalle asemalle (vaikeustason mukaan?)
    criminal_time = int(5)
    # En tiedä mitä tarkalleen tekee mutta selvitän
    manager = multiprocessing.Manager()
    # Funktion loopin boolean-arvo, selvitän vielä miksi täytyy määrittää näin, eikä voida käyttää helpompaa "state = True" -tapaa
    state = manager.Value('b', True)
    # Luodaan rikolliselle sanakirja (pelissä käytetään tietokantaa), johon muutetaan taustalla ajettavan funktion avulla rikollisen edistyminen 
    criminal_db = manager.dict({"Airport": 3})
    # Prosessin määrittely
    ProcessCriminalTimer = multiprocessing.Process(target=criminal_timer, args=(state, criminal_db, criminal_time))
    # Prosessin käynnistys
    ProcessCriminalTimer.start()

    # Tässä kohdassa voimme ajaa mitä vain koodia samaan aikaan, kun taustaprosessina criminal_timer() -funktion looppi vuorotellen: 
    #       odottaa 5 sekuntia
    #       lennättää rikollisen seuraavalle lentokentälle


    # Enteriä painamalla tulostetaan rikollisen edistys ja syöttämällä arvoksi 'c', pysäytetään tämä looppi 
    ip = "q"
    while ip != "c":
        print("\nTulostus pääohjelman loopista: Rikollisen edistyminen: ", criminal_db["Airport"])
        ip = str(input("\nPaina enter saadaksesi rikollisen edistymisen tietoosi\nSyötä 'c' päättääksesi ohjelman: "))
    

    # Funktion loopin boolean-arvon vaihto --> False, jotta looppi ei jää "ikuiseksi"
    state.value = False
    
    # Pakotetaan prosessin lopetus multiprocessing-kirjaston terminate():lla, koska kyseisen prosessin ajamassa criminal_timer()-funktiossa 
    # käytetään sleep-funktiota. Ilman prosessin lopetuksen pakotusta, ns. prosessin rauhallisella lopetuksella, join():illa, 
    # prosessin funktio ajetaan loppuun ennen prosessin sulkemista, eli jos kyseinen prosessi lopetettaisiin join():illa, 
    # pelaaja voisi joutua odottamaan jopa minuutin niin, ettei voi tehdä pelissä mitään. 
    # terminate() sulkee prosessin välittömästi
    # join() odottaa prosessin päättymisen, jonka jälkeen vasta jatketaan seuraavalle riville 
    # ajamme myös joinin, jolla varmistamme että taustaprosessi sulkeutui 
    ProcessCriminalTimer.terminate()
    ProcessCriminalTimer.join()
    
    # Sanakirjan "Airport"-avaimen arvon tulostus, jolla varmistetaan taustaprosessina pyörineen funktion toimivuus
    print("\nTulostus lopussa: Rikollisen edistyminen: ", criminal_db["Airport"])


    # Pelin alkaessa siis importataan multiprocessing-kirjasto ja määritetään criminal_timer() -funktio ajettavaksi kirjaston avulla taustaprosessina
    # Pelin lopussa pysäytetään funktion looppi ja suljetaan taustaprosessi 

    # Täytyy miettiä yhdessä, että kun saavumme lentokentälle, jossa rikollinen on, voiko hän enää lentää seuraavalle kentälle sillä aikaa, kun käymme kysymässä turvallisuuspäälliköltä rikollisesta 

