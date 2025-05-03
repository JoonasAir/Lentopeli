// Alustetaan kartta
const routes = [];
const map = L.map("map").setView([60.1756, 24.9342], 10);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// Asynkroninen funktio koordinaattien hakemiseen
async function fetchCoordinates() {
  try {
    // Haetaan koordinaatit backendistä
    /*  const response = await fetch("http://127.0.0.1:5000/flyto");
    if (!response.ok) {
      throw new Error("HTTP-virhe: " + response.status);
    }

    // Muunnetaan vastaus JSON-muotoon
    const jsonData = await response.json(); */

    const points = [
      [60.1756, 24.9342],
      [52.3667, 4.8833],
    ];

    // Päivitetään pisteiden käsittely vastaamaan uutta JSON-rakennetta
    /* const points = [
      [parseFloat(jsonData.from.latitude), parseFloat(jsonData.from.longitude)], // Lähtöpiste
      [parseFloat(jsonData.to.latitude), parseFloat(jsonData.to.longitude)], // Määränpää
    ];
 */

    // Piirretään viiva kartalle
    const polyline = L.polyline(points, { color: "blue" }).addTo(map);

    // Keskitetään kartta reitin ympärille
    const bounds = polyline.getBounds();
    map.fitBounds(bounds, {
      padding: [100, 100],
      maxZoom: 10,
    });

    // Lentokoneikoni
    const airplaneIcon = L.icon({
      iconUrl: "../images/plane.png",
      iconSize: [32, 32],
      iconAnchor: [16, 16],
    });

    // Lentokone aloituspisteeseen
    const airplaneMarker = L.marker(points[0], { icon: airplaneIcon }).addTo(
      map
    );

    // Animaation asetukset
    let progress = 0;
    let steps = 150;
    let interval = 20;
    let start = points[0];
    let end = points[1];

    function animateAirplane() {
      if (progress >= 1) {
        map.removeLayer(polyline);
        map.flyTo(end, 8, { duration: 3 });
        routes.push(points);
      } else {
        progress += 1 / steps;
        const lat = start[0] + (end[0] - start[0]) * progress;
        const lng = start[1] + (end[1] - start[1]) * progress;

        airplaneMarker.setLatLng([lat, lng]);
        setTimeout(animateAirplane, interval);
      }
    }

    animateAirplane();
  } catch (error) {
    console.log("Virhe haettaessa tietoa:", error.message);
  }
}

// Käynnistetään tietojen haku
fetchCoordinates();
