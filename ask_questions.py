# Voidaan käyttää json tiedostoa missä kysymykset
import json

# Voidaan valita satunnaisia kysymyksiä sekä sekoitta vastausvaihtoehdot
import random 

# Voidaan muuttaa kysymysten HTML elementit oikeiksi merkeiksi
import html 

# Avataan kysymykset luettavassa muodossa muuttujaan data. Käytetään encoding koska tiedosto sisältää
#muitakin kuin ASCII-merkkejä
with open("questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)


def ask_difficulty():
    print("Select difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    
    user_choice = int(input("Enter the number corresponding to your choice: "))
    
    # Määritellään vaikeusasteet
    difficulty_levels = {1: "easy", 2: "medium", 3: "hard"}

    # Tarkistetaan, että käyttäjän valinta on oikein ja palautetaan valittu vaikeusaste
    while user_choice not in difficulty_levels:
        print("Invalid choice, please try again!")
        user_choice = int(input("Enter the number corresponding to your choice: "))
    # Palauttaa valitun vaikeusasteen
    return difficulty_levels[user_choice]

# Funktio, joka kysyy satunnaisen kysymyksen valitun vaikeusasteen mukaan
def get_questions(difficulty):
    # Suodatetaan kysymykset valitun vaikeusasteen mukaan
    selected_questions = [question for question in data if question["difficulty"] == difficulty]
    return selected_questions

# Funktio, joka kysyy käyttäjältä satunnaisen kysymyksen ja tarkistaa vastauksen
def ask_question(questions):
    # Valitaan satunnainen kysymys
    question = random.choice(questions)

    # Haetaan kysymysteksti ja vastaukset
    question_text = html.unescape(question["question"])
    correct_answer = html.unescape(question["correct_answer"])
    incorrect_answers = [html.unescape(answer) for answer in question["incorrect_answers"]]
    
    # Yhdistetään vastaukset ja sekoitetaan ne
    answers = incorrect_answers + [correct_answer]
    random.shuffle(answers)

    # Tulostetaan kysymys ja vaihtoehdot
    print(f"Question: {question_text}\nOptions:")
    for i, answer in enumerate(answers, 1):
        print(f"{i}. {answer}")

    # Kysytään käyttäjältä valinta
    user_answer = int(input("Select the right answer: "))

    # Tarkistetaan, onko valittu vastaus oikea
    if answers[user_answer - 1] == correct_answer:
        print("Correct!")
        return True  # Oikea vastaus
    else:
        print(f"Wrong! The correct answer was: {correct_answer}")
        return False  # Väärä vastaus

def start_game():
    # Kysytään vaikeusaste käyttäjältä
    chosen_difficulty = ask_difficulty()
    
    # Hae kysymykset valitun vaikeusasteen mukaan
    questions = get_questions(chosen_difficulty)
    
    # Pelaaja vastaa kolmeen kysymykseen
    score = 0
    for _ in range(3):  # Voit muuttaa montako kysymystä haluat
        if ask_question(questions):
            score += 1

    # Peli päättyy
    print(f"Your score: {score}/3")

# Käynnistetään peli
start_game()




