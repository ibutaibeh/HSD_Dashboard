
document.addEventListener('DOMContentLoaded',()=>{
    var mapDiv = document.getElementById('map');
    if(!mapDiv) return;

    var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  minZoom: 9,
  attribution: '© OpenStreetMap contributors'
});
var esriSat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  maxZoom: 15,
  minZoom: 9,
  attribution: 'Tiles © Esri'
});

var map = L.map('map', {
  center: [26.0667, 50.5577],
  zoom: 10,
  layers: [esriSat]
});

var baseMaps = {
  "Street Map": osm,
  "Satellite": esriSat
};

L.control.layers(baseMaps).addTo(map);

//Map tools for creating and store polygons
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var drawControl = new L.Control.Draw({
  edit: {
    featureGroup: drawnItems
  },
  draw: {
  polygon: true,
  polyline: false,
  rectangle: false,
  circle: false,
  marker: false,
  circlemarker: false

  }
});
map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, function (e) {
  drawnItems.clearLayers();
  var layer = e.layer;
  drawnItems.addLayer(layer);
  document.getElementById("id_location").value =
    JSON.stringify(layer.toGeoJSON().geometry);
});

map.on(L.Draw.Event.EDITED, function (e) {
  e.layers.eachLayer(function (layer) {
    document.getElementById("id_location").value =
      JSON.stringify(layer.toGeoJSON().geometry);
  });
});


});
