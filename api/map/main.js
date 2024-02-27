// default camera to Australia
var extent = Cesium.Rectangle.fromDegrees(138.44, -35.19, 138.93, -34.51);
Cesium.Camera.DEFAULT_VIEW_RECTANGLE = extent;
Cesium.Camera.DEFAULT_VIEW_FACTOR = 0;

var imageryProviders = [];

imageryProviders.push(new Cesium.ProviderViewModel({
	name: "ESRI Adelaide",
	iconUrl: './icon/esri.jpg',
	tooltip: 'ESRI Adelaide Tiles',
	category: 'Offline',
	creationFunction: function() {
		return new Cesium.UrlTemplateImageryProvider({
			url: 'https://tile.datr.dev/data/esri-adelaide/{z}/{x}/{y}.jpg',
      credit: 'Esri, Maxar, Earthstar Geographics, USDA FSA, USGS, Aerogrid, IGN, IGP, and the GIS User Community',
			maximumLevel: 20,
		});
	}
}));

imageryProviders.push(new Cesium.ProviderViewModel({
	name: "MapBox Streets v11",
	iconUrl: './icon/mapBoxStreets.png',
	tooltip: 'MapBox Streets v11 Tiles',
	category: 'Offline',
	creationFunction: function() {
		return new Cesium.UrlTemplateImageryProvider({
			url: 'https://tile.datr.dev/data/mapbox-streets-v11/{z}/{x}/{y}.png',
      credit: '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> <strong><a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a></strong>',
			maximumLevel: 16,
		});
	}
}));

imageryProviders.push(new Cesium.ProviderViewModel({
	name: "MapBox Dark v10",
	iconUrl: './icon/mapBoxDark.png',
	tooltip: 'MapBox Dark v10 Tiles',
	category: 'Offline',
	creationFunction: function() {
		return new Cesium.UrlTemplateImageryProvider({
			url: 'https://tile.datr.dev/data/mapbox-dark-v10/{z}/{x}/{y}.png',
      credit: '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> <strong><a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a></strong>',
			maximumLevel: 16,
		});
	}
}));

imageryProviders.push(new Cesium.ProviderViewModel({
	name: "ESRI",
	iconUrl: './icon/esri.jpg',
	tooltip: 'ESRI Tiles',
	category: 'Offline',
	creationFunction: function() {
		return new Cesium.UrlTemplateImageryProvider({
			url: 'https://tile.datr.dev/data/esri/{z}/{x}/{y}.jpg',
      credit: 'Esri, Maxar, Earthstar Geographics, USDA FSA, USGS, Aerogrid, IGN, IGP, and the GIS User Community',
			maximumLevel: 16,
		});
	}
}));

imageryProviders.push(new Cesium.ProviderViewModel({
	name: "OpenTopoMap",
	iconUrl: './icon/opentopomap.png',
	tooltip: 'OpenTopoMap Tiles',
	category: 'Offline',
	creationFunction: function() {
		return new Cesium.UrlTemplateImageryProvider({
			url: 'https://tile.datr.dev/data/opentopomap/{z}/{x}/{y}.png',
      credit: '<code>Kartendaten: © <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>-Mitwirkende, SRTM | Kartendarstellung: © <a href="http://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)</code>',
			maximumLevel: 8,
		});
	}
}));

var terrainProviders = [];

terrainProviders.push(new Cesium.ProviderViewModel({
	name: "WGS84 Ellipsoid",
	iconUrl: './icon/opentopomap.png',
	tooltip: 'WGS84 Ellipsoid Terrain',
	category: 'Offline',
	creationFunction: function() {
		return new Cesium.EllipsoidTerrainProvider({
		});
	}
}));

terrainProviders.push(new Cesium.ProviderViewModel({
	name: "30m Adelaide",
	iconUrl: './icon/opentopomap.png',
	tooltip: '30m Adelaide Terrain',
	category: 'Offline',
	creationFunction: function() {
		return Cesium.CesiumTerrainProvider.fromUrl(
      'https://terrain.datr.dev/data/30m_adelaide/'
		);
	}
}));

terrainProviders.push(new Cesium.ProviderViewModel({
	name: "90m Australia",
	iconUrl: './icon/opentopomap.png',
	tooltip: '90m Australia Terrain',
	category: 'Offline',
	creationFunction: function() {
		return Cesium.CesiumTerrainProvider.fromUrl(
      'https://terrain.datr.dev/data/90m_australia/'
		);
	}
}));

terrainProviders.push(new Cesium.ProviderViewModel({
	name: "90m South Australia",
	iconUrl: './icon/opentopomap.png',
	tooltip: '90m South Australia Terrain',
	category: 'Offline',
	creationFunction: function() {
		return Cesium.CesiumTerrainProvider.fromUrl(
      'https://terrain.datr.dev/data/90m_south_australia/'
		);
	}
}));

var viewer = new Cesium.Viewer("cesiumContainer", {
	baseLayerPicker: true,
	imageryProviderViewModels: imageryProviders,
	terrainProviderViewModels: terrainProviders,
	geocoder: false,
	shouldAnimate: true,
	selectionIndicator: false
});

/**
 * @brief Adds a point to Cesium viewer with specified parameters.
 * @param {number} latitude - The latitude of the point in degrees.
 * @param {number} longitude - The longitude of the point in degrees.
 * @param {number} altitude - The altitude of the point in meters.
 * @param {string} pointName - The name of the point.
 * @param {string} pointColor - The color of the point in CSS color string format.
 * @param {number} timestamp - The timestamp in UNIX milliseconds indicating when the point was added.
 * @returns {Entity} The Cesium Entity representing the added point.
 */
 function addPoint(latitude, longitude, altitude, pointName, pointColor, pointSize, type, timestamp) {
  // Convert latitude, longitude, altitude to Cartesian coordinates (ECEF)
  const position = Cesium.Cartesian3.fromDegrees(longitude, latitude, altitude);

  // Create a point entity
  const pointEntity = viewer.entities.add({
      name: pointName,
      position,
      point: {
          color: Cesium.Color.fromCssColorString(pointColor),
          pixelSize: pointSize,
      },
      label: (type === "radar") ? {
          text: pointName,
          showBackground: true,
          backgroundColor: Cesium.Color.BLACK,
          font: '14px sans-serif',
          pixelOffset: new Cesium.Cartesian2(0, -20),
      } : undefined,
      properties: {
          timestamp,
          type,
      },
  });

  return pointEntity;
}

// global vars
var adsb_url;
var adsbEntities = {};

var style_adsb = {};
style_adsb.color = 'rgba(255, 0, 0, 0.5)';
style_adsb.pointSize = 8;
style_adsb.type = "adsb";

window.addEventListener('load', function () {

  // add radar points
  const radar_names = new URLSearchParams(
    window.location.search).getAll('server');
  console.log(radar_names);
  var radar_config_url = radar_names.map(
    url => `http://${url}/api/config`);
  if (this.window.location.protocol === "https:") {
    radar_config_url = radar_config_url.map(
      url => url.replace(/^http:/, 'https:'));
  }
  var style_radar = {};
  style_radar.color = 'rgba(0, 0, 0, 1.0)';
  style_radar.pointSize = 10;
  style_radar.type = "radar";
  style_radar.timestamp = Date.now();
  radar_config_url.forEach(url => {
    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        // add radar rx and tx
        if (!doesEntityNameExist(data.location.rx.name)) {
          addPoint(
            data.location.rx.latitude, 
            data.location.rx.longitude, 
            data.location.rx.altitude, 
            data.location.rx.name, 
            style_radar.color, 
            style_radar.pointSize, 
            style_radar.type, 
            style_radar.timestamp
          );
        }
        if (!doesEntityNameExist(data.location.tx.name)) {
          addPoint(
            data.location.tx.latitude, 
            data.location.tx.longitude, 
            data.location.tx.altitude, 
            data.location.tx.name, 
            style_radar.color, 
            style_radar.pointSize, 
            style_radar.type, 
            style_radar.timestamp
          );
        }
      })
      .catch(error => {
        // Handle errors during fetch
        console.error('Error during fetch:', error);
      });
  });

  // get detection data URL

  // get truth URL
  adsb_url = new URLSearchParams(
    window.location.search).get('adsb').split('&');
  adsb_url = adsb_url.map(
    url => `http://${url}/data/aircraft.json`);
  if (this.window.location.protocol === "https:") {
    adsb_url = adsb_url.map(
      url => url.replace(/^http:/, 'https:'));
  }
  adsb_url = adsb_url[0];

  // call event loops
  event_adsb();
  event_radar();

})

function removeEntitiesOlderThan(entityType, maxAgeSeconds) {

  var entities = viewer.entities.values;
  for (var i = entities.length - 1; i >= 0; i--) {
    var entity = entities[i];
    const type = entity.properties["type"].getValue();
    const timestamp = entity.properties["timestamp"].getValue();
    if (entity.properties && entity.properties["type"] && 
      entity.properties["type"].getValue() === entityType &&
      Date.now()-timestamp > maxAgeSeconds*1000) {
        viewer.entities.remove(entity);
    }
  }

}

function removeEntitiesOlderThanAndFade(entityType, maxAgeSeconds, baseAlpha) {

  var entities = viewer.entities.values;
  for (var i = entities.length - 1; i >= 0; i--) {
    var entity = entities[i];
    const type = entity.properties["type"].getValue();
    const timestamp = entity.properties["timestamp"].getValue();
    if (entity.properties && entity.properties["type"] && 
      entity.properties["type"].getValue() === entityType &&
      Date.now()-timestamp > maxAgeSeconds*1000) {
        viewer.entities.remove(entity);
    }
    else {
      entity.point.color = new Cesium.Color.fromAlpha(
        entity.point.color.getValue(), baseAlpha*(1-(Date.now()-timestamp)/(maxAgeSeconds*1000)));
    }
  }

}

function removeEntitiesByType(entityType) {

  var entities = viewer.entities.values;
  for (var i = entities.length - 1; i >= 0; i--) {
    var entity = entities[i];
    if (entity.properties && entity.properties["type"] && 
      entity.properties["type"].getValue() === entityType) {
        viewer.entities.remove(entity);
    }
  }
}

function doesEntityNameExist(name) {
  for (const entity of viewer.entities.values) {
    if (entity.name === name) {
      return true;
    }
  }
  return false;
}