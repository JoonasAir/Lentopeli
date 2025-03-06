# Voidaan käyttää json tiedostoa missä kysymykset
import json
import time
#import threading
# Voidaan valita satunnaisia kysymyksiä sekä sekoitta vastausvaihtoehdot
import random 
# Voidaan muuttaa kysymysten HTML elementit oikeiksi merkeiksi
import html 
#import game_timer
#from game_setup import game_setup


# Avataan kysymykset luettavassa muodossa muuttujaan data. Käytetään encoding koska tiedosto sisältää
#muitakin kuin ASCII-merkkejä
with open("questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)




# Määritetään vaikeusaste
def ask_difficulty():
    print("Select difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard\n")
    
    # Määritellään vaikeusasteet
    difficulty_levels = {1: "easy", 2: "medium", 3: "hard"}

    #user_choice = (input("Enter the number corresponding to your choice: "))

    # Tarkistetaan, että käyttäjän valinta on oikein ja palautetaan valittu vaikeusaste
    while True:
        try:
            user_choice = int(input("Enter the number corresponding to your choice: "))
            if 1 <= user_choice <= 3:
                break
            print("Wrong input, try!")
        except KeyboardInterrupt: 
            break
        except: 
            print("Wrong input, try again!")
        
            
            
            


        
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
    "Science & Nature",
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
    print("\nAvailable categories for questions: ")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")


    # Kysytään kategoriaa niin kauan kunnes annettu vastaus on joku numeron 1 ja 22 väliltä
    while True:
        try:
            select_category = int(input("Enter the number corresponding to your choice: "))
            if 1 <= select_category <= 24:
                break
            print("Wrong input, try again!")
        except KeyboardInterrupt: 
            break
        except: 
            print("Wrong input, try again!")

    
    # Palautetaan valittu kategoria, miinustetaan siitä 1 koska listan tulostuksessa lisättiin numeroinnin takia 1
    return categories[select_category -1]


        

# Funktio, joka kysyy satunnaisen kysymyksen valitun vaikeusasteen mukaan
def get_questions(difficulty, category):
    # Suodatetaan kysymykset valitun vaikeusasteen mukaan
    selected_questions = [question for question in data if question["difficulty"] == difficulty and question["category"] == category]
    return selected_questions


# Funktio, joka kysyy käyttäjältä satunnaisen kysymyksen ja tarkistaa vastauksen
def ask_question(questions):
    # Valitaan satunnainen kysymys
    question = random.choice(questions)

    # Haetaan kysymysteksti ja vastaukset
    question_text = html.unescape(question["question"])
    correct_answer = html.unescape(question["correct_answer"])
    incorrect_answers = [html.unescape(answer) for answer in question["incorrect_answers"]]
    
    # Yhdistetään vastaukset ja sekoitetaan ne, oikea vastaus pitää lisätä listaan että sen voi yhdistää väärien vastauksien listaan
    answers = incorrect_answers + [correct_answer]
    random.shuffle(answers)

    # Tulostetaan kysymys ja vaihtoehdot. Enumerate numeroi jokaisen listan alkoin, alkaen numerosta 1.
    print(f"\nQuestion: {question_text}\nOptions:\n")
    for i, answer in enumerate(answers, 1):
        print(f"{i}. {answer}")

    # Kysytään käyttäjältä valinta
    while True:
        try:
            user_answer = int(input("Select the right answer: "))
            if 1 <= user_answer <= len(answers):
                break
            else:
                print("Wrong input, try again!")
        except ValueError:
            print("Wrong input, try again!")

    
    # Tarkistetaan, onko valittu vastaus oikea. Pitää laittaa -1 edellisessä for silmukassa lisättiin yksi numeroinnin takia
    if answers[user_answer - 1] == correct_answer:
        print("\nCorrect!")
        return True  # Oikea vastaus
    else:
        print(f"\nWrong! The correct answer was: {correct_answer}")
        return False  # Väärä vastaus


# Testataan koodin toimivuus kolmella kysymyksellä
def practice_quiz():

    x = int(input("How many questions would you like to practice?: "))
    # Kysytään vaikeusaste käyttäjältä
    chosen_difficulty = ask_difficulty()

    # Kysytään haluttu kategoria
    choosen_category = ask_category()
    
    # Hae kysymykset valitun vaikeusasteen mukaan
    questions = get_questions(chosen_difficulty, choosen_category)
    
    # Pelaaja vastaa kolmeen kysymykseen
    score = 0
    for _ in range(x):  # Voit muuttaa montako kysymystä haluat
        if ask_question(questions):
            score += 1

    # Peli päättyy
    print(f"Your score: {score}/{x}")

# Käynnistetään peli
if __name__ == "__main__": # testikoodi main blockin sisällä, jotta sitä ei ajeta heti importin yhteydessä
    practice_quiz()




