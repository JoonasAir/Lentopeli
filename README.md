# CatchTheCriminal - ## Europe Edition


## Install needed third-party-packages
### Run following command on root directory of the game
`pip install -r requirements.txt`

## Database
### Commands for modifying existing flight_game database:

`DROP TABLE goal_reached;`
`DROP TABLE game;`
`DROP TABLE goal;`
`CREATE TABLE criminal (ID INT AUTO_INCREMENT PRIMARY KEY, Location VARCHAR(255), Visited INT DEFAULT 0);`
`CREATE TABLE leaderboard (ID INT AUTO_INCREMENT PRIMARY KEY, screen_name VARCHAR(255), points INT);`


### Grant needed privileges for your MariaDB-user
`GRANT SELECT, INSERT, UPDATE ON "flight_game".* TO "YOUR_USERNAME"@"localhost"; # Replace YOUR_USERNAME with your MariaDB-username.`
`GRANT DELETE, ALTER ON "flight_game"."criminal" TO "YOUR_USERNAME"@"localhost"; # Replace YOUR_USERNAME with your MariaDB-username.`
`FLUSH PRIVILEGES;`

## Connection

# The file 'mysql_connection.py' is not pushed to github since the file is found in '.gitignore' file. 
# Create file 'mysql_connection.py' and copy following code into it. 
```
import mysql.connector

mysql_connection = mysql.connector.connect(
    collation = "utf8mb4_general_ci",
    host = '127.0.0.1',
    port = 3306,
    database = "flight_game",
    user = "YOUR_USERNAME", # Replace YOUR_USERNAME with your MariaDB-username.
    password = "YOUR_PASSWORD", # Replace YOUR_PASSWORD with your MariaDB-password.
    autocommit = True
)
```
