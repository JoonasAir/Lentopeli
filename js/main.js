"use strict";

async function leaderboard() {
  try {
    // Fetching data from server
    const response = await fetch("http://127.0.0.1:5000/leaderboard");
    const jsonData = await response.json();

    const button = document.querySelector("#leaderboard");
    const dialog = document.querySelector("#leaderboardModal");
    const closeButton = dialog.querySelector("#closeLeaderboard"); // Sulkemismerkki

    button.addEventListener("click", function () {
      dialog.innerHTML = ""; // Tyhjennetään dialogi

      dialog.appendChild(closeButton);

      // **Lisätään otsikko**
      const title = document.createElement("h2");
      title.textContent = "Leaderboard";
      title.style.textAlign = "center";
      dialog.appendChild(title);

      // Luodaan taulukko
      const table = document.createElement("table");
      table.style.width = "100%";
      table.style.borderCollapse = "collapse";

      // Luodaan taulukon otsikkorivi
      const headerRow = document.createElement("tr");
      headerRow.innerHTML = `
        <th style="border: 1px solid black; padding: 8px;">Sijoitus</th>
        <th style="border: 1px solid black; padding: 8px;">Nimi</th>
        <th style="border: 1px solid black; padding: 8px;">Pisteet</th>
      `;
      table.appendChild(headerRow);

      // Lisätään leaderboard-data taulukkoon
      for (let i = 0; i < jsonData.length && i < 10; i++) {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td style="border: 1px solid black; padding: 8px;">${i + 1}</td>
          <td style="border: 1px solid black; padding: 8px;">${jsonData[i].Name}</td>
          <td style="border: 1px solid black; padding: 8px;">${jsonData[i].Points}</td>
        `;
        table.appendChild(row);
      }

      dialog.appendChild(table); // Lisätään taulukko modal-ikkunaan

      dialog.showModal(); // Avaa dialogin
    });

    // Lisää tapahtumakuuntelija sulkupainikkeelle
    closeButton.addEventListener("click", function () {
      dialog.close(); // Sulkee dialogin
    });
  } catch (error) {
    console.log("Error:", error.message);
  }
}

// New game modal
function newGame() {
  const button = document.querySelector("#newGameButton");
  const dialog = document.querySelector("#gameModal");
  const closeButton = dialog.querySelector("#closeModal");
  const form = dialog.querySelector("#gameForm");

  button.addEventListener("click", function () {
    dialog.showModal();
  });

  closeButton.addEventListener("click", function () {
    dialog.close();
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault(); //

    const username = document.querySelector("#username").value;
    const difficulty = document.querySelector("#difficulty").value;
    const category = document.querySelector("#category").value;

    window.location.href =
      "game.html?username=" +
      encodeURIComponent(username) +
      "&difficulty=" +
      difficulty +
      "&category=" +
      encodeURIComponent(category);
  });
}

// Kutsutaan funktiot
leaderboard();
newGame();
