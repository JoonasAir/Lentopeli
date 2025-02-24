# Pelin vaikeustason valintaan tehty funktio. 
# Tällä hetkellä vaikeustaso vaikuttaa seuraaviin asioihin:
#   - pelin alussa pelaajalle annettavaan rahamäärään
#   - aikaan, jonka aikana pelaajan tulee saada rikollinen kiinni
#   - sallittu virheiden määrä
#   - random-toiminnoista saatavien hyötyjen mahdollisuus-%
#   - rikollisen etumatka pelin alussa
#   - aika, jonka välein rikollinen lentää seuraavalle lentokentälle


# Funktioon on määritelty kolme pelin vaikeustasoa: helppo, normaali ja vaikea
# Funktio palauttaa sanakirjan, jossa on vaikeustason määräämät arvot
def difficulty():
    state = True
    while state:
        difficulty_input = str(input("Valitse pelin vaikeustaso. 'H' = Helppo, 'N' = Normaali, 'V' = Vaikea: "))

        # Python tulkitsee pienet ja isot kirjaimet eri merkkeinä, esim. "h" == "H" palauttaa arvon False vaikka kirjain on sama
        # Tästä syystä käytämme if-lausekkeen ehdossa käyttäjän syötteessä .upper() -metodia ja vertaamme tätä isoon kirjaimeen
        # .upper() muuttaa merkkijonon pienet kirjaimet isoiksi 
        if difficulty_input.upper() == "H":     # Helppo vaikeustaso
            game_money = 5000       # rahat alussa
            game_time = 60*5        # peliaika sekunteina
            mistakes_allowed = 3    # kun virhemäärät ylittävät tämän, peli päättyy (agentti vaihtuu)
            random_luck = 0.05      # mahdollisuus prosenteina random-toiminnoista saataviin hyötyihin
            criminal_head_start = 2 # rikollinen on tämän verran edellä pelin alussa
            criminal_time = 60      # tämän ajan välein rikollinen lentää seuraavalle lentokentälle
            state = False           # pysäyttää tämän funktion loopin

        elif difficulty_input.upper() == "N":   # Normaali vaikeustaso
            game_money = 3500       # rahat alussa
            game_time = 60*4        # peliaika sekunteina
            mistakes_allowed = 2    # kun virhemäärät ylittävät tämän, peli päättyy (agentti vaihtuu)
            random_luck = 0.025     # mahdollisuus prosenteina random-toiminnoista saataviin hyötyihin
            criminal_head_start = 3 # rikollinen on tämän verran edellä pelin alussa
            criminal_time = 45      # tämän ajan välein rikollinen lentää seuraavalle lentokentälle
            state = False           # pysäyttää tämän funktion loopin

        elif difficulty_input.upper() == "V":   # Vaikea vaikeustaso
            game_money = 2500       # rahat alussa
            game_time = 60*3        # peliaika sekunteina
            mistakes_allowed = 0    # kun virhemäärät ylittävät tämän, peli päättyy (agentti vaihtuu)
            random_luck = 0.01      # mahdollisuus prosenteina random-toiminnoista saataviin hyötyihin
            criminal_head_start = 4 # rikollinen on tämän verran edellä pelin alussa
            criminal_time = 30      # tämän ajan välein rikollinen lentää seuraavalle lentokentälle
            state = False           # pysäyttää tämän funktion loopin

        elif difficulty_input.upper() == "X":   # Tämä "X" on tarkoitettu pelin testaamiseen, tämä poistetaan oikeasta pelistä
            game_money = 5000       # Voit muuttaa arvoja haluamallasi tavalla testatessasi pelin toimintaa
            game_time = 60*5        
            mistakes_allowed = 3    
            random_luck = 0.05     
            criminal_head_start = 2 
            criminal_time = 60      
            state = False

        else:
            print("Annoit virheellisen syötteen, koita jotain seuraavista: 'H', 'T', 'V'")

    # lisätään arvot sanakirjaan
    parameters = {
        'game_money':game_money, 
        'game_time':game_time, 
        'mistakes_allowed':mistakes_allowed, 
        'random_luck':random_luck, 
        'criminal_head_start':criminal_head_start, 
        'criminal_time':criminal_time}
    
    return parameters

# esimerkki funktion käytöstä
if __name__ == "__main__":
    game_parameters = difficulty()
    print(game_parameters)
    print(game_parameters["game_money"])