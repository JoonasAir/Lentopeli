'use strict';

const baseUrl = 'http://127.0.0.1:5000';

const queryString = window.location.search;

const urlParams = new URLSearchParams(queryString);

const name_input = urlParams.get("username");
const difficulty_input = urlParams.get("difficulty");
const category_input = urlParams.get("category");

const dataToFlask = {
    name_input: name_input,
    difficulty_input: difficulty_input,
    category_input: category_input
}

// Käyttäjän syöttämien aloitustietojen haku 
// ja pelin parametrien luonti palvelimella
async function gameSetup() {
    try {
        const response = await fetch(baseUrl + '/gameSetup', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dataToFlask)
        });
        const data = await response.json();

        return data
    } catch (error) {
        console.error("Error:", error)
    }
}

// Päivittää html:ään statustiedot
function updateStatusBox(game_dict) {
    document.querySelector("#screen-name").textContent = game_dict["screen_name"];
    document.querySelector("#difficulty").textContent = game_dict["game_difficulty"];
    document.querySelector("#category").textContent = game_dict["quiz_category"];
    document.querySelector("#money").textContent = game_dict["game_money"];
    document.querySelector("#CO2-player").textContent = game_dict["CO2_player"];
    document.querySelector("#airports-hacked").textContent = game_dict["airports_hacked"];
    document.querySelector("#CO2-criminal").textContent = game_dict["CO2_criminal"];

}

// Peli kasataan tämän funktion sisään
async function main() {
    const game_dict = await gameSetup() // Pelin parametrien luonti palvelimella, palauttaa pythonista tutun game_dict -sanakirjan 
    updateStatusBox(game_dict.data) // Päivittää html:ään statustiedot

    await fetchCoordinates(game_dict);

    // Alustetaan kartta
    const routes = [];
    const map = L.map("map").setView([game_dict["coordinates"][0][0], game_dict["coordinates"][0][1]], 10);
    const marker = L.marker([game_dict["coordinates"][0][0], game_dict["coordinates"][0][1]]).addTo(map);
    marker.bindPopup("<b>Olet tässä</b>").openPopup();

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    // animateAirplane(game_dict)
}




// Asynkroninen funktio koordinaattien hakemiseen
async function fetchCoordinates(game_dict) {
  try {
    // Haetaan koordinaatit backendistä
    const response = await fetch("http://127.0.0.1:5000/flyto", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(game_dict)
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

    game_dict["coordinates"] = points

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

  // Animaation asetukset
  let progress = 0;
  const steps = 150;
  const interval = 20;

  //Animaatiofunktio
  async function animate() {
    const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay));
    const marker = L.marker([
      game_dict["coordinates"][1][0],
      game_dict["coordinates"][1][1],
      ]).addTo(map);
    
    if (progress >= 1) {
      map.removeLayer(polyline);
      marker.bindPopup("<b>Olet tässä</b>").openPopup();
      await map.flyTo(end, 8, { duration: 3 });
      routes.push(game_dict["coordinates"]);
      map.removeLayer(airplaneMarker);
      await sleep(3000);
      marker.closePopup();
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
async function flyToNextAirport(game_dict, routes, map) {
  // Update player's location

  // Update coordinates
  // game_dict = fetchCoordinates(game_dict)

  // calculate emissions
  const data = await co2(routes, 0)
  game_dict["KM_player"] += data.distanceKM
  game_dict["CO2_player"] += data.co2

  // animateAirplane()
  drawLine(game_dict, map)
  // Reduce money
  game_dict["game_money"] -= game_dict["flight_price"]

  // Update html
  updateStatusBox(game_dict);



main()