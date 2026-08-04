document.addEventListener('DOMContentLoaded', function () {
  var mapEl = document.getElementById('route-map');
  if (!mapEl || typeof L === 'undefined' || typeof L.GPX === 'undefined') return;

  var gpxUrl = mapEl.dataset.gpx;
  var elevationEl = document.getElementById('route-elevation');
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
    var gpx = e.target;
    map.fitBounds(gpx.getBounds());
    if (elevationEl) {
      drawElevationProfile(elevationEl, gpx.get_elevation_data(), gpx.get_elevation_gain());
    }
  }).addTo(map);

  function drawElevationProfile(container, points, elevationGain) {
    if (!points || points.length < 2) return;

    var width = 600, height = 120, padding = 4;
    var maxDist = points[points.length - 1][0];
    var elevations = points.map(function (p) { return p[1]; });
    var minEle = Math.min.apply(null, elevations);
    var maxEle = Math.max.apply(null, elevations);
    var eleRange = Math.max(maxEle - minEle, 1);

    function x(d) { return padding + (d / maxDist) * (width - 2 * padding); }
    function y(e) { return height - padding - ((e - minEle) / eleRange) * (height - 2 * padding); }

    var linePoints = points.map(function (p) { return x(p[0]) + ',' + y(p[1]); }).join(' ');
    var areaPoints = linePoints + ' ' + x(maxDist) + ',' + height + ' ' + x(0) + ',' + height;

    container.innerHTML =
      '<svg viewBox="0 0 ' + width + ' ' + height + '" preserveAspectRatio="none" role="img" aria-label="Profil altimétrique du parcours">' +
      '<polygon points="' + areaPoints + '" class="elevation-area"></polygon>' +
      '<polyline points="' + linePoints + '" class="elevation-line"></polyline>' +
      '</svg>' +
      '<div class="elevation-stats">' +
      '<span>D+ ' + Math.round(elevationGain) + ' m</span>' +
      '<span>Alt. ' + Math.round(minEle) + '–' + Math.round(maxEle) + ' m</span>' +
      '</div>';
  }
});
