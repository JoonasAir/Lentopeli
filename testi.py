import mysql_connector

try:
    conn = mysql.connector.connect(
        host="localhost",  # tai käytä oikeaa MySQL-palvelimen IP-osoitetta
        user="joonas",  # tai käytä oikeaa käyttäjätunnusta
        password="lentopeli",  # korvaa oikealla salasanalla
        database="test_db"  # korvaa oikealla tietokannan nimellä
    )
    print("Yhteys onnistui!")
    conn.close()
except mysql.connector.Error as err:
    print(f"Virhe: {err}")
