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
      dialog.innerHTML = ""; // Clear dialog content

      dialog.appendChild(closeButton);

      // Add leaderboard data to dialog
      for (let i = 0; i < jsonData.length && i < 10; i++) {
        const listItem = document.createElement("p");
        listItem.textContent =
          i + 1 + ". " + jsonData[i].Name + ": " + jsonData[i].Points;
        dialog.appendChild(listItem);
      }

      dialog.showModal(); // Open dialog
    });

    // Adding event listener to close button
    closeButton.addEventListener("click", function () {
      dialog.close(); // Close dialog
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
      category;
  });
}

// Kutsutaan funktiot
leaderboard();
newGame();
