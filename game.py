from criminal_headstart import criminal_headstart
from game_setup import game_setup
import multiprocessing
from criminal_timer_multiprocessing import criminal_timer
import mysql.connector


connection = mysql.connector.connect(
    collation = "utf8mb4_general_ci",
    host = '127.0.0.1',
    port = 3306,
    database = "flight_game",
    user = "python",
    password = "koulu123",
    autocommit = True
)

if __name__ == "__main__": # Main block

# Start menu (new game, highscores, quiz practice, instructions, exit game)


# New game 

#   screen_name, starting location and difficulty parameters returned in dictionary
    game_dict = game_setup() # sanakirjan avaimet: 'game_money', 'game_time', 'random_luck', 'criminal_headstart', 'criminal_time', 'screen_name', 'player_location'
    criminal_headstart(game_dict["criminal_headstart"]) # clears criminal table and adds "criminal_headstart" amount of airports 
    
#   quiz questions

 
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


# The player is presented with a menu at the airport, where they can choose what to do:

#   1. Talk to the security chief
#           (find out if the criminal has been at the airport)


#   2. Visit the restroom
#           (chance to meet an eyewitness. 
#           The eyewitness might also deceive you)


#   3. Have a coffee
#           (chance to meet an eyewitness. 
#           The eyewitness might also deceive you)


#   4. Have a meal
#           (chance to meet an eyewitness. 
#           The eyewitness might also deceive you)


#   5. Buy a flight ticket
#           (we can buy a flight ticket using the ICAO code)

 
#   7. Check remaining time and money
 

#  *8. Solve the clue --> quiz questions
#           (this option is visible to the player if they have 
#           talked to the security chief and if the criminal 
#           has been at the airport)


#  *8. Try to solve the previous clue again --> same quiz question as earlier
#           (this option is visible to the player if they have 
#           talked to the security chief and if the criminal 
#           has not been at the airport)


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
