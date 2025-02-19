# Pelin vaikeustason valintaan tehty funktio. 
# Tällä hetkellä vaikeustaso vaikuttaa seuraaviin asioihin:
#   - pelin alussa pelaajalle annettavaan rahamäärään
#   - aikaan, jonka aikana pelaajan tulee saada rikollinen kiinni
#   - sallittu virheiden määrä
#   - random-toiminnoista saatavien hyötyjen mahdollisuus-%
#   - rikollisen etumatka pelin alussa
#   - aika, jonka välein rikollinen lentää seuraavalle lentokentälle


# Funktioon on määritelty kolme pelin vaikeustasoa: helppo, normaali ja vaikea
# Näiden lisäksi funktioon on määritelty ylimääräinen vaikeustaso "X", 
# joka on tarkoitettu pelin testaamiseen. Arvoja saa muuttaa mielensä mukaan peliä testatessa, tämä poistetaan varsinaisesta pelistä
def difficulty():
    while True:
        diff = str(input("Valitse pelin vaikeustaso. 'H' = Helppo, 'N' = Normaali, 'V' = Vaikea: "))

        if diff.upper() == "H":     # Helppo vaikeustaso
            game_money = 5000       # rahat alussa
            game_time = 60*5        # peliaika sekunteina
            mistakes_allowed = 3    # kun virhemäärät ylittävät tämän, peli päättyy (agentti vaihtuu)
            random_luck = 0.05      # mahdollisuus prosenteina random-toiminnoista saataviin hyötyihin
            criminal_head_start = 2 # rikollinen on tämän verran edellä pelin alussa
            criminal_time = 60      # tämän ajan välein rikollinen lentää seuraavalle lentokentälle
            break

        elif diff.upper() == "N":   # Normaali vaikeustaso
            game_money = 3500       # rahat alussa
            game_time = 60*4        # peliaika sekunteina
            mistakes_allowed = 2    # kun virhemäärät ylittävät tämän, peli päättyy (agentti vaihtuu)
            random_luck = 0.025     # mahdollisuus prosenteina random-toiminnoista saataviin hyötyihin
            criminal_head_start = 3 # rikollinen on tämän verran edellä pelin alussa
            criminal_time = 45      # tämän ajan välein rikollinen lentää seuraavalle lentokentälle
            break

        elif diff.upper() == "V":   # Vaikea vaikeustaso
            game_money = 2500       # rahat alussa
            game_time = 60*3        # peliaika sekunteina
            mistakes_allowed = 0    # kun virhemäärät ylittävät tämän, peli päättyy (agentti vaihtuu)
            random_luck = 0.01      # mahdollisuus prosenteina random-toiminnoista saataviin hyötyihin
            criminal_head_start = 4 # rikollinen on tämän verran edellä pelin alussa
            criminal_time = 30      # tämän ajan välein rikollinen lentää seuraavalle lentokentälle
            break

        elif diff.upper() == "X":   # Tämä "X" on tarkoitettu pelin testaamiseen, tämä poistetaan oikeasta pelistä
            game_money = 5000       # Voit muuttaa arvoja haluamallasi tavalla testatessasi pelin toimintaa
            game_time = 60*5        
            mistakes_allowed = 3    
            random_luck = 0.05     
            criminal_head_start = 2 
            criminal_time = 60      
            break

        else:
            print("Annoit virheellisen syötteen, koita jotain seuraavista: 'H', 'T', 'V'")

    return game_money, game_time, mistakes_allowed, random_luck, criminal_head_start, criminal_time
