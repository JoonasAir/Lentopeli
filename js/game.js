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

    div.append(name);
    div.append(temp);
    div.append(icon);
    div.append(desc);
  } catch (error) {
    console.log("ERROR:", error.message);
  }
}

// Funktio co2 sekä kokonaismatkan laskemiseen
async function co2(coordinates) {
  try {
    const response = await fetch("http://127.0.0.1:5000/co2distance", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(coordinates),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("CO2-vastaus:", data);
  } catch (error) {}
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

    game_dict.data["coordinates"] = points;
    return game_dict

  } catch (error) {
    console.log("Virhe haettaessa tietoa:", error.message);
  }
}

// // Piirretään viiva kartalle
// const polyline = L.polyline(game_dict["coordinates"], { color: "blue" }).addTo(map);

// // Keskitetään kartta reitin ympärille
// const bounds = polyline.getBounds();
// map.fitBounds(bounds, {
//     padding: [100, 100],
//     maxZoom: 10,
// });

// // Lentokoneikoni
// const airplaneIcon = L.icon({
//     iconUrl: "../images/plane.png",
//     iconSize: [32, 32],
//     iconAnchor: [16, 16],
// });

// // Lentokone aloituspisteeseen
// const airplaneMarker = L.marker(game_dict["coordinates"][0], { icon: airplaneIcon }).addTo(
//     map
// );

// // Animaation asetukset
// let progress = 0; // Animaation etenemisen tila (0 = alku, 1 = loppu)
// let steps = 150; // Kuinka monessa vaiheessa animaatio etenee
// let interval = 20; // Viive jokaisen animaatioaskeleen välillä (ms)
// let start = game_dict["coordinates"][0]; // Lentoreitin aloituspiste
// let end = game_dict["coordinates"][1]; // Lentoreitin päätepiste

// function animateAirplane(game_dict) {
//   if (progress >= 1) {
//     // Kun animaatio on valmis:
//     map.removeLayer(polyline); // Poista polku kartalta
//     map.flyTo(end, 8, { duration: 3 }); // Siirrä kartta lopulliseen sijaintiin (zoom 8)
//     routes.push(game_dict["coordinates"]); // Lisää reitti tallennettuihin reitteihin
//   } else {
//     progress += 1 / steps; // Kasvata animaation etenemistä
//     const lat = start[0] + (end[0] - start[0]) * progress; // Lasketaan uusi väliarvo latitude
//     const lng = start[1] + (end[1] - start[1]) * progress; // Lasketaan uusi väliarvo longitude
//     airplaneMarker.setLatLng([lat, lng]); // Päivitä lentokoneen sijainti kartalla
//     setTimeout(animateAirplane, interval); // Suorita seuraava animaatioaskel viiveen jälkeen
//   }
// }

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

  gameInput.addEventListener("click", (event) => {
    const buttonValue = event.target.value;

    if (buttonValue === "talkToSecurity") {
      console.log("Talking to the airport's security chief...");
    } else if (buttonValue === "solveClue") {
      
      console.log("Solving the clue...");
    } else if (buttonValue === "solvePreviousClue") {
      //
      console.log("Trying to solve the previous clue again...");
    } else if (buttonValue === "randomAction") {
      //
      console.log("Doing the random action...");
    }
  });
  return game_dict;
}

// Fly to the next airport
async function flyToNextAirport(game_dict) {
  // Update player's location

  // Update coordinates

  // Update emissions

  // animateAirplane()

}

// PELI KASATAAN TÄMÄN FUNKTION SISÄLLE
async function main() {
  // PELIN JA HTML:N ALUSTUS #####################################################
  let game_dict = await gameSetup(); // Pelin parametrien luonti palvelimella, palauttaa pythonista tutun game_dict -sanakirjan
  startTimer(game_dict.data["game_time"]);
  // Mitä tapahtuu kun aika loppuu
  document.addEventListener("timerEnd", () => {
    game_dict["time_left_bool"] = false;
  });
  updateStatusBox(game_dict.data); // Päivittää html:ään statustiedot
  game_dict = await fetchCoordinates(game_dict); // Haetaan rikollisen ja pelaajan koordinaatit
  // Alustetaan kartta
  const routes = [];
  const map = L.map("map").setView(
    [game_dict.data["coordinates"][0][0], game_dict.data["coordinates"][0][1]],
    10
  );
  const marker = L.marker([
    game_dict.data["coordinates"][0][0],
    game_dict.data["coordinates"][0][1],
  ]).addTo(map);
  marker.bindPopup("<b>Olet tässä</b>").openPopup();
  
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);
  weather(game_dict.data.coordinates[0])

  // sleep-funktion teko
  const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay));

  // PELIN LOOPPI ALKAA TÄSTÄ ##################################################
  let endGame = false;
  while (!endGame) {
    // reset airport_menu-helper parameters to default value before entering airport-menu at the new airport
    game_dict["talk_to_chief"] = false;
    game_dict["tried_luck"] = false;
    game_dict["first_iteration"] = true;
    game_dict["next_location_bool"] = false;
    game_dict["clue_solved"] = false;
    game_dict["criminal_was_here"] = false;

    // AIRPORT-MENU
    while (!game_dict["next_location_bool"]) {
      game_dict = await airportOptions(game_dict); // haetaan vaihtoehdot mitä voidaan tehdä lentoasemalla ja viedään gaming consoleen napeiksi
      game_dict = await airportActions(game_dict); // event listener napeille -> tehdään napin mukainen toiminto

      // flyToNextAirport(game_dict) // EI ALOITETTU VIELÄ
      await sleep(5000); // sleep-funktion käyttö, jotta kone ei mene jumiin, poistetaan myöhemmin
    }

    if (game_dict.data["first_airport"]) {
      game_dict.data["first_airport"] = false;
    }

    await sleep(5000); // sleep-funktion käyttö, jotta kone ei mene jumiin, poistetaan myöhemmin
    endGame = await stopGame(game_dict); // tarkistaa palvelimelta täyttyykö edellytykset pelin päättämiselle
    console.log("Game ends:", endGame);
  }
}

main();
