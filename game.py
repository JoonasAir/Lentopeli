from difficulty import difficulty
from time import sleep
import multiprocessing
from criminal_timer_multiprocessing import criminal_timer

# Käyttäessämme multiprocessing-kirjastoa kirjoitamme koodin main blockkiin, sillä käytämme multiprocessing-kirjastoa. 
# (Importit ja funktioiden määritykset tehdään ennen main blockia)
# Aina uuden multiprocessing-prosessin käynnistyessä tämä uusi prosessi suorittaa koodin ensimmäisestä rivistä lähtien, 
# jotta saa tarvittavat importit ja funktiot muistiinsa. Jotta vältymme ylimääräisiltä, esim. tulostuksilta, 
# kirjoitamme print-funktion main-blockin sisään ja näin tämä tulostus tapahtuu vain pääprosessin toimesta. 
# (multiprocessing-prosessin __name__ on "__mp_main__") 
if __name__ == "__main__":
# aloitusvalikko

#   1. aloita uusi peli

#   2. highscores 
#           (Tulostaa top 10 pisteet käyttäjä voi valita vaikeustason 
#           jonka parhaat tulokset tulostetaan. Pelinimi voi esiintyä 
#           vain kerran tulostetussa listassa.)        
#   3. harjoittele pelin tehtäviä
#   4. sulje peli


# uusi peli (tiedot tallennetaan tietokantaan)
#   - pelinimi
    screen_name = str(input("Syötä pelinimesi: "))
#    - pelin vaikeustason valinta
    game_money, game_time, mistakes_allowed, random_luck, criminal_head_start, criminal_time = difficulty()
#   - kysymysten tyypin valinta (matikka, fysiikka, yleiset tms.)?

#   - arvotaan pelin aloituspiste (iso lentokenttä euroopasta)
 
 
# pelin taustatarina (Y/N)
# (pelaajalle hänen halutessaan tulostetaan pelin taustatarina)


# pelaaja on saanut vihjeen että rikollinen on ollut lentokentällä X
# peli alkaa kyseiseltä lentokentältä


    # Managerin avulla saamme tiedon liikkumaan prosessien välillä (kun pääohjelmasta muutamme criminal_timer_state -> False niin taustaprosessin looppi sulkeutuu)
    manager = multiprocessing.Manager()
    # Funktion loopin boolean-arvo. Edellisessä kommentissa kerrottu miksei voida käyttää helpompaa "criminal_timer_state = True" -tapaa tämän määrittämiseen
    criminal_timer_state = manager.Value('b', True)
    # Prosessin määrittely
    ProcessCriminalTimer = multiprocessing.Process(target=criminal_timer, args=(criminal_timer_state, criminal_time))
    # Prosessin käynnistys
    ProcessCriminalTimer.start()


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
    # Pakotetaan taustaprosessin lopetus, sillä prosessin loopissa sleep-funktio 
    # (muuten pelaaja joutuu odottamaan tässä kohtaa niin pitkään, että rikollinen lentää seuraavalle lentoasemalle)
    ProcessCriminalTimer.terminate()
    # Varmistetaan, että taustaprosessi on päättynyt
    ProcessCriminalTimer.join()


# Pelin päättyessä: 
#   1. pisteet lasketaan
#   2. tulostuu pelatun pelin tilastot (pelinimi, kuinka mones pelinimellä pelattu peli, vaikeustaso, pisteet, kulunut aika, rahat alussa, kulutetut rahat, lentojen määrä, harhalentojen määrä, junamatkojen määrä, harhajunamatkojen määrä, harhajunamatkojen kilometrit, huijatuksi joutumisen kerrat)
#   3. jos kyseessä pelinimen paras pistetulos, tallennetaan tietokantaan tietokantaan kyseiselle riville tieto tästä, jos pelinimellä aikaisempia pelejä, poistetaan aikaisempi merkintä

# paluu aloitusvalikkoon