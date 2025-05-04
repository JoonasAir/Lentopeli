from mysql_connection import mysql_connection
from flask import Flask, request, jsonify
from flask_cors import CORS
from game_setup import game_setup
from game_parameters import game_parameters
from questions import get_questions
import json

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


@app.route("/flyto", methods=['PUT'])
def get_location():
    data = request.json["data"]

    cursor1 = mysql_connection.cursor()
    cursor2 = mysql_connection.cursor()
    sqlfrom = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident='{data["player_location"]}'"
    sqlto = "SELECT latitude_deg, longitude_deg FROM airport WHERE ident='EHAM'"

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


if __name__ == "__main__":
   app.run(debug=True)