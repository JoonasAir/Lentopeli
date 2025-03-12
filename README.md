# CatchTheCriminal - Europe Edition

### works at least with python version 3.13.1
## Install needed third-party-packages
### Run following command in terminal, at *root* directory of the game
```
pip install -r requirements.txt
```

## Prepare database for the game (with **root** account)
### Copy/paste following commands in your **flight_game** -database

#### Delete **goal_reached** table
```
DROP TABLE goal_reached;
```

#### Delete **game** table
```
DROP TABLE game;
```

#### Delete **goal** table
```
DROP TABLE goal;
```

#### Create **criminal** table
```
CREATE TABLE criminal (ID INT AUTO_INCREMENT PRIMARY KEY, Location VARCHAR(255), Visited INT DEFAULT 0);
```

#### Create **leaderboard** table
```
CREATE TABLE leaderboard (ID INT AUTO_INCREMENT PRIMARY KEY, screen_name VARCHAR(255), points INT);
```


#### Grant privileges (Replace **YOUR_USERNAME** with your actual MariaDB-username.)
```
GRANT SELECT, INSERT, UPDATE ON "flight_game".* TO "YOUR_USERNAME"@"localhost"; # Replace YOUR_USERNAME with your MariaDB-username.
```

#### Grant privileges (Replace **YOUR_USERNAME** with your actual MariaDB-username.)
```
GRANT DELETE, ALTER ON "flight_game"."criminal" TO "YOUR_USERNAME"@"localhost"; # Replace YOUR_USERNAME with your MariaDB-username.
```

#### Flush privileges

```
FLUSH PRIVILEGES;
```


## Connection

### Create file 'mysql_connection.py' and copy following code into it. 
Replace **YOUR_USERNAME** and **YOUR_PASSWORD** with your actual MariaDB username and password.
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
