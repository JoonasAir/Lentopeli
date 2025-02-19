

# aloitusvalikko
#   1. aloita uusi peli
#   2. highscores 
#           (Tulostaa top 10 pisteet käyttäjä voi valita vaikeustason 
#           jonka parhaat tulokset tulostetaan. Pelinimi voi esiintyä 
#           vain kerran tulostetussa listassa.)        
#   3. harjoittele pelin tehtäviä
#   4. sulje peli
#   5. ?

# uusi_peli (tiedot tallennetaan tietokantaan)
#   - pelinimi
#   - pelin vaikeustason valinta, vaikeustaso määrää:
#       - pelaajan rahat
#       - aika löytää rikollinen
#       - kuinka monta virhettä sallitaan
#       - randomtoiminnoista saatavien hyötyjen (silminnäkijä WC:ssä) 
#         mahdollisuus kasvaa helpolla ja pienenee vaikealla vaikeustasolla
#       - rikollinen on X lentoasemaa pelaajaa edellä pelin alussa
#   - kysymysten tyypin valinta (matikka, fysiikka, yleiset tms.)?
#   - arvotaan pelin aloituspiste (iso lentokenttä euroopasta)
 
# pelin taustatarina (Y/N)
# (pelaajalle hänen halutessaan tulostetaan pelin taustatarina)


# pelaaja on saanut vihjeen että rikollinen on ollut lentokentällä X
# peli alkaa kyseiseltä lentokentältä

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
 
# Pelin päättyessä: 
#   1. pisteet lasketaan
#   2. tulostuu pelatun pelin tilastot (pelinimi, kuinka mones pelinimellä pelattu peli, vaikeustaso, pisteet, kulunut aika, rahat alussa, kulutetut rahat, lentojen määrä, harhalentojen määrä, junamatkojen määrä, harhajunamatkojen määrä, harhajunamatkojen kilometrit, huijatuksi joutumisen kerrat)
#   3. jos kyseessä pelinimen paras pistetulos, tallennetaan tietokantaan tietokantaan kyseiselle riville tieto tästä, jos pelinimellä aikaisempia pelejä, poistetaan aikaisempi merkintä

# paluu aloitusvalikkoon