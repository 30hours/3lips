function event_radar() {

  var radar_url = window.location.origin + 
    '/api' + window.location.search;

  fetch(radar_url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    for (const key in data["detections_localised"]) {
      if (data["detections_localised"].hasOwnProperty(key)) {
        const target = data["detections_localised"][key];
        const points = target["points"];
        
        console.log(points);
        
      }
    }
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