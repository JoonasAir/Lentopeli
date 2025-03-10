
def settings(difficulty_parameters, styles):

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


                if user_input == 1:
                    user_input = int(input(styles['input'] + "Give amount of money you would like to have in the beginning of the game: ") + styles["reset"])
                    #        'game_money': 5000,         # money at the beginning of the game
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                if user_input == 2:
                    user_input = int(input(styles['input'] + ": ") + styles["reset"])
                    #        'flight_price':200,         # price of a flight ticket          """
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                if user_input == 3:
                    user_input = int(input(styles['input'] + ": ") + styles["reset"])
                    #        'game_time': 60*5,          # time at the beginning of the game
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                if user_input == 4:
                    user_input = int(input(styles['input'] + ": ") + styles["reset"])
                    #        'criminal_headstart': 4,    # the criminal's head start at the start of the game
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                if user_input == 5:
                    user_input = int(input(styles['input'] + ": ") + styles["reset"])
                    #        'criminal_time': 3,         # the time interval at which the criminal flies to the next location
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                if user_input == 6:
                    user_input = int(input(styles['input'] + ": ") + styles["reset"])
                    #        'difficulty': 'easy'        # difficulty for quiz questions
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                if user_input == 7:
                    user_input = int(input(styles['input'] + ": ") + styles["reset"])
                    #        'random_luck': 0.50,        # the possibility of benefiting from random functions
                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])

                if user_input == 0:
                    break



        elif user_input == 2: # Appereance settings
            while True:

                print(styles["menu"] + "\nS E T T I N G S   -   A P P E A R A N C E\n\n"+ styles["reset"])
    
                option_number = 1
                menu = "Change color of:\n"
    
                menu += f"    {option_number} - input prints\n"
                option_number += 1
                menu += f"    {option_number} - warning prints\n"
                option_number += 1
                menu += f"    {option_number} - output prints\n"
                option_number += 1
                menu += f"    {option_number} - menu location prints ('S E T T I N G S' etc.)\n"
                option_number += 1
                menu += f"    {option_number} - in-game location prints ('You're in aiport/country X')\n"
                option_number += 1
                menu += f"    {option_number} - in-game time prints (You have min:sec time left)\n"
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




                if user_input == 1: # input prints
                    user_input = int(input(styles['input'] + "Select color for input prints: ") + styles["reset"])
                    # "input":Fore.CYAN

                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])



                if user_input == 2: # warning prints
                    user_input = int(input(styles['input'] + ": ") + styles["reset"])
                    # "warning":Fore.RED

                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])



                if user_input == 3: # output prints
                    user_input = int(input(styles['input'] + ": ") + styles["reset"])
                    # "output":Fore.LIGHTYELLOW_EX

                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])



                if user_input == 4: # menu location prints ('S E T T I N G S' etc.)
                    user_input = int(input(styles['input'] + ": ") + styles["reset"])
                    # "menu":Fore.LIGHTMAGENTA_EX

                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])



                if user_input == 5: # in-game location prints ('You're in aiport/country X')
                    user_input = int(input(styles['input'] + ": ") + styles["reset"])
                    # "location":Fore.LIGHTGREEN_EX

                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])



                if user_input == 6: # in-game time prints (You have min:sec time left)
                    user_input = int(input(styles['input'] + ": ") + styles["reset"])
                    # "time":Fore.LIGHTBLUE_EX

                    print(styles['warning'] + "NOT WORKING YET!" + styles["reset"])



                if user_input == 0: # Back to settings menu
                    break



        elif user_input == 0: # Back to main menu
            break


if __name__ == "__main__":
    from styles import styles