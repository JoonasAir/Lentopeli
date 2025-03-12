from game import leaderboard_update


def stop_game(game_dict:dict):


    if game_dict["criminal_caught"]: # olemme saaneet rikollisen kiinni
        print("Sait rikollisen kiinni. Voitit pelin!")
        game_dict["win_game"] = True
        return True



    elif not game_dict["game_money"] >= game_dict["flight_price"]: #rahat loppu
        print("Sinulla ei ole enää varaa lentolippuun. Hävisit pelin.")
        game_dict["win_game"] = False
        return True



    elif not game_dict["time_left_bool"]: # aika loppu
        print("Aika on loppunut. Hävisit pelin.")
        game_dict["win_game"] = False
        return True



