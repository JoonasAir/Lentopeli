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


# Määritetään vaikeusaste
def ask_difficulty():
    print("Select difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard\n")
    
    user_choice = int(input("Choose your difficulty level:\n"))
    
    # Määritellään vaikeusasteet
    difficulty_levels = {1: "easy", 2: "medium", 3: "hard\n"}

    # Tarkistetaan, että käyttäjän valinta on oikein ja palautetaan valittu vaikeusaste
    while user_choice not in difficulty_levels:
        print("Invalid choice, please try again!")
        user_choice = int(input("Enter the number corresponding to your choice: "))
    # Palauttaa valitun vaikeusasteen
    return difficulty_levels[user_choice]


# Määritetään kategoria kysymyksille
def ask_category():

    categories = [
    "General Knowledge",
    "Entertainment: Books",
    "Entertainment: Movies",
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

    # Kysytään kategoriaa niin kauan kunnes annettu vastaus on joku numeron 1 ja listan pituuden väliltä
    select_category = int(input("Choose your category: "))
    while select_category < 1 or select_category > len(categories):
        print("Invalid choise. Please choose again!")
        select_category = int(input("Choose your category: "))

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
    user_answer = int(input("Select the right answer: "))

    # Tarkistetaan, onko valittu vastaus oikea. Pitää laittaa -1 edellisessä for silmukassa lisättiin yksi numeroinnin takia
    if answers[user_answer - 1] == correct_answer:
        print("\nCorrect!")
        return True  # Oikea vastaus
    else:
        print(f"\nWrong! The correct answer was: {correct_answer}")
        return False  # Väärä vastaus


# Testataan koodin toimivuus kolmella kysymyksellä
def start_game():
    # Kysytään vaikeusaste käyttäjältä
    chosen_difficulty = ask_difficulty()

    choosen_category = ask_category()
    
    # Hae kysymykset valitun vaikeusasteen mukaan
    questions = get_questions(chosen_difficulty, choosen_category)
    
    # Pelaaja vastaa kolmeen kysymykseen
    score = 0
    for _ in range(3):  # Voit muuttaa montako kysymystä haluat
        if ask_question(questions):
            score += 1

    # Peli päättyy
    print(f"Your score: {score}/3")

# Käynnistetään peli
start_game()




