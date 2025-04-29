from styles import styles

def tutorial():

    tutorial = "Here is the tutorial for the game. (incoming) \n    1. how the game works\n    2. game settings\n    3. practice quiz questions\n    4. leaderboard"


    print(styles["output"] + f"{tutorial}" + styles["reset"])
    
    input(styles["input"] + "\nPress enter to return to the main menu." + styles["reset"])

if __name__ == "__main__":
    tutorial()
