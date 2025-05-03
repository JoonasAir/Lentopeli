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
    fetchCoordinates(game_dict);
    // Alustetaan kartta
    const routes = [];
    const map = L.map("map").setView([game_dict["coordinates"][0][0], game_dict["coordinates"][0][1]], 10);
    
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);
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

//     // Piirretään viiva kartalle
//     const polyline = L.polyline(points, { color: "blue" }).addTo(map);

//     // Keskitetään kartta reitin ympärille
//     const bounds = polyline.getBounds();
//     map.fitBounds(bounds, {
//       padding: [100, 100],
//       maxZoom: 10,
//     });

//     // Lentokoneikoni
//     const airplaneIcon = L.icon({
//       iconUrl: "../images/plane.png",
//       iconSize: [32, 32],
//       iconAnchor: [16, 16],
//     });

//     // Lentokone aloituspisteeseen
//     const airplaneMarker = L.marker(points[0], { icon: airplaneIcon }).addTo(
//       map
//     );

//     // Animaation asetukset
//     let progress = 0; // Animaation etenemisen tila (0 = alku, 1 = loppu)
//     let steps = 150; // Kuinka monessa vaiheessa animaatio etenee
//     let interval = 20; // Viive jokaisen animaatioaskeleen välillä (ms)
//     let start = points[0]; // Lentoreitin aloituspiste
//     let end = points[1]; // Lentoreitin päätepiste

//     function animateAirplane() {
//       if (progress >= 1) {
//         // Kun animaatio on valmis:
//         map.removeLayer(polyline); // Poista polku kartalta
//         map.flyTo(end, 8, { duration: 3 }); // Siirrä kartta lopulliseen sijaintiin (zoom 8)
//         routes.push(points); // Lisää reitti tallennettuihin reitteihin
//       } else {
//         progress += 1 / steps; // Kasvata animaation etenemistä
//         const lat = start[0] + (end[0] - start[0]) * progress; // Lasketaan uusi väliarvo latitude
//         const lng = start[1] + (end[1] - start[1]) * progress; // Lasketaan uusi väliarvo longitude

//         airplaneMarker.setLatLng([lat, lng]); // Päivitä lentokoneen sijainti kartalla
//         setTimeout(animateAirplane, interval); // Suorita seuraava animaatioaskel viiveen jälkeen
//       }
//     }

//     animateAirplane();
//   } catch (error) {
//     console.log("Virhe haettaessa tietoa:", error.message);
//   }
// }




main()