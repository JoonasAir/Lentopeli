from random import randint
from mysql_connection import mysql_connection
from colorama import Fore, Style
from quiz_icao import quiz_icao
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
        ("Visit the restroom",      "you got lucky",    "You went to restroom and now feel better.", "You already went to the restroom."),
        ("Go to get a cup coffee",  "you got lucky",    "You went to get a large cup of coffee and now feel more energized.", "Maybe it's better not to get a second cup of coffee."),
        ("Go to get a meal",        "you got lucky",    "You went to grab a hamburger meal and now feel better. ", "You already went to Mc'Donalds. You're not hungry."),
        ("Go to relax in a lounge", "you got lucky",    "You went to lounge to rest for a moment. You're not tired anymore and are able to focus on hasing the criminal."),
        ]
    random_index = randint(0, len(random_actions)-1)
    menu = "\nAIRPORT MENU\n\nChoose your action from following options:\n"
    menu += f"    1 - {airport_actions[0]}\n"               # Check remaining time and money
    menu += f"    2 - {random_actions[random_index][0]}\n"  # Randomly picked action from random_actions
    menu += f"    3 - {airport_actions[1]}\n"               # Talk to airport's security chief

    # Solve the clue
    if game_dict["talk_to_chief"] and game_dict['criminal_was_here'] and game_dict["clue_solved"] != True and game_dict["next_location"] == "": # visible IF we've talked to security chief AND the criminal has been at the airport AND we haven't solved the clue yet AND we don't know next location
        menu += f"    4 - {airport_actions[2]}\n"

    # Try to solve the previous clue again
    if game_dict["talk_to_chief"] and not game_dict["criminal_was_here"] and game_dict["clue_solved"] != True and game_dict["next_location"] == "": # visible IF we've talked to security chief AND the criminal has NOT been at the airport AND we haven't solved the clue yet AND we don't know next location
        menu += f"    4 - {airport_actions[3]}\n"           

    # Buy a flight ticket
    elif game_dict["next_location"] != "": # visible IF we got the location (from quiz or with luck)
        menu += f"    4 - {airport_actions[4]}\n"


    user_input = int(input(menu + "Input: "))
    print()
    return game_dict, user_input, random_actions[random_index]





def airport_menu(game_dict):

    cursor = mysql_connection.cursor()
    luck = bool(randint(0,1000000)/1000000 <= game_dict["random_luck"]) # check if we are lucky. Based on variable random_luck defined on game_setup()

    while True: # break out from loop when we fly to next location

        game_dict, user_input, random_action = airport_menu_input(game_dict) # ask what user wants to do at the airport

        # Print remaining time and money
        if user_input == 1 : 
            print(Fore.RED + f"\nYou have {game_dict['game_money']}€ left to spend. \n" + Style.RESET_ALL)


        # Randomly picked action from random_actions
        elif user_input == 2:
            if game_dict["tried_luck"]:
                print(Fore.RED + f"\n{random_action[3]}" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"\nYou chose to {random_action[0].lower()}.\n" + Style.RESET_ALL)
                game_dict["tried_luck"] = True
                if luck:
                    game_dict["got_location"] = True
                    sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
                    cursor.execute(sql)
                    result = cursor.fetchone()[0]
                    game_dict["next_location"] = result
                    print(Fore.RED + f"{random_action[1]}\n" + Style.RESET_ALL)

                    print(Fore.RED + f"The next airport's ICAO-code is: {result}\n" + Style.RESET_ALL)

                else:
                    print(Fore.RED + f"{random_action[2]}\n" + Style.RESET_ALL)


        # Talk to airport's security chief
        elif user_input == 3: 
            game_dict = security(game_dict, luck)
            



        # Buy a flight ticket
        elif user_input == 4 and game_dict["next_location"] != "": # If user input is 4 and we got the location (from quiz or eyewitness)
            print(Fore.RED + f"\nBuy a flight ticket" + Style.RESET_ALL)


            break # endless loop ends here


        # Solve the clue
        elif user_input == 4 and game_dict["talk_to_chief"] and game_dict['criminal_was_here'] and game_dict["clue_solved"] != True and game_dict["next_location"] == "": # visible IF we've talked to security chief AND the criminal has been at the airport AND we haven't solved the clue yet AND we don't know next location
            question_bool = ask_question(game_dict["quiz_questions"])
            game_dict["got_location"] = quiz_icao(question_bool)


        # Try to solve the previous clue again
        elif user_input == 4 and game_dict["talk_to_chief"] and not game_dict["criminal_was_here"] and game_dict["clue_solved"] != True and game_dict["next_location"] == "": # visible IF we've talked to security chief AND the criminal has NOT been at the airport AND we haven't solved the clue yet AND we don't know next location
            print(Fore.RED + f"\nTry to solve the previous clue again" + Style.RESET_ALL)



    return game_dict
            
    
    

if __name__ == "__main__":
    from questions import ask_category, ask_question, get_questions
    from game_setup import game_setup

    # define game_dict
    while True:
        #setup game parameters
        game_dict = game_setup()
        game_dict["quiz_category"] = ask_category()
        game_dict["quiz_questions"] = get_questions(game_dict["difficulty"], game_dict["quiz_category"])

        game_dict = airport_menu(game_dict)
