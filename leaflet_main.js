//js file
console.log("Step 0 - load file");

// this is a function - later we will make it run once (on load)
function loadMap() {
	// Step 1 : set up basemap (cartodb, tilemile or tilelayer)
	console.log("Step 1 - set up map");

	// create a leaflet map in the container map id and then set it to zoom to london with lat long coordinates, zoom
	// into my empty container <div id="mapid"></div>
	var map = L.map('mapid').setView([51.505, -0.09], 13);
	L.tileLayer('http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', { maxZoom: 18,  }).addTo(map);

	// Step 2 : Load data using JQuery - explanation : (http://api.jquery.com/jquery.getjson/)
	jQuery.getJSON('events.json', function(data){
		// important javascript concept: the jQuery.getJSON doesn't return data,
		// instead you pass a callback function (like this function)
		// then when the data is available, the function runs.
		console.log("Step 2 - data loaded");
		console.log(data);
		L.geoJson(data,{
			onEachFeature: function (feature, layer) {
				// this is another callback function, that leaflet uses
				// to add a popup to each marker
				layer.bindPopup(feature.properties.name);
			}
		}).addTo(map);
	});

	//interactions

	// timeline

} //Close function



// once the page is ready, run loadMap
// this runs once and add the listener to the browser
if(window.addEventListener){
	// here loadMap is the callback function; it will run when the browser is done loading the page
	window.addEventListener('DOMContentLoaded', loadMap, false);
} else {
	window.onload=loadMap;
}
