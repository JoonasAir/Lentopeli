import os
import psutil
import requests
from geopy import distance
from flask_cors import CORS
from stop_game import stop_game
from game_setup import game_setup
from criminal import criminal_timer
from security import talk_to_security
from flask import Flask, request, jsonify
from multiprocessing import Event, Process
from game_parameters import game_parameters
from airport_menu import airport_menu_input
from mysql_connection import mysql_connection
from questions import ask_question, get_questions


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


# Leaderboard haku
@app.route("/leaderboard")
def leaderboard():
    sql = "SELECT screen_name, points FROM leaderboard ORDER BY points DESC;"
    kursori = mysql_connection.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    
    results = []
    for rivi in tulos:
        result = {"Name": rivi[0],
                "Points": rivi[1]}
        results.append(result)
        
    return jsonify(results)
    

# tehdään game_dict ja palautetaan game.js:ään
@app.route("/gameSetup", methods=['POST'])
def gameSetup():
    data = request.json
    game_dict = game_setup(game_parameters, data)
    game_dict["quiz_questions"] = get_questions(game_dict["quiz_difficulty"], game_dict["quiz_category"])
    return jsonify({"message": "Game setup received successfully", "data": game_dict}), 200


# haetaan lentokentän nimi ja maa ICAO:lla
@app.route('/location')
def print_location():
    cursor = mysql_connection.cursor()
    sql = "SELECT location FROM criminal WHERE visited = 1 ORDER BY id DESC LIMIT 1;"
    cursor.execute(sql)
    icao = cursor.fetchone()[0]
    cursor = mysql_connection.cursor(dictionary=True)
    sql = f"SELECT country.name AS country, airport.name AS airport FROM airport, country WHERE country.iso_country = airport.iso_country AND airport.ident = '{icao}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    location = f"{result['airport']}, {result['country']}"
    return jsonify(location)


# taustaprosessina juokseva ajastin joka lisää X ajan välein uuden sijainnin rikollisen tietokanta-tauluun
ProcessCriminalTimer = None
stop_event = Event()

# käynnistetään ajastin
@app.route('/startCriminalTimer', methods=['POST'])
def startCriminalTimer():
    time = request.json
    try: cleanup_processes()
    except: pass
    global ProcessCriminalTimer, stop_event
 # Defining a background process that runs criminal_timer -function
    ProcessCriminalTimer = Process(target=criminal_timer, args=(time, stop_event))
 # Start the process
    ProcessCriminalTimer.start()

    return jsonify({"status": "Timer started"})

# pysäytetään ajastin
@app.route('/stopCriminalTimer')
def cleanup_processes():
    try: 
        current_pid = os.getpid()
        current_process = psutil.Process(current_pid)
        for child in current_process.children(recursive=True):
            child.terminate()
            child.wait()
        return jsonify({"message":"Process terminated succesfully"})
    except: return jsonify({"message":"An error occurred while trying to terminate process"})


# haetaan sijaintimme ja määränpäämme koordinaatit
@app.route("/flyto", methods=['PUT'])
def get_location():
    data = request.json
    try: data = data["data"]
    except: pass

    cursor1 = mysql_connection.cursor()
    sqlfrom = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{data["player_location"]}'"
    cursor1.execute(sqlfrom)
    flyfrom = cursor1.fetchall()

    cursor2 = mysql_connection.cursor()
    sqlto = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{data["next_location"]}'"
    cursor2.execute(sqlto)
    flyto = cursor2.fetchall()

    if not flyfrom or not flyto:
        return jsonify({"error": "No data found"}), 404
    result = {
        "from": {"latitude": flyfrom[0][0], "longitude": flyfrom[0][1]},
        "to": {"latitude": flyto[0][0], "longitude": flyto[0][1]}
    }
    return jsonify(result)


# tarkistetaan täyttyykö edellytykset pelin päättämiselle
@app.route('/stopGame', methods=['POST'])
def stopGame():
    data = request.json
    try:
        data = data["data"]
    except:
        pass

    returnValue = stop_game(data)

    if returnValue:
        return jsonify({"message": "Game ends now", "data": True}), 200
    else:
        return jsonify({"message": "Game continues", "data": False}), 200


# haetaan lentokentän toiminto-vaihtoehdot
@app.route('/airportOptions', methods=['POST'])
def airportOptions():
    game_dict = request.json
    try:
        game_dict = game_dict["data"]
    except:
        pass
    finally:
        game_dict = airport_menu_input(game_dict)
        
    try:
        return jsonify({'message':"Airport menu options returned", 'data': game_dict["data"]})
    except:
        return jsonify({'message':"Airport menu options returned", 'data': game_dict})
    
    
# jos pelaaja valitsee random-toiminnon lentokentällä, tämä funktio kertoo mitä tapahtuu seuraavaksi
@app.route('/randomLuck', methods=['POST'])
def randomLuck():
    cursor = mysql_connection.cursor()
    game_dict = request.json
    try: game_dict = game_dict["data"]
    except: pass
    game_dict["game_output"] = []
    if game_dict["tried_luck"]: # jos pelaaja on koittanut onneaan kyseisellä lentokentällä
            game_dict["game_output"].append(f"{game_dict["airport_options"][2]["text"][3]}")
    else:
        game_dict["tried_luck"] = True
        if game_dict["random_luck_bool"]: # jos käy tuuri
            sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
            cursor.execute(sql)
            result = cursor.fetchone()
            if type(result) == tuple: 
                game_dict['correct_location'] = True
                game_dict["game_output"].append(game_dict["airport_options"][2]["text"][1])
                game_dict["next_location_bool"] = True
                game_dict["next_location"] = result[0]
        else: # jos ei käy tuuri
            game_dict["game_output"].append(f"{game_dict["airport_options"][2]["text"][2]}\n" )

    return game_dict


# tarkistetaan olemmeko samalla kentällä rikollisen kanssa
@app.route('/criminalCaught')
def criminalCaught():
    try:
        cursor = mysql_connection.cursor()
        sql1 = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
        cursor.execute(sql1)
        criminal_location = cursor.fetchone()
        if criminal_location is None:
            return jsonify(True)
        elif criminal_location[0] == "":
            return jsonify(True)
        else:
            return jsonify(False)
    except Exception as e:
        print(f"Error in /criminalCaught: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    
# jos pelaaja valitsee lentokentällä puhua turvallisuuspäällikölle
@app.route('/talkToSecurity', methods=['POST'])
def talkToSecurity():
    game_dict = request.json
    try: game_dict = game_dict["data"]
    except: pass
    game_dict = talk_to_security(game_dict)
    
    return game_dict


# jos pelaaja haluaa ratkaista vihjeen lentokentällä
@app.route('/solveClue', methods=['POST'])
def solveClue():
    game_dict = request.json
    try: game_dict = game_dict["data"]
    except: pass
    game_dict = ask_question(game_dict)
    
    return game_dict
    

# palautetaan oikea tai väärä seuraava sijainti sen mukaan vastasiko pelaaja kysymykseen oikein vai väärin
@app.route('/nextLocation', methods=['POST'])
def solvePreviousClue():
    game_dict = request.json
    cursor = mysql_connection.cursor()
    if game_dict["previous_quiz_answer"]:
        sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchone()
        game_dict['correct_location'] = True
    else: 
        sql = "SELECT ident FROM airport WHERE continent = 'EU' AND type = 'large_airport' AND airport.name LIKE '%Airport' AND ident NOT IN (SELECT location FROM criminal) ORDER BY RAND() LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchone()
        game_dict['correct_location'] = False
    game_dict["next_location"] = result[0]
    game_dict["next_location_bool"] = True

    return game_dict


# päivitetään tietokannan criminal -tauluun sijaintimme kohdalle visited -sarake 0 -> 1 
@app.route('/updateToVisited', methods=['POST'])
def updateToVisited():
    location = request.json
    if not mysql_connection.is_connected():
        mysql_connection.reconnect()
    cursor = mysql_connection.cursor()
    sql_select = """
    SELECT id
    FROM criminal
    WHERE visited = 0 AND location = %s
    LIMIT 1;
    """
    cursor.execute(sql_select, (location,))
    result = cursor.fetchone()
    if result:
        criminal_id = result[0]
        sql_update = """
        UPDATE criminal
        SET visited = 1
        WHERE id = %s;
        """
        cursor.execute(sql_update, (criminal_id,))
        return jsonify({"message": "Updated", "value": True})
    else:
        return jsonify({"message": "No matching record found", "value": False}), 404


# haetaan säätiedot 
@app.route('/weather', methods=["POST"])
def getTemp():
    coordinates = request.json
    API_KEY = "f23df786656104dd27426c1f6b2a0c82"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={coordinates[0]}&lon={coordinates[1]}&appid={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp_kelvin = data['main']['temp']
            temp_celcius = temp_kelvin - 273.15
            rounded_temp = round(temp_celcius)
            
            result = {
                'icon': data['weather'][0]['icon'],
                'temp': rounded_temp, 
                'desc': data['weather'][0]['description'],
            }
            return jsonify(result)
    except requests.exceptions.RequestException as e:
        print("Hakua ei voitu suorittaa.")      


## CO2 laskuri, ottaa koordinaatit routes listasta johon upataan koordinaatit aina kun lennetään. 
## Index 0 pelaaja, index 1 rikollinen
@app.route('/co2distance', methods=['POST'])
def calculateCO2():
    data = request.json
    routes = data["routes"]
    coord1 = tuple(routes[-1][0])
    coord2 = tuple(routes[-1][1])
    distanceKM = round(distance.distance(coord1, coord2).km)
    co2 = round(distanceKM * 0.15) 
    result = {
        'co2':co2,
        'distanceKM':distanceKM
    }
    return jsonify(result)


if __name__ == "__main__":
   app.run(debug=True)