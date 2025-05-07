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



// Käyttäjän syöttämien aloitustietojen haku
// ja pelin parametrien luonti palvelimella
async function gameSetup() {
  try {
    const response = await fetch(baseUrl + "/gameSetup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dataToFlask),
    });
    let data = await response.json();
    data = data.data
    return data;
  } catch (error) {
    console.error("Error:", error);
  }
}


// Game timer
const timerElement = document.getElementById("timer");
const timerEndEvent = new Event("timerEnd");
let timerInterval;

// Käynnistää ajastimen (vain kun peli alkaa tai nollataan)
function startGameTimer(countdownTime) {
  clearInterval(timerInterval); // Estetään päällekkäiset ajastimet
  timerInterval = setInterval(() => {
    countdownTime = updateGameTimer(countdownTime); // Päivitetään countdownTime sekuntin välein
  }, 1000);  
  updateGameTimer(countdownTime); // Päivitetään heti, jotta käyttäjä näkee ajan muutoksen
}  

function updateGameTimer(countdownTime) {
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



// Käynnistää palvelimella taustaprosessin, joka lisää X ajan välein tietokantaan rikolliselle uuden sijainnin
async function startCriminalTimer(time) {
  try {
    const response = await fetch(baseUrl + "/startCriminalTimer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(time),
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
  }
}

// Pysäyttää palvelimen taustaprosessin
async function stopCriminalTimer() {
  try {
    await fetch(baseUrl + "/stopCriminalTimer");
  } catch (error) {
    console.error("Error:", error);
  }
}


// Päivittää rikollisen tauluun sijainnin, johon saavuimme, Visited -sarakkeen 0 -> 1
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



// Tarkistetaan ollaanko samalla lentokentällä rikollisen kanssa (yksi pelin päättämisen ehdoista)
async function criminalCaught() {
  try {
    const response = await fetch(baseUrl + "/criminalCaught");
    const criminal_caught_bool = await response.json()
    return criminal_caught_bool
  } catch (error) {
    console.error("Error:", error);
  }

}



// Päivitetään sijaintimme html:ään
async function locationToGamingConsole() {
  try {
    const response = await fetch(baseUrl + "/location");
    const data = await response.json();
    document.getElementById("location").innerText = data;
  } catch (error) {
    console.error("Error:", error);
  }
}



// Päivittää html:ään statustiedot
async function updateStatusBox(game_dict) {
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



// Funktio säätietojen hakemiseen ja html:ään lisäämiseen
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



// Funktio lentomatkan kilometrejen ja co2-päästöjen laskemiseen
async function co2(routes) {
  const payload = {
    routes: routes,
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



// Funktio lentomatkan alku- ja loppupisteen koordinaattien hakemiseen
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


// Piirretään kartalle lentoreitti ja näytetään lennon animaatio, 
// sekä lisätään punaiset/vihreät merkit sen mukaan ollaanko oikeassa vai väärässä paikassa
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
  const steps = 100;
  const interval = 20;

  //Animaatiofunktio
  async function animate() {
    const sleep = (delay) =>
      new Promise((resolve) => setTimeout(resolve, delay));

    if (progress >= 1) {
      map.removeLayer(polyline);
      await map.flyTo(end, 5, { duration: 1.5 });
      map.removeLayer(airplaneMarker);

      await sleep(1500);

      const marker = L.circleMarker(
        [game_dict["coordinates"][1][0], game_dict["coordinates"][1][1]],
        {
          color: "white",
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
  animate()
}



// Tarkistaa palvelimelta täyttyykö edellytykset pelin päättämiselle
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



// Haetaan palvelimelta oikeat toiminnot ja tehdään näistä napit html:ään 
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

// Päivitetään html:ään pelin toiminto-napit airportOptions funktiossa
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

// Tehdään jatkotoimenpiteet sen mukaan mitä toiminto-nappia pelaaja painaa
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
          resolve(data);
        } catch (error) {
          console.error("Error:", error);
          resolve(game_dict);
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
          game_dict = await questionModal(game_dict);
          resolve(game_dict);

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

      gameInput.removeEventListener("click", handleClick);
    };

    gameInput.addEventListener("click", handleClick);
  });
}

// Luodaan ja avataan modaali, jossa on tietovisa-kysymys ja vastausnapit
async function questionModal(game_dict) {
  const question = game_dict["clue"][0];
  const answers = game_dict["clue"][1];
  const correctAnswer = game_dict["clue"][2];
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
        if (answer === correctAnswer) { // Oikea vastaus
          console.log("Correct answer");
          game_dict["previous_quiz_answer"] = true;

        } else { // Väärä vastaus
          console.log("Wrong answer");
          game_dict["previous_quiz_answer"] = false;
          
          // Jos vastausvaihtoehtoja on enemmän kuin 2, 
          // poistetaan vastattu väärä vastaus seuraavaa kierrosta varten
          if (game_dict.clue[1].length > 2) { 
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


// Haetaan pelaajan seuraava sijainti sen mukaan, vastasiko kysymykseen oikein
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


// Lisätään html:ään output teksti sen mukaan mikä toiminto tehtiin
function gameOutput(game_dict) {
  const gameOutput = document.getElementById("game-output");
  gameOutput.innerHTML = "<h3>Game output</h3>";
  for (let result of game_dict["game_output"]) {
    gameOutput.innerHTML += `<p>${result}</p>`;
  }
}


// Lennetään seuraavalle lentokentälle, tässä funktiossa
// tarvittavat toimenpiteet lentokentältä toiselle siirtymisen välissä
async function flyToNextAirport(game_dict, routes, map) {
  // Haetaan koordinaatit lennon alku- ja loppupisteille
  game_dict = await fetchCoordinates(game_dict);

  // Lisätään koordinaatit listaan talteen
  routes.push(game_dict.coordinates)

  // Kartan animaatio
  await drawLine(game_dict, map);

  // Lasketaan lentomatka ja päästöt, sekä lisätään nämä kokonaiskilometreihin ja päästöihin
  const data = await co2(routes);
  game_dict["KM_player"] += data.distanceKM;
  game_dict["CO2_player"] += data.co2;

  // Vähennetään lentolipun verran rahaa
  game_dict["game_money"] -= game_dict["flight_price"];

  // Päivitetään pelaajan sijainti
  game_dict["player_location"] = game_dict["next_location"];

  // Päivitetään tietokantaan rikollisen tauluun uuden sijaintimme rivin Visited-sarake 0 -> 1
  await updateToVisited(game_dict["player_location"]);

  // Päivitetään html:ään pelin statustiedot
  await updateStatusBox(game_dict);
  await locationToGamingConsole();

  return { game_dict: game_dict, routes: routes };
}




// PELI KASATAAN TÄMÄN FUNKTION SISÄLLE
async function main() {

  // PELIN ALUSTUS #####################################################
  let routes = [];
  let routes_criminal = [];

  // Pelin parametrien luonti palvelimella.
  // Palauttaa sanakirjan, jossa säilömme pelin keskeiset parametrit.
  let game_dict = await gameSetup();

  // Käynnistetään pelin ajastin ja lisätään html:ään
  startGameTimer(game_dict["game_time"]);
  
  // Luodaan event listener ajan päättymiselle. 
  document.addEventListener("timerEnd", () => {
    game_dict["time_left_bool"] = false; // Yksi pelin päättämisen ehdoista
  });

  // Käynnistetään palvelimella taustaprosessina juokseva ajastin, 
  // joka lisää rikolliselle X ajan välein tietokantaan uuden sijainnin (X määräytyy vaikeustason mukaan)
  await startCriminalTimer(game_dict.criminal_time)

  // Päivitetään tietokantaan rikollisen tauluun sijaintimme riville visited -sarake 0 -> 1 
  await updateToVisited(game_dict["player_location"]);

  // Päivittää html:ään statustiedot
  await updateStatusBox(game_dict); 

  // Haetaan koordinaatit karttaa varten
  game_dict = await fetchCoordinates(game_dict); 

  // Alustetaan kartta
  const map = L.map("map").setView(
    [game_dict["coordinates"][0][0], game_dict["coordinates"][0][1]],
    10
  );

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  const marker = L.marker([
    game_dict["coordinates"][0][0],
    game_dict["coordinates"][0][1],
  ]).addTo(map);
  marker.bindPopup("<b>Starting point</b>").openPopup();

  // Haetaan sijaintimme säätiedot API:lla ja lisätään html:ään 
  weather(game_dict.coordinates[0]);

  // lisätään sijaintimme html:ään
  locationToGamingConsole(game_dict["player_location"]);
  
  
  // PELIN LOOPPI ALKAA TÄSTÄ ########################################################################
  let endGame = false;
  while (!endGame) {
    // nollataan lentokenttä-loopin helper-muuttujat vakioarvoihin ennen kun mennään uudelle lentokentälle
    game_dict["talk_to_chief"] = false;
    game_dict["tried_luck"] = false;
    game_dict["first_iteration"] = true;
    game_dict["next_location_bool"] = false;
    game_dict["clue_solved"] = false;
    game_dict["criminal_was_here"] = false;

    // Muuttuja, joka määrittää onko pelaajalla mahdollista saada tuuri-apua pelin etenemiseen
    game_dict["random_luck_bool"] = Math.random() <= game_dict["random_luck"];

    // LENTOKENTTÄ -LOOPPI ALKAA TÄSTÄ ###############################################################
    while (!game_dict["next_location_bool"]) {

      // Haetaan palvelimelta toiminto-vaihtoehdot ja lisätään html:ään napeiksi
      game_dict = await airportOptions(game_dict); 
      
      // Tehdään painetun napin mukainen toiminto
      game_dict = await airportActions(game_dict); 
      
      // Päivitetään html:ään painetun napin tuottama output
      gameOutput(game_dict);
    }

    // Lennetään kentältä toiselle. Funktio sisältää kaikki tarvittavat toiminnot
    const data = await flyToNextAirport(game_dict, routes, map);
    game_dict = data.game_dict;
    routes = data.routes;


    // if (game_dict["first_airport"]) {
    //   game_dict["first_airport"] = false;
    // }

    // Tarkistetaan palvelimelta, olemmeko saaneet rikollisen kiinni
    game_dict["criminal_caught"] = await criminalCaught()

    // tarkistaa palvelimelta täyttyykö edellytykset pelin päättämiselle
    endGame = await stopGame(game_dict); 
  }

  // PELIN LOOPPI PÄÄTTYI ##################################################################
  console.log("EXIT FROM GAME LOOP")

  // Pysäytetään palvelimella taustaprosessina pyörivä ajastin
  await stopCriminalTimer();

  // Pelin jälkeinen html 
  const boxes = document.querySelector(".boxes")

  if (game_dict.criminal_caught) { // Saimme rikollisen kiinni
    boxes.innerHTML = "Sait rikollisen kiinni, voitit pelin!"

  } else if (!game_dict.game_money >= game_dict.flight_price) { // Rahat loppuivat
    boxes.innerHTML = "Rahasi loppui, hävisit pelin!"

  } else if (!game_dict.time_left_bool) { // Aika loppui
    boxes.innerHTML = "Aika loppui, hävisit pelin!"
  }
}

main();
