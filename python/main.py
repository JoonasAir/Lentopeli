from multiprocessing import Event, Process
from mysql_connection import mysql_connection
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from game_setup import game_setup
from game_parameters import game_parameters
from airport_menu import airport_menu_input
from security import talk_to_security
from questions import ask_question, get_questions, quiz_icao
from stop_game import stop_game
from criminal import criminal_timer
from geopy import distance

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



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
    


# create game_dict and return to game.js
@app.route("/gameSetup", methods=['POST'])
def gameSetup():
    data = request.json
    game_dict = game_setup(game_parameters, data)
    game_dict["quiz_questions"] = get_questions(game_dict["quiz_difficulty"], game_dict["quiz_category"])
    return jsonify({"message": "Game setup received successfully", "data": game_dict}), 200



@app.route('/location', methods=['POST'])
def print_location():
    icao = request.json
    cursor = mysql_connection.cursor(dictionary=True)
    sql = f"SELECT country.name AS country, airport.name AS airport FROM airport, country WHERE country.iso_country = airport.iso_country AND airport.ident = '{icao}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    location = f"{result['airport']}, {result['country']}"
    return jsonify(location)




ProcessCriminalTimer = None
stop_event = Event()

@app.route('/startCriminalTimer', methods=['POST'])
def startCriminalTimer():
    time = request.json
    global ProcessCriminalTimer, stop_event
 # Defining a background process that runs criminal_timer -function
    ProcessCriminalTimer = Process(target=criminal_timer, args=(time, stop_event))
 # Start the process
    ProcessCriminalTimer.start()

    return {"status": "Timer started"}

@app.route('/stopCriminalTimer')
def stopCriminalTimer():
    global ProcessCriminalTimer, stop_event

    if ProcessCriminalTimer and ProcessCriminalTimer.is_alive():
 # Terminate the criminal_timer -background process
        stop_event.set()
        ProcessCriminalTimer.terminate()
 # Ensures that the main program waits for the terminated process to clean up properly before continuing
        ProcessCriminalTimer.join()
        ProcessCriminalTimer = None
        return {"status": "Timer stopped"}
    else:
        return {"status": "No timer running"}



@app.route("/flyto", methods=['PUT'])
def get_location():
    data = request.json
    try: data = data["data"]
    except: pass
    cursor1 = mysql_connection.cursor()
    cursor2 = mysql_connection.cursor()
    sqlto = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{data["next_location"]}'"

    sqlfrom = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{data["player_location"]}'"


    cursor1.execute(sqlfrom)
    flyfrom = cursor1.fetchall()

    cursor2.execute(sqlto)
    flyto = cursor2.fetchall()

    if not flyfrom or not flyto:
        return jsonify({"error": "No data found"}), 404

    result = {
        "from": {"latitude": flyfrom[0][0], "longitude": flyfrom[0][1]},
        "to": {"latitude": flyto[0][0], "longitude": flyto[0][1]}
    }
    return jsonify(result)



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
    
    

@app.route('/randomLuck', methods=['POST'])
def randomLuck():
    cursor = mysql_connection.cursor()
    game_dict = request.json
    try: game_dict = game_dict["data"]
    except: pass
    game_dict["game_output"] = []
    if game_dict["tried_luck"]: # if we have tried our luck at current airport
            game_dict["game_output"].append(f"{game_dict["airport_options"][2]["text"][3]}")
    else:
        game_dict["tried_luck"] = True
        if game_dict["random_luck_bool"]:
            sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
            cursor.execute(sql)
            result = cursor.fetchone()
            if type(result) == tuple:
                game_dict['correct_location'] = True
                game_dict["game_output"].append(game_dict["airport_options"][2]["text"][1])
                game_dict["next_location_bool"] = True
                game_dict["next_location"] = result[0]
            else: 
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@\nsaimme(ko?) rikollisen kiinni \n@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        else:
            game_dict["game_output"].append(f"{game_dict["airport_options"][2]["text"][2]}\n" )

    return game_dict


@app.route('/talkToSecurity', methods=['POST'])
def talkToSecurity():
    game_dict = request.json
    try: game_dict = game_dict["data"]
    except: pass
    game_dict = talk_to_security(game_dict)
    
    return game_dict


@app.route('/solveClue', methods=['POST'])
def solveClue():
    game_dict = request.json
    try: game_dict = game_dict["data"]
    except: pass
    game_dict = ask_question(game_dict)
    
    return game_dict

    
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
    index = data["index"] #  0 = player  -  1 = criminal

    coord1 = tuple(routes[-1][index])
    coord2 = tuple(routes[-2][index])
    distanceKM = round(distance.distance(coord1, coord2).km)
    co2 = round(distanceKM * 0.15) 
    result = {
        'co2':co2,
        'distanceKM':distanceKM
    }
    return jsonify(result)


if __name__ == "__main__":
   app.run(debug=True)