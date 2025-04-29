"use strict";

async function leaderboard() {
  try {
    // Fetching data from server
    const response = await fetch("http://127.0.0.1:5000/leaderboard");
    const jsonData = await response.json();

    const button = document.querySelector("#leaderboard");
    const dialog = document.querySelector("dialog");
    const closeButton = dialog.querySelector("span"); // Sulkemismerkki

    button.addEventListener("click", function () {
      dialog.innerHTML = ""; // Clear dialog content

      dialog.appendChild(closeButton);

      // Add leaderboard data to dialog
      for (let i = 0; i < jsonData.length; i++) {
        const listItem = document.createElement("p");
        listItem.textContent = jsonData[i].Name + ": " + jsonData[i].Points;
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

leaderboard();
