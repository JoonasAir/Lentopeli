from airport_menu import airport_action, airport_menu_input
from game_setup import game_setup
import multiprocessing
from criminal import criminal_timer, criminal_headstart
from questions import ask_category, get_questions, ask_question


def new_game():
    #TODO add 'Check remaining time' -option on every input
    print("At any moment of the game give 't' as an input to get remaining time.")

#   screen_name, starting location and difficulty parameters returned in dictionary
    game_dict = game_setup() # keys of the dictionary: 'game_money', 'game_time', 'random_luck', 'criminal_headstart', 'criminal_time', 'screen_name', 'player_location', 'difficulty', 'quiz_category'
    criminal_headstart(game_dict["criminal_headstart"]) # clears criminal table and adds "criminal_headstart" amount of airports 

#   Choosing category of quiz questions
    game_dict["quiz_category"] = ask_category()
#   Get quiz questions with right difficulty and category
    quiz_questions = get_questions(game_dict["difficulty"], game_dict["quiz_category"])



#   background story of the game (Y/N) = (player can read or skip the story)



#   Game starts

    # Defining and starting a background process for criminal_timer function
    # Using Manager to share state between processes (when we change criminal_timer_state to False in the main program, the loop in the background process will close)
    manager = multiprocessing.Manager()
    # Boolean value for the function loop. We have to use manager because we need this variable in both processes
    criminal_timer_state = manager.Value('b', True)
    # Define the process
    ProcessCriminalTimer = multiprocessing.Process(target=criminal_timer, args=(criminal_timer_state, game_dict['criminal_time']))
    # Start the process
    ProcessCriminalTimer.start()


    
    while not game_dict["criminal_caught"]:

        # Player is presented with options what he can do at the airport
        game_dict, airport_input, airport_random_action = airport_menu_input(game_dict)
        # player's input on previous with other helper-variables is passed to airport_action where the action happens
        game_dict = airport_action(game_dict, airport_input, airport_random_action)

        # check at the new airport if we caught the criminal
        #game_dict["criminal_caught"] = criminal_caught()








# The game ends when:
#   1. You reach the same airport as the criminal

#   2. The criminal manages to sabotage X number of airports

#   3. Time runs out
#   4. You fly off course or get deceived too many times



    # Ending the loop running in the background process
    criminal_timer_state.value = False
    # Force the termination of the background process, as the process loop contains a sleep function 
    # (otherwise the player would have to wait until the criminal flies to the next airport)
    ProcessCriminalTimer.terminate()
    # Ensure the background process has ended before moving on
    ProcessCriminalTimer.join()


# When the game ends:
#   1. Scores are calculated
#   2. The game statistics are printed (screen name, how many games played with this screen name, difficulty level, score, elapsed time, money at the start, money spent, number of flights, number of off-course flights)
#   3. Save game stats to the leaderboard table

# Return to the start menu

if __name__ == "__main__":
    new_game()
