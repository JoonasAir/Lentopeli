from copy import deepcopy
from game_parameters import game_parameters_DEFAULT
from unnecessary.styles import styles_DEFAULT, colors


def settings(game_parameters:dict, styles:dict):

    while True:
        print(styles["menu"] + "\nS E T T I N G S\n\n"+ styles["reset"])

        option_number = 1
        menu = "Select from following options:\n"

        menu += f"    {option_number} - Custom difficulty's settings\n"
        option_number += 1

        menu += f"    {option_number} - Appearance settings\n"

        menu += f"    0 - Back to main menu\n"
        menu += "Input: "

        while True: # Asks input until valid one is given
            try:
                user_input = int(input(styles['input'] + menu + styles["reset"]))
                if user_input in range(option_number+1):
                    break
                else:
                    print(styles["warning"] + "Invalid input. Try again." + styles["reset"])
            except ValueError:
                print(styles["warning"] + "Invalid input. Try again." + styles["reset"])


        if user_input == 1: # Custom difficulty's settings
            while True:

                print(styles["menu"] + "\nS E T T I N G S   -   C U S T O M   D I F F I C U L T Y\n\n"+ styles["reset"])
    
                option_number = 1
                menu = "Select from following options:\n"
    
                menu += f"    {option_number} - amount of money at the beginning of the game\n"
                option_number += 1
                menu += f"    {option_number} - price of a flight ticket\n"
                option_number += 1
                menu += f"    {option_number} - time to catch the criminal\n"
                option_number += 1
                menu += f"    {option_number} - criminal's head start at the start of the game\n"
                option_number += 1
                menu += f"    {option_number} - time interval at which the criminal flies to the next location\n"
                option_number += 1
                menu += f"    {option_number} - difficulty for quiz questions\n"
                option_number += 1
                menu += f"    {option_number} - possibility of gaining random benefits\n"
                option_number += 1
                menu += f"    {option_number} - RESET DEFAULT\n"
                menu += f"    0 - Back to settings menu\n"
                menu += "Input: "

                while True: # Asks input until valid one is given
                    try:
                        user_input = int(input(styles['input'] + menu + styles["reset"]))
                        if user_input in range(option_number+1):
                            break
                        else:
                            print(styles["warning"] + "Invalid input. Try again." + styles["reset"])
                    except ValueError:
                        print(styles["warning"] + "Invalid input. Try again." + styles["reset"])


                if user_input == 1: # money at the beginning of the game
                    print(styles["output"] + f"Money at the beginning of the game.\nCurrent value: {game_parameters["game_money"]}" + styles["reset"])
                    user_input = int(input(styles['input'] + "Give amount of money you would like to have in the beginning of the game: " + styles["reset"]))
                    game_parameters['game_money'] = user_input
                    print(styles["output"] + f"game_money updated to: {game_parameters['game_money']}" + styles["reset"])

                elif user_input == 2: # price of a flight ticket
                    print(styles["output"] + f"" + styles["reset"])
                    user_input = int(input(styles['input'] + ": " + styles["reset"]))
                    #        'flight_price':200,                   """
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                elif user_input == 3: # time at the beginning of the game
                    print(styles["output"] + f"" + styles["reset"])
                    user_input = int(input(styles['input'] + ": " + styles["reset"]))
                    #        'game_time': 60*5,          
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                elif user_input == 4: # the criminal's head start at the start of the game
                    print(styles["output"] + f"" + styles["reset"])
                    user_input = int(input(styles['input'] + ": " + styles["reset"]))
                    #        'criminal_headstart': 4,    
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                elif user_input == 5: # the time interval at which the criminal flies to the next location
                    print(styles["output"] + f"" + styles["reset"])
                    user_input = int(input(styles['input'] + ": " + styles["reset"]))
                    #        'criminal_time': 3,         
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                elif user_input == 6: # difficulty for quiz questions
                    print(styles["output"] + f"" + styles["reset"])
                    user_input = int(input(styles['input'] + ": " + styles["reset"]))
                    #        'difficulty': 'easy'        
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                elif user_input == 7: # the possibility of benefiting from random functions
                    print(styles["output"] + f"" + styles["reset"])
                    user_input = int(input(styles['input'] + ": " + styles["reset"]))
                    #        'random_luck': 0.50,        
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                elif user_input == 8: # RESET CUSTOM DIFFICULTY SETTINGS TO DEFAULT 
                    
                    user_confirm = str(input(styles['warning'] + "\nDo you want to reset the custom difficulty settings to default? This cannot be undone.\n'Y' = Yes, 'N' = No: " + styles["reset"])).strip().upper()
                    while user_confirm not in ("N", "Y"):
                        print(styles['warning'] + "\nInvalid input. Try again. ")
                        user_confirm = str(input(styles['warning'] + "\nDo you want to reset the custom difficulty settings to default? This cannot be undone.\n'Y' = Yes, 'N' = No: " + styles["reset"])).strip().upper()
                    
                    if user_confirm == "Y":
                        game_parameters = deepcopy(game_parameters_DEFAULT)
                        print(styles['output'] + "\nThe custom difficulty settings have been reset to their default values.\n" + styles["reset"])

                    else: print(styles['output'] + "\nSettings left untouched.\n" + styles["reset"])

                if user_input == 0:
                    break



        elif user_input == 2: # Appereance settings
            while True:

                print(styles["menu"] + "\nS E T T I N G S   -   A P P E A R A N C E\n\n"+ styles["reset"])
                color_list = [("warning", "change appearance of warning prints"), 
                               ("input", "change appearance of input prints"), 
                               ("output", "change appearance of output prints"), 
                               ("menu", "change appearance of menu headers ('S E T T I N G S' etc.)"), 
                               ("location", "change appearance of in-game location prints ('You're in aiport/country X')"), 
                               ("time", "change appearance of in-game time prints (You have min:sec time left)")
                               ]

                option_number = 1
                menu = styles["input"] + "Select from following options:\n" + styles["reset"]

                for index in range(len(color_list)):
                    menu += styles[color_list[index][0]] + f"    {option_number} - {color_list[index][1]}\n" + styles["reset"]
                    option_number += 1


                menu += styles["input"] + f"\n    {option_number} - RESET DEFAULT\n"
                menu += f"    0 - Back to settings menu\n"
                menu += "Input: " + styles["reset"]

                while True: # Asks input until valid one is given
                    try:
                        user_input = int(input(styles['input'] + menu + styles["reset"]))
                        if user_input in range(option_number+1):
                            break
                        else:
                            print(styles["warning"] + "Invalid input. Try again." + styles["reset"])
                    except ValueError:
                        print(styles["warning"] + "Invalid input. Try again." + styles["reset"])

                try:
                    error = color_list[user_input-1]
                    if user_input-1 in range(len(color_list)):
                        option_num = 1
                        option_ls = []
                        for color in colors:
                            print(f"{colors[color]}    {option_num}. {color}{styles['reset']}")
                            option_num += 1
                            option_ls.append(color)

                        user_color = int(input(styles["input"] + "Choose a color from earlier options: "))

                        styles[color_list[user_input-1]] = colors[option_ls[user_color-1]]

                except KeyboardInterrupt or ValueError or IndexError: # Crtl+C or string input or invalid index (wrong input)
                    pass

            
                if user_input == len(color_list)+1: # RESET APPEARANCE SETTINGS TO DEFAULT

                    user_confirm = str(input(styles['warning'] + "\nDo you want to reset the appearance settings to default? This cannot be undone.\n'Y' = Yes, 'N' = No: " + styles["reset"])).strip().upper()
                    while user_confirm not in ("N", "Y"):
                        print(styles['warning'] + "\nInvalid input. Try again. " + styles["reset"])
                        user_confirm = str(input(styles['warning'] + "\nDo you want to reset the appearance settings to default? This cannot be undone.\n'Y' = Yes, 'N' = No: " + styles["reset"])).strip().upper()

                    if user_confirm == "Y":
                        styles = deepcopy(styles_DEFAULT)
                        print(styles['output'] + "\nAppearance settings have been reset to their default values.\n" + styles["reset"])

                    else: print(styles['output'] + "\nSettings left untouched.\n" + styles["reset"])


                if user_input == 0: # Back to settings menu
                    break

                    



        elif user_input == 0: # Back to main menu
            break
        
    return game_parameters, styles

if __name__ == "__main__":
    pass
