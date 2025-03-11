from random import randint
from player import change_location, print_location
from mysql_connection import mysql_connection
from questions import quiz_icao
from security import talk_to_security
from styles import styles




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
    random_actions = [
        ("Visit the restroom", 
         "You overheard a conversation in the restroom about Shadow's next move! The individuals were discussing a recent sighting of Shadow boarding a flight. You decide to verify this information and find out it's true; you got his location.", 
         "You went to the restroom and now feel refreshed.", 
         "You already went to the restroom. No need to go again."),

        ("Go to get a cup of coffee", 
         "The barista, recognizing you as an Interpol agent, mentioned seeing someone suspicious matching Shadow's description. They saw him purchasing a ticket at the counter. You decide to follow up on this lead and confirm that Shadow was indeed spotted here recently; you got his location.", 
         "You went to get a large cup of coffee and now feel more energized.", 
         "Maybe it's better not to get a second cup of coffee. You've had enough caffeine."),

        ("Go to get a meal", 
         "A fellow diner, impressed by your Interpol badge, shared a rumor about Shadow's next move. They overheard Shadow talking on the phone about his next flight. You decide to verify this information and discover it's a false alarm; the diner was mistaken.", 
         "You went to grab a hamburger meal and now feel satisfied.", 
         "You already went to McDonald's. You're not hungry anymore."),

        ("Go to relax in a lounge", 
         "You saw a live news report in the lounge hinting at Shadow's activities! The report mentioned increased security due to a recent sighting of Shadow. You decide to verify this information and find out that the report is accurate; you got his location.", 
         "You went to the lounge to rest for a moment and now feel rejuvenated.", 
         "You already relaxed in the lounge. Time to get back to work."),

        ("Browse the duty-free shop", 
         "A shop assistant, noticing your Interpol credentials, mentioned seeing someone suspicious. They saw Shadow making a purchase and then heading towards the gates. You decide to investigate further and confirm that the person was indeed acting suspiciously; you got his location.", 
         "You browsed the duty-free shop and found some interesting items.", 
         "You already browsed the duty-free shop. No need to go again."),

        ("Check the flight information board", 
         "You noticed some unusual activity on the flight information board. You decide to check it out and discover that Shadow has been tampering with the flight schedules. The tampering indicates his next move; you got his location.", 
         "You checked the flight information board and confirmed your flight details.", 
         "You already checked the flight information board. No need to check again."),

        ("Talk to the information desk", 
         "The staff at the information desk, eager to assist an Interpol agent, gave you a tip about Shadow's next move. They received a report from security about Shadow's recent activity. You decide to follow up on this lead and find out that the tip is credible; you got his location.", 
         "You talked to the information desk and got some useful travel information.", 
         "You already talked to the information desk. No need to ask again."),

        ("Visit the airport bookstore", 
         "You found a live news broadcast in the bookstore with an update on Shadow's activities! The broadcast mentioned a recent sighting of Shadow in the airport. You decide to verify this information and confirm that the broadcast is providing accurate updates; you got his location.", 
         "You visited the airport bookstore and found some interesting reads.", 
         "You already visited the airport bookstore. No need to go again."),

        ("Take a walk around the terminal", 
         "You overheard a conversation about Shadow's next move while walking. The individuals were discussing seeing Shadow near the boarding gates. You decide to investigate further and find out that the conversation was based on a real sighting; you got his location.", 
         "You took a walk around the terminal and stretched your legs.", 
         "You already took a walk around the terminal. No need to walk again."),

        ("Charge your phone at a charging station", 
         "You saw a suspicious person leaving a note at the charging station. The note mentioned Shadow's next flight. You decide to check it out and discover that the note contains valuable information about Shadow's plans; you got his location.", 
         "You charged your phone and now have a full battery.", 
         "You already charged your phone. No need to charge again.")
    ]

    if game_dict["first_iteration"]:
        game_dict["random_index_airport"] = randint(0, len(random_actions)-1)
        game_dict["first_iteration"] = False

    menu = "\nChoose your action from following options:\n"
    menu += f"    {option_num} - {airport_actions[0]}\n"               # Check remaining time and money
    option_num += 1
    option_list.append(airport_actions[0])
    menu += f"    {option_num} - {random_actions[game_dict['random_index_airport']][0]}\n"  # Randomly picked action from random_actions
    option_num += 1
    option_list.append(random_actions[game_dict['random_index_airport']][0])
    menu += f"    {option_num} - {airport_actions[1]}\n"               # Talk to airport's security chief
    option_list.append(airport_actions[1])
    option_num += 1

    # Solve the clue
    if game_dict["talk_to_chief"] and game_dict['criminal_was_here'] and game_dict["clue_solved"] != True and game_dict["next_location"] == "": # visible IF we've talked to security chief AND the criminal has been at the airport AND we haven't solved the clue yet AND we don't know next location
        menu += f"    {option_num} - {airport_actions[2]}\n"
        option_num += 1
        option_list.append(airport_actions[2])

    # Try to solve the previous clue again
    if game_dict["talk_to_chief"] and not game_dict["criminal_was_here"] and game_dict["clue_solved"] != True and game_dict["next_location"] == "": # visible IF we've talked to security chief AND the criminal has NOT been at the airport AND we haven't solved the clue yet AND we don't know next location
        menu += f"    {option_num} - {airport_actions[3]}\n"           
        option_num += 1
        option_list.append(airport_actions[3])

    # Buy a flight ticket
    elif game_dict["next_location"] != "": # visible IF we got the location (from quiz or with luck_bool)
        menu += f"    {option_num} - {airport_actions[4]}\n"
        option_num += 1
        option_list.append(airport_actions[4])
    
    while True:
        try:
            user_input_int = int(input(styles["input"] + menu + "Input: "+ styles["reset"]))
            if user_input_int in range(1, len(option_list)+1):
                break
            else:
                print(styles["warning"] + "Invalid input, try again." + styles["reset"])
        except ValueError:
            print(styles["warning"] + "Invalid input, try again." + styles["reset"])
        except KeyboardInterrupt:
            break

    
    
    user_input = option_list[user_input_int-1]
    
    return game_dict, user_input, random_actions[game_dict['random_index_airport']]





def airport_menu(game_dict:dict):

    cursor = mysql_connection.cursor()

    while True: # break out from loop when we fly to next location
        luck_bool = bool(randint(0,1000000)/1000000 <= game_dict["random_luck"]) # check if we are luck_bool. Based on variable random_luck defined on game_setup()
        print("\n")

        game_dict, user_input, random_action = airport_menu_input(game_dict) # ask what user wants to do at the airport
        print("\n\n")

        if user_input == "Check remaining money" : 
            print(styles["output"] + f"You have {game_dict['game_money']}€ left to spend." + styles["reset"])


        elif user_input == random_action[0]:
            if game_dict["tried_luck"]:
                print(styles["output"] + f"{random_action[3]}" + styles["reset"])
            else:
                print(styles["output"] + f"You chose to {random_action[0].lower()}.\n" + styles["reset"])
                game_dict["tried_luck"] = True
                if luck_bool:
                    game_dict["got_location"] = True
                    sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
                    cursor.execute(sql)
                    result = cursor.fetchone()[0]
                    game_dict["next_location"] = result
                    print(styles["output"] + f"{random_action[1]}\n" + styles["reset"])

                    print(styles["output"] + f"The next airport's ICAO-code is: {result}\n" + styles["reset"])

                else:
                    print(styles["output"] + f"{random_action[2]}\n" + styles["reset"])


        elif user_input == "Talk to airport's security chief": 
            game_dict = talk_to_security(game_dict, luck_bool)
            



        elif user_input == "Buy a flight ticket": 
            print(styles["output"] + f"\nHere you buy a flight ticket" + styles["reset"])
            change_location(game_dict)
            
            #TODO change player's location
            
            

            break # endless loop ends here


        elif user_input == "Solve the clue":
            ask_question_bool = ask_question(game_dict["quiz_questions"])
            quiz_icao(ask_question_bool, game_dict)


        elif user_input == "Try to solve the previous clue again": 
            print(styles["output"] + f"\nHere you try to solve the previous clue again" + styles["reset"])



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
