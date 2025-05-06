"use strict";

const baseUrl = "http://127.0.0.1:5000";

const queryString = window.location.search;

const urlParams = new URLSearchParams(queryString);

const name_input = urlParams.get("username");
const difficulty_input = urlParams.get("difficulty");
const category_input = urlParams.get("category");

const dataToFlask = {
  name_input: name_input,
  difficulty_input: difficulty_input,
  category_input: category_input,
};

// Game timer
const timerElement = document.getElementById("timer");
const timerEndEvent = new Event("timerEnd");
let timerInterval;

function updateTimer(countdownTime) {
  const minutes = Math.floor(countdownTime / 60);
  const seconds = countdownTime % 60;

  timerElement.textContent = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  if (countdownTime > 0) {
    countdownTime--; // Vähennetään sekunti
  } else {
    clearInterval(timerInterval); // Lopetetaan ajastus
    document.dispatchEvent(timerEndEvent); // Lähetetään "timerEnd" tapahtuma
  }
  return countdownTime;
}

// Käynnistää ajastimen (vain kun peli alkaa tai nollataan)
function startTimer(countdownTime) {
  clearInterval(timerInterval); // Estetään päällekkäiset ajastimet
  timerInterval = setInterval(() => {
    countdownTime = updateTimer(countdownTime); // Päivitetään countdownTime sekuntin välein
  }, 1000);
  updateTimer(countdownTime); // Päivitetään heti, jotta käyttäjä näkee ajan muutoksen
}

// Käyttäjän syöttämien aloitustietojen haku
// ja pelin parametrien luonti palvelimella
async function gameSetup() {
  try {
    const response = await fetch(baseUrl + "/gameSetup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dataToFlask),
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
  }
}

function startCriminalTimer(time) {
  try {
    const response = fetch(baseUrl + "/startCriminalTimer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(time),
    });
    data = response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
  }
}

function stopCriminalTimer() {
  try {
    fetch(baseUrl + "/stopCriminalTimer");
  } catch (error) {
    console.error("Error:", error);
  }
}

// päivitetään sijainti gaming consoleen
async function locationToGamingConsole(icao) {
  try {
    const response = await fetch(baseUrl + "/location", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(icao),
    });
    const data = await response.json();
    document.getElementById("location").innerText = data;
  } catch (error) {
    console.error("Error:", error);
  }
}

// Päivittää html:ään statustiedot
function updateStatusBox(game_dict) {
  document.querySelector("#screen-name").textContent = game_dict["screen_name"];
  document.querySelector("#difficulty").textContent =
    game_dict["game_difficulty"];
  document.querySelector("#category").textContent = game_dict["quiz_category"];
  document.querySelector("#money").textContent = game_dict["game_money"];
  document.querySelector("#CO2-player").textContent = game_dict["CO2_player"];
  document.querySelector("#airports-hacked").textContent =
    game_dict["airports_hacked"];
  document.querySelector("#CO2-criminal").textContent =
    game_dict["CO2_criminal"];
}

// Funktio säätietojen hakemiseen
async function weather(coordinates) {
  try {
    const response = await fetch("http://127.0.0.1:5000/weather", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(coordinates),
    });
    const data = await response.json();

    let div = document.getElementById("weather");

    let temp = document.createElement("p");

    let desc = document.createElement("p");
    let name = document.createElement("p");

    desc.innerText = data["desc"];
    temp.innerText = data["temp"] + " °C";
    name.innerText = data["name"];
    let icon = document.createElement("img");
    icon.src = `https://openweathermap.org/img/wn/${data["icon"]}@2x.png`;
    icon.alt = "weather_icon";

    div.append(temp);
    div.append(icon);
    div.append(desc);
  } catch (error) {
    console.log("ERROR:", error.message);
  }
}

// Funktio co2 sekä kokonaismatkan laskemiseen
async function co2(routes, index) {
  const payload = {
    routes: routes,
    index: index,
  };
  try {
    const response = await fetch("http://127.0.0.1:5000/co2distance", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { co2: data.co2, distanceKM: data.distanceKM };
  } catch (error) {
    console.log("ERROR:", error.message);
  }
}

// Asynkroninen funktio koordinaattien hakemiseen
async function fetchCoordinates(game_dict) {
  try {
    // Haetaan koordinaatit backendistä
    const response = await fetch("http://127.0.0.1:5000/flyto", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(game_dict),
    });

    if (!response.ok) {
      throw new Error("HTTP-virhe: " + response.status);
    }

    // Muunnetaan vastaus JSON-muotoon
    const jsonData = await response.json();

    // const points = [
    //   [60.1756, 24.9342],
    //   [52.3667, 4.8833],
    // ];

    // Päivitetään pisteiden käsittely vastaamaan uutta JSON-rakennetta
    const points = [
      [parseFloat(jsonData.from.latitude), parseFloat(jsonData.from.longitude)], // Lähtöpiste
      [parseFloat(jsonData.to.latitude), parseFloat(jsonData.to.longitude)], // Määränpää
    ];
    try {
      game_dict.data["coordinates"] = points;
    } catch (error) {
      game_dict["coordinates"] = points;
    }
    return game_dict;
  } catch (error) {
    console.log("Virhe haettaessa tietoa:", error.message);
  }
}

async function drawLine(game_dict, map) {
  //Piirrä reitti annetuilla koordinaateilla
  const polyline = L.polyline(game_dict["coordinates"], {
    color: "blue",
  }).addTo(map);
  //Asetata näkymä reitin ympärille
  const bounds = polyline.getBounds();
  map.fitBounds(bounds, {
    padding: [100, 100],
    maxZoom: 10,
  });

  //Lentokoneikoni
  const airplaneIcon = L.icon({
    iconUrl: "../images/plane.png",
    iconSize: [32, 32],
    iconAnchor: [16, 16],
  });

  // Lentokone aloituspisteeseen
  const start = game_dict["coordinates"][0];
  const end = game_dict["coordinates"][1];
  const airplaneMarker = L.marker(start, { icon: airplaneIcon }).addTo(map);

  // Animaation asetukset
  let progress = 0;
  const steps = 150;
  const interval = 20;

  //Animaatiofunktio
  async function animate() {
    const sleep = (delay) =>
      new Promise((resolve) => setTimeout(resolve, delay));

    if (progress >= 1) {
      map.removeLayer(polyline);
      await map.flyTo(end, 8, { duration: 3 });
      routes.push(game_dict["coordinates"]);
      map.removeLayer(airplaneMarker);

      await sleep(3000);

      const marker = L.circleMarker(
        [game_dict["coordinates"][1][0], game_dict["coordinates"][1][1]],
        {
          color: "white", // Alkuperäinen väri
          fillColor: "blue",
          fillOpacity: 1,
          radius: 10,
        }
      ).addTo(map);

      if (!game_dict["correct_location"]) {
        marker.setStyle({ color: "red", fillColor: "red" });
        marker.bindPopup("<b>Criminal hasn't been here!</b>").openPopup();
        await sleep(2000);
        marker.closePopup();
      } else {
        marker.setStyle({ color: "green", fillColor: "green" });
        marker.bindPopup("<b>Criminal was here!</b>").openPopup();
        await sleep(2000);
        marker.closePopup();
      }
    } else {
      progress += 1 / steps;
      const lat = start[0] + (end[0] - start[0]) * progress;
      const lng = start[1] + (end[1] - start[1]) * progress;
      airplaneMarker.setLatLng([lat, lng]);
      setTimeout(animate, interval);
    }
  }

  animate();
}

// tarkistaa palvelimelta täyttyykö edellytykset pelin päättämiselle
async function stopGame(game_dict) {
  try {
    const response = await fetch(baseUrl + "/stopGame", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(game_dict),
    });
    const data = await response.json();
    return data.data;
  } catch (error) {
    console.error("Error:", error);
  }
}

// Update game input -buttons in airportOptions()
function updateGameInput(newButtons) {
  const gameInput = document.querySelector("#game-input");
  gameInput.innerHTML = "<h3>Game input</h3>";
  for (const newButton of newButtons) {
    if (typeof newButton !== "string") {
      if (newButton["value"] != "randomAction") {
        const button = document.createElement("button");
        button.value = newButton["value"];
        button.textContent = newButton["text"];
        gameInput.appendChild(button);
      } else {
        const button = document.createElement("button");
        button.value = newButton["value"];
        button.textContent = newButton["text"][0];
        gameInput.appendChild(button);
      }
    }
  }
}

// Get correct input options from backend
async function airportOptions(game_dict) {
  try {
    const response = await fetch(baseUrl + "/airportOptions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(game_dict),
    });
    const data = await response.json();

    const options = data["data"]["airport_options"];
    updateGameInput(options);
    return data.data;
  } catch (error) {
    console.error("Error:", error);
  }
}

// Airport actions
async function airportActions(game_dict) {
  const gameInput = document.querySelector("#game-input");

  return new Promise((resolve) => {
    const handleClick = async (event) => {
      const buttonValue = event.target.value;

      // TALK TO SECURITY
      if (buttonValue === "talkToSecurity") {
        try {
          const response = await fetch(baseUrl + "/talkToSecurity", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(game_dict),
          });
          const data = await response.json();
          resolve(data); // Resolve with the updated game_dict
        } catch (error) {
          console.error("Error:", error);
          resolve(game_dict); // Resolve with the original game_dict in case of error
        }

        // SOLVE A CLUE
      } else if (buttonValue === "solveClue") {
        try {
          const response = await fetch(baseUrl + "/solveClue", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(game_dict),
          });
          const data = await response.json();

          // Question modal
          game_dict = await questionModal(data);
          resolve(game_dict);
        } catch (error) {
          console.error("Error:", error);
          resolve(game_dict);
        }

        // SOLVE PREVIOUS CLUE
      } else if (buttonValue === "solvePreviousClue") {
        try {
          const response = await fetch(baseUrl + "/solvePreviousClue", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(game_dict),
          });
          const data = await response.json();
          resolve(data);
        } catch (error) {
          console.error("Error:", error);
          resolve(game_dict);
        }

        // RANDOM ACTION
      } else if (buttonValue === "randomAction") {
        try {
          const response = await fetch(baseUrl + "/randomLuck", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(game_dict),
          });
          const data = await response.json();
          resolve(data);
        } catch (error) {
          console.error("Error:", error);
          resolve(game_dict);
        }
      }

      // Remove the event listener after handling the click
      gameInput.removeEventListener("click", handleClick);
    };

    // Add the event listener
    gameInput.addEventListener("click", handleClick);
  });
}

// Question modal
async function questionModal(game_dict) {
  const question = game_dict["clue"][0]; // Question text
  const answers = game_dict["clue"][1]; // List of answers
  const correctAnswer = game_dict["clue"][2]; // Correct answer
  const modal = document.getElementById("questionModal");
  const questionText = document.getElementById("questionText");
  const answersContainer = document.getElementById("answersContainer");

  questionText.textContent = question;
  answersContainer.innerHTML = "";

  return new Promise((resolve) => {
    answers.forEach((answer) => {
      const button = document.createElement("button");
      button.textContent = answer;
      button.value = answer;
      button.classList.add("answer-button");

      button.addEventListener("click", () => {
        if (answer === correctAnswer) {
          console.log("Correct answer");
          game_dict["previous_quiz_answer"] = true;
        } else {
          console.log("Wrong answer");
          game_dict["previous_quiz_answer"] = false;
          if (game_dict.clue[1].length > 2) {
            // Poistetaan vastattu vastaus listasta kun vastasimme väärin
            game_dict["clue"][1] = game_dict["clue"][1].filter(
              (item) => item !== answer
            );
          }
        }
        game_dict = nextLocation(game_dict);
        modal.close();
        resolve(game_dict);
      });
      answersContainer.appendChild(button);
    });
    modal.showModal();
  });
}

async function nextLocation(game_dict) {
  try {
    const response = await fetch(baseUrl + "/nextLocation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(game_dict),
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
  }
}

async function updateToVisited(location) {
  try {
    const response = await fetch(baseUrl + "/updateToVisited", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(location),
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
  }
}

function gameOutput(game_dict) {
  const gameOutput = document.getElementById("game-output");
  gameOutput.innerHTML = "<h3>Game output</h3>";
  for (let result of game_dict["game_output"]) {
    gameOutput.innerHTML += `<p>${result}</p>`;
  }
}

// Fly to the next airport
async function flyToNextAirport(game_dict, routes, map) {
  // Update coordinates
  game_dict = await fetchCoordinates(game_dict);

  // animateAirplane()
  drawLine(game_dict, map);

  // calculate emissions
  const data = await co2(routes, 0);
  game_dict["KM_player"] += data.distanceKM;
  game_dict["CO2_player"] += data.co2;

  // Reduce money
  game_dict["game_money"] -= game_dict["flight_price"];

  // Update player's location
  game_dict["player_location"] = game_dict["next_location"];

  // Update location in criminal table to visited
  await updateToVisited(game_dict["player_location"]);

  // Update html
  updateStatusBox(game_dict);
  locationToGamingConsole(game_dict["player_location"]);

  return { game_dict: game_dict, routes: routes };
}

let routes = [
  // RANDOM LOCATIONS (temporary)
  [
    [50.1109, 8.6821],
    [48.8566, 2.3522],
  ], // Frankfurt, Germany to Paris, France
  [
    [51.5074, -0.1278],
    [52.52, 13.405],
  ], // London, UK to Berlin, Germany
  [
    [41.9028, 12.4964],
    [40.4168, -3.7038],
  ], // Rome, Italy to Madrid, Spain
  [
    [59.3293, 18.0686],
    [60.1695, 24.9354],
  ], // Stockholm, Sweden to Helsinki, Finland
  [
    [53.3498, -6.2603],
    [55.7558, 37.6173],
  ], // Dublin, Ireland to Moscow, Russia
  [
    [47.4979, 19.0402],
    [48.2082, 16.3738],
  ], // Budapest, Hungary to Vienna, Austria
  [
    [37.9838, 23.7275],
    [45.815, 15.9819],
  ], // Athens, Greece to Zagreb, Croatia
  [
    [50.0755, 14.4378],
    [52.2297, 21.0122],
  ], // Prague, Czech Republic to Warsaw, Poland
  [
    [55.6761, 12.5683],
    [59.9139, 10.7522],
  ], // Copenhagen, Denmark to Oslo, Norway
  [
    [43.7102, 7.262],
    [45.4642, 9.19],
  ], // Nice, France to Milan, Italy
];

// PELI KASATAAN TÄMÄN FUNKTION SISÄLLE
async function main() {
  // PELIN ALUSTUS #####################################################

  let game_dict = await gameSetup(); // Pelin parametrien luonti palvelimella, palauttaa pythonista tutun game_dict -sanakirjan
  startTimer(game_dict.data["game_time"]);
  await updateToVisited(game_dict.data["player_location"]);

  // try {stopCriminalTimer()} catch (error) {console.log(error)}
  startCriminalTimer(game_dict.data.criminal_time);

  // Mitä tapahtuu kun aika loppuu
  document.addEventListener("timerEnd", () => {
    game_dict["time_left_bool"] = false;
  });
  updateStatusBox(game_dict.data); // Päivittää html:ään statustiedot
  game_dict = await fetchCoordinates(game_dict); // Haetaan rikollisen ja pelaajan koordinaatit
  // Alustetaan kartta

  const map = L.map("map").setView(
    [game_dict.data["coordinates"][0][0], game_dict.data["coordinates"][0][1]],
    10
  );

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  const marker = L.marker([
    game_dict.data["coordinates"][0][0],
    game_dict.data["coordinates"][0][1],
  ]).addTo(map);
  marker.bindPopup("<b>Starting point</b>").openPopup();

  weather(game_dict.data.coordinates[0]);

  let endGame = false;
  try {
    game_dict = game_dict.data;
  } catch (error) {
    console.log(error);
  }
  locationToGamingConsole(game_dict["player_location"]);

  // PELIN LOOPPI ALKAA TÄSTÄ ##################################################

  while (!endGame) {
    console.log(
      "GAME LOOP'S FIRST ROW",
      ` Current: ${game_dict.player_location}, Next: ${game_dict.next_location}`
    );
    // reset airport_menu-helper parameters to default value before entering airport-menu at the new airport
    game_dict["talk_to_chief"] = false;
    game_dict["tried_luck"] = false;
    game_dict["first_iteration"] = true;
    game_dict["next_location_bool"] = false;
    game_dict["clue_solved"] = false;
    game_dict["criminal_was_here"] = false;

    game_dict["random_luck_bool"] = Math.random() <= game_dict["random_luck"];

    // AIRPORT-MENU
    while (!game_dict["next_location_bool"]) {
      console.log(
        "AIRPORT LOOP'S FIRST ROW",
        ` Current: ${game_dict.player_location}, Next: ${game_dict.next_location}`
      );
      game_dict = await airportOptions(game_dict); // haetaan vaihtoehdot mitä voidaan tehdä lentoasemalla ja viedään gaming consoleen napeiksi
      game_dict = await airportActions(game_dict); // event listener napeille -> tehdään napin mukainen toiminto
      gameOutput(game_dict);
      // game_dict["next_location_bool"] = true
    }

    // Lennetään kentältä toiselle - funktio sisältää kaikki tarvittavat toiminnot
    console.log(
      "FLY TO NEXT AIRPORT",
      ` Current: ${game_dict.player_location}, Next: ${game_dict.next_location}`
    );
    const data = await flyToNextAirport(game_dict, routes, map);
    game_dict = data.game_dict;
    routes = data.routes;

    if (game_dict["first_airport"]) {
      game_dict["first_airport"] = false;
    }

    endGame = await stopGame(game_dict); // tarkistaa palvelimelta täyttyykö edellytykset pelin päättämiselle
  }
  stopCriminalTimer();
}

main();
