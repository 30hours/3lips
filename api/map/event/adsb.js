function event_adsb() {

  fetch(adsb_url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Update aircraft points based on new data
      updateAircraftPoints(data);
    })
    .catch(error => {
      // Handle errors during fetch
      console.error('Error during fetch:', error);
    })
    .finally(() => {
      // Schedule the next fetch after a delay (e.g., 5 seconds)
      setTimeout(event_adsb, 1000);
    });
}

// Function to update aircraft points
function updateAircraftPoints(data) {

  removeEntitiesOlderThanAndFade("adsb", 60, 0.5);

  // Process aircraft data and add points
  const aircraft = data.aircraft || [];
  aircraft.forEach(processAircraftData);
}

// Function to process aircraft data
function processAircraftData(aircraftData) {
  const icao = aircraftData.hex;
  const flight = aircraftData.flight;
  const lat = aircraftData.lat;
  const lon = aircraftData.lon;
  const alt = aircraftData.alt_baro;
  const seen_pos = aircraftData.seen_pos;

  // Check if the aircraft has valid position data
  if (lat !== undefined && lon !== undefined && alt !== undefined && seen_pos < 10) {
    addPoint(lat, lon, alt, flight, 'rgba(255, 0, 0, 0.5)', 10, "adsb", Date.now());
  }
}