from colorama import Fore, Style
from copy import deepcopy

styles_DEFAULT = {
    "input":Fore.CYAN,
    "warning":Fore.RED,
    "time":Fore.LIGHTBLUE_EX,
    "location":Fore.LIGHTYELLOW_EX,
    "menu":Fore.LIGHTMAGENTA_EX,
    "output":Fore.GREEN,
    "reset":Style.RESET_ALL
}
styles = deepcopy(styles_DEFAULT) # copy styles_DEFAULT to new dictionary with deepcopy. Otherwise those would exist in same location in memory and basically be the same dictionary with two names. We need this original for user to be able to reset default settings
