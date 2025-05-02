# Voidaan käyttää json tiedostoa missä kysymykset
import json
from mysql_connection import mysql_connection
# Voidaan valita satunnaisia kysymyksiä sekä sekoitta vastausvaihtoehdot
import random 
# Voidaan muuttaa kysymysten HTML elementit oikeiksi merkeiksi
import html 


# Avataan kysymykset luettavassa muodossa muuttujaan data. Käytetään encoding koska tiedosto sisältää
#muitakin kuin ASCII-merkkejä

with open("./json/questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)



# Määritetään vaikeusaste
def ask_difficulty():

    print(f"Select difficulty level:")
    print(f"1. Easy")
    print(f"2. Medium")
    print(f"3. Hard\n")
    
    # Määritellään vaikeusasteet
    difficulty_levels = {1: "easy", 2: "medium", 3: "hard"}

    #user_choice = (input("Enter the number corresponding to your choice: "))

    # Tarkistetaan, että käyttäjän valinta on oikein ja palautetaan valittu vaikeusaste
    while True:
        try:
            user_choice = int(input(f"Enter the number corresponding to your choice: "))
            if 1 <= user_choice <= 3:
                break
            print(f"Wrong input, try!")
        except KeyboardInterrupt: 
            break
        except: 
            print(f"Wrong input, try again!")
        
            
            
            


        
    # Palauttaa valitun vaikeusasteen
    return difficulty_levels[user_choice]


# Määritetään kategoria kysymyksille
def ask_category():

    categories = [
    "General Knowledge",
    "Entertainment: Books",
    "Entertainment: Film",
    "Entertainment: Music",
    "Entertainment: Musicals & Theatres",
    "Entertainment: Television",
    "Entertainment: Video Games",
    "Entertainment: Board games",
    "Entertainment: Comics",
    "Entertainment: Anime & Manga",
    "Entertainment: Cartoon & Animation",
    "Science &amp; Nature",
    "Science: Computers",
    "Science: Mathematics",
    "Science: Gadgets",
    "Mythology",
    "Sports",
    "Geography",
    "History",
    "Politics",
    "Art",
    "Celebrities",
    "Animals",
    "Vehicles"
    ]

    # Tulostetaan ja numeroidaan kaikki listassa olevat kategoriat
    print(f"\nAvailable categories for questions: ")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")


    # Kysytään kategoriaa niin kauan kunnes annettu vastaus on joku numeron 1 ja 22 väliltä
    while True:
        try:
            select_category = int(input(f"Enter the number corresponding to your choice: "))
            if 1 <= select_category <= 24:
                break
            print(f"Wrong input, try again!")
        except KeyboardInterrupt: 
            break
        except: 
            print(f"Wrong input, try again!")

    
    # Palautetaan valittu kategoria, miinustetaan siitä 1 koska listan tulostuksessa lisättiin numeroinnin takia 1
    return categories[select_category -1]


        

# Funktio, joka kysyy satunnaisen kysymyksen valitun vaikeusasteen mukaan
def get_questions(difficulty:str, category:str):
    # Suodatetaan kysymykset valitun vaikeusasteen mukaan
    selected_questions = [question for question in data if question["difficulty"] == difficulty and question["category"] == category]
    return selected_questions


# Funktio, joka kysyy käyttäjältä satunnaisen kysymyksen ja tarkistaa vastauksen
def ask_question(questions:list):
    # Valitaan satunnainen kysymys
    question = random.choice(questions)

    # Haetaan kysymysteksti ja vastaukset
    question_text = html.unescape(question["question"])
    correct_answer = html.unescape(question["correct_answer"])
    incorrect_answers = [html.unescape(answer) for answer in question["incorrect_answers"]]
    
    # Yhdistetään vastaukset ja sekoitetaan ne, oikea vastaus pitää lisätä listaan että sen voi yhdistää väärien vastauksien listaan
    answers = incorrect_answers + [correct_answer]
    random.shuffle(answers)
    previous_question = [answers, correct_answer, question_text]

    # Tulostetaan kysymys ja vaihtoehdot. Enumerate numeroi jokaisen listan alkoin, alkaen numerosta 1.
    print(f"\nQuestion: {question_text}\nOptions:\n")
    for i, answer in enumerate(answers, 1):
        print(f"{i}. {answer}")
        

    # Kysytään käyttäjältä valinta
    while True:
        try:
            user_answer = int(input(f"Select the right answer: "))
            if 1 <= user_answer <= len(answers):
                break
            else:
                print(f"Wrong input, try again!")
        except ValueError:
            print(f"Wrong input, try again!")

    
    # Tarkistetaan, onko valittu vastaus oikea. Pitää laittaa -1 edellisessä for silmukassa lisättiin yksi numeroinnin takia
    if answers[user_answer - 1] == correct_answer:
        #print(f"\nCorrect!")
        return True, previous_question# Oikea vastaus
    else:
        #print(f"\nWrong! The correct answer was: {correct_answer}")
        return False, previous_question  # Väärä vastaus
    
def ask_again(previous_question):
    answers, correct_answer, question_text = previous_question

    print(f"\nQuestion: {question_text}\nOptions:\n")
    for i, answer in enumerate(answers, 1):
        print(f"{i}. {answer}")


    while True:
        try:
            user_answer = int(input(f"Select the right answer: "))
            if 1 <= user_answer <= len(answers):
                break
            else:
                print(f"Wrong input, try again!")
        except ValueError:
            print(f"Wrong input, try again!")
    
    if answers[user_answer - 1] == correct_answer:
        #print(f"\nCorrect!")
        return True # Oikea vastaus
    else:
        #print(f"\nWrong! The correct answer was: {correct_answer}")
        return False  # Väärä vastaus




# takes following parameters:
#   1. boolean (from ask_question() -function)
#       True    ->    return ICAO for the next location in the criminal-table the player has not visited yet 
#       False   ->    return random ICAO (not player's current location and not found in criminal-table)
#   2. Player's current location (ICAO-code)


def quiz_icao(ask_question_bool:bool, game_dict:dict):
    player_location = game_dict["player_location"]
    cursor = mysql_connection.cursor()

    if ask_question_bool == True:# we'll get right ICAO-code
        sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchone()
        if type(result) == tuple: # if the sql query returns a value
            game_dict["next_location_bool"] = True
            print(f"The next location is: {result[0]}")


    elif ask_question_bool == False:# we'll get wrong ICAO-code
        sql = f"SELECT ident FROM airport WHERE continent = 'EU' AND type = 'large_airport' AND name LIKE '%airport' AND ident NOT IN (SELECT location FROM criminal) AND ident != '{player_location}' ORDER BY RAND() LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchone()
        if type(result) == tuple: # if the sql query returns a value
            game_dict["next_location_bool"] = True
            print(f"The next location is: {result[0]}")


# Testataan koodin toimivuus kolmella kysymyksellä
def practice_quiz():

    x = int(input(f"How many questions would you like to practice?: "))
    # Kysytään vaikeusaste käyttäjältä
    chosen_difficulty = ask_difficulty()

    # Kysytään haluttu kategoria
    choosen_category = ask_category()
    
    # Hae kysymykset valitun vaikeusasteen mukaan
    questions = get_questions(chosen_difficulty, choosen_category)
    
    # Pelaaja vastaa kolmeen kysymykseen
    score = 0
    for _ in range(x):
        boolean, previous_question = ask_question(questions) 
        if boolean:
            score += 1
            print(f"\nCorrect!")
        else:
            print(f"\nWrong! The correct answer was: {previous_question[1]}")

            

    # Peli päättyy
    print(f"Your score: {score}/{x}! ")

# Käynnistetään peli
if __name__ == "__main__": # testikoodi main blockin sisällä, jotta sitä ei ajeta heti importin yhteydessä
    practice_quiz()




