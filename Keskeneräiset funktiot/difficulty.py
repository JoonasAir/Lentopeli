# Pelin vaikeustason valintaan tehty funktio. 
# Tällä hetkellä vaikeustaso muuttaa aikaa, jonka välein rikollinen lentää uudelle lentokentälle

def difficulty():
    while True:
        diff = str(input("Valitse pelin vaikeustaso. 'H' = Helppo, 'T' = Tavallinen, 'V' = Vaikea: "))
        if diff.upper() == "H":
            criminal_time = 60
            break
        elif diff.upper() == "T":
            criminal_time = 40
            break
        # X on pienemmällä ajalla testaamista varten, tämä poistetaan oikeasta pelistä
        elif diff.upper() == "X":
            criminal_time = 3
            break
        elif diff.upper() == "V":
            criminal_time = 20
            break
        else:
            print("Annoit virheellisen syötteen, koita jotain seuraavista: 'H', 'T', 'V'")
    return criminal_time
