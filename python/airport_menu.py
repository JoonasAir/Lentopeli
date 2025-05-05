from random import randint

from click import option
from player import change_location
from mysql_connection import mysql_connection
from questions import quiz_icao, ask_question, ask_again
from security import talk_to_security
from reduce_money import reduce_money
from game_parameters import airport_random_options
import textwrap
import shutil


def airport_menu_input(game_dict:dict):
    try:
        game_dict = game_dict["value"]
    except:
        pass
    
    if game_dict["first_iteration"]:
        game_dict["random_event_index"] = randint(0, len(airport_random_options)-1)
        game_dict["first_iteration"] = False
    

    airport_options = [
        {"text": "Talk to airport's security chief", "value": "talkToSecurity"},
        {"text": "Solve the clue", "value": "solveClue"},                               # visible if we've talked to security chief and the criminal has been at the airport
        {"text": "Try to solve the previous clue again", "value": "solvePreviousClue"},    # visible if we gave wrong ansver in quiz -> we came to wrong airport and we have talked to security chief to find out that the criminal has not been here
        {"text": airport_random_options, "value": "randomAction"},
    ]


    if len(game_dict['airport_options']) == 0 or game_dict["first_iteration"]:
        option_list = [str(game_dict["player_location"])]
        # Talk to security
        option_list.append({"text": airport_options[0]["text"], "value": airport_options[0]["value"]})
        # Random action
        option_list.append({"text": airport_options[-1]["text"][game_dict["random_event_index"]], "value": airport_options[-1]["value"]})

        # Solve the clue
        if game_dict["talk_to_chief"] and game_dict['criminal_was_here'] and not game_dict["clue_solved"] and not game_dict["next_location_bool"]: # visible IF we've talked to security chief AND the criminal has been at the airport AND we haven't solved the clue yet AND we don't know next location
            option_list.append({"text": airport_options[1]["text"], "value": airport_options[1]["value"]})

        # Try to solve the previous clue again
        if game_dict["talk_to_chief"] and not game_dict["criminal_was_here"] and not game_dict["clue_solved"] and not game_dict["next_location_bool"]: # visible IF we've talked to security chief AND the criminal has NOT been at the airport AND we haven't solved the clue yet AND we don't know next location
            option_list.append({"text": airport_options[2]["text"], "value": airport_options[2]["value"]})
        game_dict["airport_options"] = option_list
    
    elif not game_dict["first_iteration"]:
        option_list = [
            game_dict["player_location"], 
            {"text": airport_options[0]["text"], "value": airport_options[0]["value"]},
            game_dict["airport_options"][2]
            ]

        # Solve the clue
        if game_dict["talk_to_chief"] and game_dict['criminal_was_here'] and not game_dict["clue_solved"] and not game_dict["next_location_bool"]: # visible IF we've talked to security chief AND the criminal has been at the airport AND we haven't solved the clue yet AND we don't know next location
            option_list.append({"text": airport_options[1]["text"], "value": airport_options[1]["value"]})

        # Try to solve the previous clue again
        if game_dict["talk_to_chief"] and not game_dict["criminal_was_here"] and not game_dict["clue_solved"] and not game_dict["next_location_bool"]: # visible IF we've talked to security chief AND the criminal has NOT been at the airport AND we haven't solved the clue yet AND we don't know next location
            option_list.append({"text": airport_options[2]["text"], "value": airport_options[2]["value"]})

        game_dict["airport_options"] = option_list


    return game_dict





def airport_menu(game_dict:dict):

    cursor = mysql_connection.cursor()
    user_input = 0
    random_action = 0
    while True: # break out from loop when we fly to next location
        game_dict["random_luck_bool"] = bool(randint(0,1000000)/1000000 <= game_dict["random_luck"]) # check if we are lucky calculated with variable "game_dict["random_luck"])" defined on game_setup()

        game_dict = airport_menu_input(game_dict) # ask what user wants to do at the airport

        if user_input == "Check remaining money": 
            print(f"You have {game_dict['game_money']}€ left to spend." )


        elif user_input == random_action[0]:
            if game_dict["tried_luck"]: # if we have tried our luck at current airport
                print(f"{random_action[3]}" )
            else:
                print(f"You chose to {random_action[0].lower()}.\n" )
                game_dict["tried_luck"] = True
                if game_dict["random_luck_bool"]:
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
            game_dict = talk_to_security(game_dict)
            



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
    game_dict["random_luck_bool"] = bool(randint(0,1000000)/1000000 <= game_dict["random_luck"])
    game_dict["quiz_category"] = ask_category()
    game_dict["quiz_questions"] = get_questions(game_dict["difficulty"], game_dict["quiz_category"])
    game_dict = airport_menu(game_dict)
