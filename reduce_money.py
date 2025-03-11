
def reduce_money(game_dict):

    flight_cost = game_dict["flight_price"]

#Tarkistaa käyttäjän rahaa
    if game_dict["game_money"] < flight_cost:
       print("You don't have enough money to buy a ticket. Game over!")
       return game_dict

#Vähentää lentolipun hinta
    game_dict["game_money"] = game_dict["game_money"] - game_dict["flight_price"]

#Näyttää kuinka paljon rahaa on vielä jäljellä
    print(f"You took a flight. Remaining money: {game_dict['game_money']}€.")

    return game_dict

if __name__ == "__main__":
    from game_setup import game_setup
    from game_parameters import game_parameters
    game_dict = game_setup(game_parameters)

    reduce_money(game_dict)
    reduce_money(game_dict)
