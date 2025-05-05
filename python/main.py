from urllib import response
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
import json
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
    location =  f"{result['airport']}, {result['country']}."
    return jsonify(location)



@app.route("/flyto", methods=['PUT'])
def get_location():
    data = request.json

    cursor1 = mysql_connection.cursor()
    cursor2 = mysql_connection.cursor()
    sqlto = "SELECT latitude_deg, longitude_deg FROM airport WHERE ident='EHAM'"
    try: 
        sqlfrom = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{data["data"]["player_location"]}'"
    except:
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
            game_dict["next_location_bool"] = True
            sql = "SELECT location FROM criminal WHERE visited = 0 LIMIT 1;"
            cursor.execute(sql)
            result = cursor.fetchone()
            if type(result) == tuple:
                longtext = game_dict["airport_options"][2]["text"][1]
                game_dict["game_output"].append(f"{longtext}\n" )
                game_dict["next_location_bool"] = True
                game_dict["next_location"] = result[0]
                game_dict["game_output"].append(f"The next location is: {result[0]}" )
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



# @app.route('/solvePreviousClue', methods=['POST'])
# def solvePreviousClue():
#     game_dict = request.json




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