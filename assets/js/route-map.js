document.addEventListener('DOMContentLoaded', function () {
  var mapEl = document.getElementById('route-map');
  if (!mapEl || typeof L === 'undefined' || typeof L.GPX === 'undefined') return;

  var gpxUrl = mapEl.dataset.gpx;
  var iconBase = 'https://unpkg.com/leaflet-gpx@1.7.0/';

  var map = L.map(mapEl, { scrollWheelZoom: false });
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19
  }).addTo(map);

  new L.GPX(gpxUrl, {
    async: true,
    marker_options: {
      startIconUrl: iconBase + 'pin-icon-start.png',
      endIconUrl: iconBase + 'pin-icon-end.png',
      shadowUrl: iconBase + 'pin-shadow.png'
    }
  }).on('loaded', function (e) {
    map.fitBounds(e.target.getBounds());
  }).addTo(map);
});
