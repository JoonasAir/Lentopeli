from mysql_connection import mysql_connection
from flask import Flask, request, jsonify
from flask_cors import CORS
from game_setup import game_setup
from game_parameters import game_parameters
from airport_menu import airport_menu_input
from questions import get_questions
from stop_game import stop_game
import json

app = Flask(__name__)
CORS(app)
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
        data = data["value"]
    except:
        pass

    returnValue = stop_game(data)

    if returnValue:
        return jsonify({"message": "Game ends now", "value": True}), 200
    else:
        return jsonify({"message": "Game continues", "value": False}), 200



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
        return jsonify({'message':"Airport menu options returned", 'value': game_dict["data"]})
    except:
        return jsonify({'message':"Airport menu options returned", 'value': game_dict})



if __name__ == "__main__":
   app.run(debug=True)