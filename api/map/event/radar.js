function event_radar() {

  radar_url = window.location.origin + '/api' + window.location.search;
  console.log(radar_url);

  fetch(radar_url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Update aircraft points based on new data
    console.log("test");
  })
  .catch(error => {
    // Handle errors during fetch
    console.error('Error during fetch:', error);
  })
  .finally(() => {
    // Schedule the next fetch after a delay (e.g., 5 seconds)
    setTimeout(event_radar, 1000);
  });

}