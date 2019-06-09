

function renderMap(elementId, latitude, longitude, accessToken) {
    var map  = L.map(elementId).setView([latitude, longitude], 12);
    var attribution = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery ©<a href="https://www.mapbox.com/">Mapbox</a>'
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        maxZoom: 18,
        id: 'mapbox.streets',
        attribution: attribution,
        accessToken: accessToken
    }).addTo(map);
}
