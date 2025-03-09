from colorama import Style
from settings import colors


def tutorial():

    tutorial = "Here is the tutorial for the game. \nIt tells user:\n    1. progression of the game\n    2. rules and useful nicks\n    3. in main menu's option 'settings':\n        1. you can make custom difficulty by modifying settings\n        2. modify colors of different categories\n    4. you can practice quiz questions "


    print(colors["output"] + f"{tutorial}" + Style.RESET_ALL)
    
    input(colors["input"] + "\nPress enter to return to the main menu." + Style.RESET_ALL)

if __name__ == "__main__":
    tutorial()
