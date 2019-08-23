var map = L.map('map').setView([28.5383, -81.3792], 13);

// var tileString = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
var tileString = 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png'
var OpenStreetMap_Mapnik = L.tileLayer(tileString, {
	maxZoom: 19,
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var maxTraffic = 234069.728928;


function getStyle(weight){
	return function(feature) {
	    return {
	        fillColor: '#830303',
	        weight: weight*(feature.properties.Traffic/maxTraffic),
	        color: '#830303'
	    };
	}
}

var Roadlines = new L.GeoJSON.AJAX("./test.json", {style: getStyle(20)});       
// var Devices = new L.GeoJSON.AJAX("../data/Traffic/ptms/geojson/ptms.json");       

Roadlines.addTo(map);

var hour = 1;
setInterval(function(){
	var weight = Math.abs((hour%26+1)-13)+9;
    Roadlines.setStyle(getStyle(weight));
	hour += 1;
}, 50);