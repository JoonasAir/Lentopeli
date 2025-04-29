from mysql_connection import mysql_connection
from flask import Flask, jsonify
from flask_cors import CORS

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
    
   



if __name__ == "__main__":
   app.run(debug=True)