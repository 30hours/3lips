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

