from random import randint


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
    menu += f"    4 - {airport_actions[2]}\n"               # Solve the clue

# visible if we gave wrong ansver in quiz -> we came to wrong airport and we have talked to security chief to find out that the criminal has not been here
    menu += f"    4 - {airport_actions[3]}\n"               # Try to solve the previous clue again

# visible after solving a clue
    menu += f"    4 - {airport_actions[4]}\n"               # Buy a flight ticket


    user_input = input(menu + "Input: ")

    return user_input

def airport_actions(user_input):
    while user_input != 0:
    
        if user_input == 1 : # Check remaining time and money
            print("Check remaining time and money")
    
        elif user_input == 2: # Randomly picked action from random_actions
            print("Randomly picked action from random_actions")

        elif user_input == 3: # Talk to airport's security chief
            print("Talk to airport's security chief")
    
        elif user_input == 4: # Solve the clue
            print("Solve the clue")
    
        elif user_input == 4: # Try to solve the previous clue again
            print("Try to solve the previous clue again")
    
        elif user_input == 4: # Buy a flight ticket
            print("Buy a flight ticket")
            
    
    

if __name__ == "__main__":
    airport_actions(airport_menu())
