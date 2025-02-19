from difficulty import difficulty
from time import sleep
import multiprocessing
from criminal_timer_multiprocessing import criminal_timer


# aloitusvalikko

#   1. aloita uusi peli

#   2. highscores 
#           (Tulostaa top 10 pisteet käyttäjä voi valita vaikeustason 
#           jonka parhaat tulokset tulostetaan. Pelinimi voi esiintyä 
#           vain kerran tulostetussa listassa.)        
#   3. harjoittele pelin tehtäviä
#   4. sulje peli
#   5. ?
print(1)
# uusi peli (tiedot tallennetaan tietokantaan)
#   - pelinimi
screen_name = str(input("Syötä pelinimesi: "))
print(2)
#    - pelin vaikeustason valinta
game_money, game_time, mistakes_allowed, random_luck, criminal_head_start, criminal_time = difficulty()
print(3)
#   - kysymysten tyypin valinta (matikka, fysiikka, yleiset tms.)?

#   - arvotaan pelin aloituspiste (iso lentokenttä euroopasta)
 
 
# pelin taustatarina (Y/N)
# (pelaajalle hänen halutessaan tulostetaan pelin taustatarina)


# pelaaja on saanut vihjeen että rikollinen on ollut lentokentällä X
# peli alkaa kyseiseltä lentokentältä
if __name__ == "__main__":
    print(4)
# En tiedä mitä tarkalleen tekee mutta selvitän
    try:
        manager = multiprocessing.Manager()
    except Exception as e:
        print(f"An error occurred: {e}")
    print(5)
    criminal_timer_state = manager.Value('b', True)
# Luodaan rikolliselle sanakirja, johon {criminal_time} välein lisätään arvoon +1 
# (TÄMÄ POISTETAAN JA FUNKTIOON LISÄTÄÄN TIETOKANTAA MUOKKAAVA KOMENTO)
    print(6)
    criminal_db = manager.dict({"Progress": criminal_head_start})
# Prosessin määrittely
    print(7)
    ProcessCriminalTimer = multiprocessing.Process(target=criminal_timer, args=(criminal_timer_state, criminal_db, criminal_time))
# Prosessin käynnistys
    print(8)
    ProcessCriminalTimer.start()
    print(9)

# pelaajalle aukeaa lentokentällä valikko, mitä hän voi tehdä:
#   1. käy puhumassa turvallisuuspäällikön kanssa 
#           (selvittää onko rikollinen käynyt lentoasemalla)
# 
#   2. käy WC:ssä
#           (mahdollisuus silminnäkijän tapaamiseen. 
#           Silminnäkijä voi myös huijata sinua)
#
#   3. käy kahvilla
#           (mahdollisuus silminnäkijän tapaamiseen. 
#           Silminnäkijä voi myös huijata sinua)
#
#   4. käy syömässä
#           (mahdollisuus silminnäkijän tapaamiseen. 
#           Silminnäkijä voi myös huijata sinua)
#
#   5. osta lentolippu
#           (voimme ostaa ICAO-koodilla lentolipun)
#
#   6. matkusta junalla 
#           (voimme ostaa ICAO-koodilla junaliput oikeaan määränpäähän)
# 
#   7. jäljellä oleva aika ja raha
# 
#   8. *käy palvelinhuoneessa* --> löysit johtolangan 
#           (tämä näkyy pelaajalle jos olemme käyneet 
#           puhumassa turvallisuuspäällikölle ja jos 
#           rikollinen on käynyt lentoasemalla)
#
#   9. *ratkaise johtolanka* --> tietovisakysymykset
#           (tämä näkyy pelaajalle, 
#           kun olemme käyneet palvelinhuoneessa)
#
#   8. *palaa edelliselle lentokentälle*
#           (tämä näkyy pelaajalle, jos olemme käyneet
#           puhumassa turvallisuuspäällikölle ja jos
#           rikollinen ei ole käynyt lentoasemalla)

# Peli päättyy, kun:
#   1. pääset samalle lentokentälle jossa rikollinen on
#   2. rikollinen pääsee turmelemaan X määrän lentoasemia
#   3. aika loppuu
#   4. lennät harhaan tai joudut huijatuksi liian monta kertaa



# Muutetaan criminal_timer -funktion loopin arvo --> False, jotta looppi ei jää taustalle pyörimään
    criminal_timer_state.value = False
    print(10)
# Pakotetaan taustaprosessin lopetus, sillä prosessin loopissa sleep-funktio 
# (muuten pelaaja joutuu odottamaan tässä kohtaa niin pitkään, että rikollinen lentää seuraavalle lentoasemalle)
    ProcessCriminalTimer.terminate()
    print(11)
# Varmistetaan, että taustaprosessi on päättynyt
    ProcessCriminalTimer.join()
    print(12)


# Pelin päättyessä: 
#   1. pisteet lasketaan
#   2. tulostuu pelatun pelin tilastot (pelinimi, kuinka mones pelinimellä pelattu peli, vaikeustaso, pisteet, kulunut aika, rahat alussa, kulutetut rahat, lentojen määrä, harhalentojen määrä, junamatkojen määrä, harhajunamatkojen määrä, harhajunamatkojen kilometrit, huijatuksi joutumisen kerrat)
#   3. jos kyseessä pelinimen paras pistetulos, tallennetaan tietokantaan tietokantaan kyseiselle riville tieto tästä, jos pelinimellä aikaisempia pelejä, poistetaan aikaisempi merkintä

# paluu aloitusvalikkoon