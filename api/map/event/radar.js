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

        console.log(target);
        console.log(points);

        removeEntitiesOlderThanAndFade("detection", 60, 0.5);

        for (const point in points) {
          addPoint(
            points[point][0], 
            points[point][1], 
            points[point][2], 
            "detection", 
            style_point.color, 
            style_point.pointSize, 
            style_point.type, 
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

var style_point = {};
style_point.color = 'rgba(0, 255, 0, 1.0)';
style_point.pointSize = 16;
style_point.type = "detection";
style_point.timestamp = Date.now();