def stop_game(game_dict:dict):


    if game_dict["criminal_caught"]: # olemme saaneet rikollisen kiinni
        print("Saat rikollisen kiinni. Voitit pelin! Peli päättyy!")
        return True



    elif not game_dict["game_money"] >= game_dict["flight_price"]: #rahat loppu
        print("Sinulla ei ole enää varaa lentolippuun. Hävisit pelin.")
        return True



    elif not game_dict["time_left_bool"]: # aika loppu
        print("Aika on loppunut. Hävisit pelin")
        return True



