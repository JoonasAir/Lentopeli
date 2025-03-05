from random import randint
from game_setup import game_setup
from mysql_connection import mysql_connection
from colorama import Fore, Style

from security import security


# you're in X country at X airport
# t - time



def airport_menu_input(game_dict:dict):
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





def airport_action(game_dict, user_input, random_action):
    cursor = mysql_connection.cursor()
    luck = bool(randint(0,100)/100 <= game_dict["random_luck"]) # check if we are lucky. Based on variable random_luck defined on game_setup()
    
    while True: # break out from loop when we fly to next location
        
        # Print remaining time and money
        if user_input == 1 : 
            print(Fore.RED + f"\nYou have {game_dict['game_money']}€ left to spend. \n" + Style.RESET_ALL)


        # Randomly picked action from random_actions
        elif user_input == 2: 
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


        # Talk to airport's security chief
        elif user_input == 3: 
            game_dict = security(game_dict, luck)
            



        # Buy a flight ticket
        elif user_input == 4 and game_dict["got_location"]: # If user input is 4 and we got the location (from quiz or eyewitness)
            print(Fore.RED + f"\nBuy a flight ticket" + Style.RESET_ALL)


            break # endless loop ends here


        # Solve the clue
        elif user_input == 4 and game_dict["talk_to_chief"] and game_dict["criminal_was_here"]: # If input = 4 AND we have talked to the chief AND he told that the criminal have been here
            print(Fore.RED + f"\nSolve the clue" + Style.RESET_ALL)



        # Try to solve the previous clue again
        elif user_input == 4 and game_dict["talk_to_chief"] and not game_dict["criminal_was_here"]: # If input = 4 AND we talked to chief AND he told that the criminal haven't been here
            print(Fore.RED + f"\nTry to solve the previous clue again" + Style.RESET_ALL)



    return game_dict
            
    
    

if __name__ == "__main__":
    # define game_dict
    game_dict = game_setup()

    airport_action(game_dict)
