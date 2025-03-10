from styles import styles

def tutorial():

    tutorial = "Here is the tutorial for the game. \nIt tells user:\n    1. progression of the game\n    2. rules and useful nicks\n    3. in main menu's option 'settings':\n        1. you can make custom difficulty by modifying settings\n        2. modify styles of different categories\n    4. you can practice quiz questions "


    print(styles["output"] + f"{tutorial}" + styles["reset"])
    
    input(styles["input"] + "\nPress enter to return to the main menu." + styles["reset"])

if __name__ == "__main__":
    tutorial()
