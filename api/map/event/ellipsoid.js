function event_ellipsoid() {

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
    for (const key in data["ellipsoids"]) {
      if (data["ellipsoids"].hasOwnProperty(key)) {
        const points = data["ellipsoids"][key];
        console.log(points);

        removeEntitiesOlderThanAndFade("ellipsoids", 30, 0.5);

        for (const point in points) {
          addPoint(
            points[point][0], 
            points[point][1], 
            points[point][2], 
            "ellipsoids", 
            style_ellipsoid.color, 
            style_ellipsoid.pointSize, 
            style_ellipsoid.type, 
            Date.now()
          );
        }
        
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

var style_ellipsoid = {};
style_ellipsoid.color = 'rgba(0, 0, 255, 1.0)';
style_ellipsoid.pointSize = 16;
style_ellipsoid.type = "ellipsoids";
style_ellipsoid.timestamp = Date.now();