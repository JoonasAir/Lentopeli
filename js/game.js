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
}

main()