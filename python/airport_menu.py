from random import randint
from player import change_location
from python.mysql_connection import mysql_connection
from questions import quiz_icao, ask_question, ask_again
from security import talk_to_security
from reduce_money import reduce_money
from game_parameters import airport_random_actions
import textwrap
import shutil


def airport_menu_input(game_dict:dict):
    print(game_dict["time_left_str"])
    option_num = 1
    option_list = []
    
    airport_actions = [
        "Check remaining money",
        "Talk to airport's security chief", 
        "Solve the clue",                       # visible if we've talked to security chief and the criminal has been at the airport
        "Try to solve the previous clue again", # visible if we gave wrong ansver in quiz -> we came to wrong airport and we have talked to security chief to find out that the criminal has not been here
        "Buy a flight ticket",                  # visible after solving a clue
    ]

    if game_dict["first_iteration"]:
        game_dict["random_index_airport"] = randint(0, len(airport_random_actions)-1)
        game_dict["first_iteration"] = False

    menu = "\nChoose your action from following options:\n"
    menu += f"    {option_num} - {airport_actions[0]}\n"               # Check remaining time and money
    option_num += 1
    option_list.append(airport_actions[0])
    menu += f"    {option_num} - {airport_random_actions[game_dict['random_index_airport']][0]}\n"  # Randomly picked action from airport_random_actions
    option_num += 1
    option_list.append(airport_random_actions[game_dict['random_index_airport']][0])
    menu += f"    {option_num} - {airport_actions[1]}\n"               # Talk to airport's security chief
    option_list.append(airport_actions[1])
    option_num += 1

    # Solve the clue
    if game_dict["talk_to_chief"] and game_dict['criminal_was_here'] and game_dict["clue_solved"] != True and not game_dict["next_location_bool"]: # visible IF we've talked to security chief AND the criminal has been at the airport AND we haven't solved the clue yet AND we don't know next location
        menu += f"    {option_num} - {airport_actions[2]}\n"
        option_num += 1
        option_list.append(airport_actions[2])

    # Try to solve the previous clue again
    if game_dict["talk_to_chief"] and not game_dict["criminal_was_here"] and game_dict["clue_solved"] != True and not game_dict["next_location_bool"]: # visible IF we've talked to security chief AND the criminal has NOT been at the airport AND we haven't solved the clue yet AND we don't know next location
        menu += f"    {option_num} - {airport_actions[3]}\n"           
        option_num += 1
        option_list.append(airport_actions[3])

    # Buy a flight ticket
    elif game_dict["next_location_bool"]: # visible IF we got the location (from quiz or with luck_bool)
        menu += f"    {option_num} - {airport_actions[4]}\n"
        option_num += 1
        option_list.append(airport_actions[4])
    
    while True:
        try:
            user_input_int = int(input(menu + "Input: "))
            if user_input_int in range(1, len(option_list)+1):
                break
            else:
                print("Invalid input, try again." )
        except ValueError:
            print("Invalid input, try again." )
        except KeyboardInterrupt:
            break

    
    
    user_input = option_list[user_input_int-1]
    
    return game_dict, user_input, airport_random_actions[game_dict['random_index_airport']]





def airport_menu(game_dict:dict):

    cursor = mysql_connection.cursor()

    while True: # break out from loop when we fly to next location
        luck_bool = bool(randint(0,1000000)/1000000 <= game_dict["random_luck"]) # check if we are luck_bool. Based on variable random_luck defined on game_setup()
        print("\n")

        game_dict, user_input, random_action = airport_menu_input(game_dict) # ask what user wants to do at the airport
        print("\n\n")

        if user_input == "Check remaining money" : 
            print(f"You have {game_dict['game_money']}€ left to spend." )


        elif user_input == random_action[0]:
            if game_dict["tried_luck"]: # if we have tried our luck at current airport
                print(f"{random_action[3]}" )
            else:
                print(f"You chose to {random_action[0].lower()}.\n" )
                game_dict["tried_luck"] = True
                if luck_bool:
                    game_dict["got_location"] = True
                    sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    if type(result) == tuple:
                        longtext = random_action[1]
                        terminal_width = shutil.get_terminal_size().columns
                        wrapped_text = textwrap.fill(longtext, width = terminal_width/2)



                        print(f"{wrapped_text}\n" )
                        game_dict["next_location_bool"] = True
                        print(f"The next location is: {result[0]}" )

                else:
                    print(f"{random_action[2]}\n" )


        elif user_input == "Talk to airport's security chief": 
            game_dict = talk_to_security(game_dict, luck_bool)
            



        elif user_input == "Buy a flight ticket": 
            change_location(game_dict)
            reduce_money(game_dict)
            
            break # airport loop ends here


        elif user_input == "Solve the clue":
            ask_question_bool, game_dict['previous_question'] = ask_question(game_dict["quiz_questions"])
            quiz_icao(ask_question_bool, game_dict)


        elif user_input == "Try to solve the previous clue again": 
            ask_question_bool = ask_again(game_dict["previous_question"])
            quiz_icao(ask_question_bool, game_dict)



    return game_dict
            
    
    

if __name__ == "__main__":
    from questions import ask_category, get_questions
    from game_setup import game_setup
    from game_parameters import game_parameters

    game_dict = game_setup(game_parameters)
    luck_bool = bool(randint(0,1000000)/1000000 <= game_dict["random_luck"])
    game_dict["quiz_category"] = ask_category()
    game_dict["quiz_questions"] = get_questions(game_dict["difficulty"], game_dict["quiz_category"])
    game_dict = airport_menu(game_dict)
