from random import randint
from game_setup import game_setup
from mysql_connection import mysql_connection
from colorama import Fore, Style


# you're in X country at X airport
# t - time



def airport_menu(game_dict:dict):
    airport_actions = [
        "Check remaining money",
        "Talk to airport's security chief", 
        "Solve the clue",                       # visible if we've talked to security chief and the criminal has been at the airport
        "Try to solve the previous clue again", # visible if we gave wrong ansver in quiz -> we came to wrong airport and we have talked to security chief to find out that the criminal has not been here
        "Buy a flight ticket",                  # visible after solving a clue
        ]
    random_actions = [
        ("Visit the restroom",      "you got lucky",    "you went to restroom and feel better"),
        ("Go to get a cup coffee",  "you got lucky",    "you went to restroom and feel better"),
        ("Go to get a meal",        "you got lucky",    "you went to restroom and feel better"),
        ("Go to relax in a lounge", "you got lucky",    "you went to restroom and feel better"),
        ]
    random_index = randint(0, len(random_actions)-1)
    menu = "\nAIRPORT MENU\n\nChoose your action from following options:\n"
    menu += f"    1 - {airport_actions[0]}\n"               # Check remaining time and money
    menu += f"    2 - {random_actions[random_index][0]}\n"  # Randomly picked action from random_actions
    menu += f"    3 - {airport_actions[1]}\n"               # Talk to airport's security chief

# visible if we've talked to security chief and the criminal has been at the airport
    if game_dict["talk_to_chief"] and game_dict['criminal_was_here']: 
        menu += f"    4 - {airport_actions[2]}\n"           # Solve the clue

# visible if we gave wrong ansver in quiz -> we came to wrong airport and we have talked to security chief to find out that the criminal has not been here
    if game_dict["previous_quiz_answer"] == False and game_dict["talk_to_chief"]:
        menu += f"    4 - {airport_actions[3]}\n"           # Try to solve the previous clue again

# visible after solving a clue
    elif game_dict["got_location"]:
        menu += f"    4 - {airport_actions[4]}\n"           # Buy a flight ticket


    user_input = int(input(menu + "Input: "))
    print()
    return game_dict, user_input, random_actions[random_index]





def airport_actions(game_dict:dict):
    game_dict, user_input, random_action = airport_menu(game_dict)
    cursor = mysql_connection.cursor()



    while user_input != 0:
        luck = bool(randint(0,100)/100 <= game_dict["random_luck"]) # check if we are lucky on this iteration of the loop or not. Based on variable random_luck defined on game_setup()
        

        if user_input == 1 : # Check remaining time and money
            print(Fore.RED + f"\nYou have {game_dict['game_money']}€ left to spend. \n" + Style.RESET_ALL)
    


        elif user_input == 2: # Randomly picked action from random_actions
            print(Fore.RED + f"\nYou chose to {random_action[0].lower()}." + Style.RESET_ALL)

            if luck:
                game_dict["got_location"] = True
                sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
                cursor.execute(sql)
                result = cursor.fetchone()[0]
                print(Fore.RED + f"{random_action[1]}" + Style.RESET_ALL)
                print(Fore.RED + f"The fight ICAO-code is: {result}\n" + Style.RESET_ALL)

            else:
                print(Fore.RED + f"{random_action[2]}\n" + Style.RESET_ALL)



        #TODO Figure out why not working
        elif user_input == 3: # Talk to airport's security chief

            if game_dict["talk_to_chief"] == False: # If we haven't talked to the security chief yet at current airport
                game_dict["talk_to_chief"] = True
                sql = "SELECT location FROM criminal WHERE visited = 1 ORDER BY ID DESC LIMIT 1;" 
                cursor.execute(sql)
                result = cursor.fetchone()

                if game_dict["player_location"] == result[0]: # If our location equals to the last of the visited locations in criminal-table
                    print(Fore.RED + f"\nSecurity chief's monitows were down due to the criminal's attack.\nStill he had a clue about criminal for you. Try to solve it\n" + Style.RESET_ALL)
                    game_dict["criminal_was_here"] = True

                else:
                    print(Fore.RED + f"\nSecurity chief told you the criminal haven't been at the airport. Try to solve last clue again.\n" + Style.RESET_ALL)
                    game_dict["criminal_was_here"] = False



            elif luck and game_dict["criminal_was_here"]: # If criminal have been here and we got lucky
                game_dict["got_location"] = True
                sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
                cursor.execute(sql)
                result = cursor.fetchone()
                result = result[0][0]
                print(Fore.RED + f"\n{result}" + Style.RESET_ALL)
                print(Fore.RED + f"\nThe chief had just found the country where the criminal headed from here!" + Style.RESET_ALL)
                print(Fore.RED + f"\nThe fight ICAO-code is: {result}" + Style.RESET_ALL)



            elif game_dict["criminal_was_here"]:
                pass


            else:
                print(Fore.RED + f"\nThe chief had nothing new to tell you. He was still on a mission to recover his monitors from the attack of the criminal." + Style.RESET_ALL)
            


        elif user_input == 4 and game_dict["got_location"]: # Buy a flight ticket
            print(Fore.RED + f"\nBuy a flight ticket" + Style.RESET_ALL)
    
            # reset helper parameters to default value
            game_dict['talk_to_chief'] = False,
            game_dict['previous_quiz_answer'] = bool,
            game_dict['got_location'] = False,
            game_dict['criminal_was_here'] = bool,



        elif user_input == 4 and game_dict["talk_to_chief"] and game_dict["criminal_was_here"]: # Solve the clue
            print(Fore.RED + f"\nSolve the clue" + Style.RESET_ALL)
            
            # quiz here


        elif user_input == 4 and game_dict["talk_to_chief"] and not game_dict["criminal_was_here"]: # Try to solve the previous clue again
            print(Fore.RED + f"\nTry to solve the previous clue again" + Style.RESET_ALL)



        


        game_dict, user_input, random_action = airport_menu(game_dict)

    return game_dict
            
    
    

if __name__ == "__main__":
    # define game_dict
    game_dict = game_setup()

    airport_actions(game_dict)
