from colorama import Style
from settings import colors


def leaderboard():
    


    result = "Leaderboard is printed here"

    print(colors["output"] + f"{result}" + Style.RESET_ALL)

    input(colors["input"] + "\nPress enter to return to the main menu." + Style.RESET_ALL)
