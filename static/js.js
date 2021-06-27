//function initMap() {
//  latLng = new google.maps.LatLng(-8.064903, -34.896872)
//  var mapOptions = {
//    center: latLng,
//    zoom: 16,
//    mapTypeId: google.maps.MapTypeId.ROADMAP
//  };
//  var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
//
//  var marker = new google.maps.Marker({
//      position: latLng,
//      title:"Hello World!",
//      visible: true
//  });
//  marker.setMap(map);
//}

// Initialize and add the map
function initMap() {
  // The location of Uluru
  const uluru = { lat: -25.344, lng: 131.036 };
  // The map, centered at Uluru
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: uluru,
  });
  // The marker, positioned at Uluru
  const marker = new google.maps.Marker({
    position: uluru,
    map: map,
  });
}
//function initMap() {
//  const uluru = { lat: -25.363, lng: 131.044 };
//  const map = new google.maps.Map(document.getElementById("map"), {
//    zoom: 4,
//    center: { lat: 0, lng: 0 },
//  });
//  const contentString =
//    '<div id="content">' +
//    '<div id="siteNotice">' +
//    "</div>" +
//    '<h1 id="firstHeading" class="firstHeading">Uluru</h1>' +
//    '<div id="bodyContent">' +
//    "<p><b>Uluru</b>, also referred to as <b>Ayers Rock</b>, is a large " +
//    "sandstone rock formation in the southern part of the " +
//    "Northern Territory, central Australia. It lies 335&#160;km (208&#160;mi) " +
//    "south west of the nearest large town, Alice Springs; 450&#160;km " +
//    "(280&#160;mi) by road. Kata Tjuta and Uluru are the two major " +
//    "features of the Uluru - Kata Tjuta National Park. Uluru is " +
//    "sacred to the Pitjantjatjara and Yankunytjatjara, the " +
//    "Aboriginal people of the area. It has many springs, waterholes, " +
//    "rock caves and ancient paintings. Uluru is listed as a World " +
//    "Heritage Site.</p>" +
//    '<p>Attribution: Uluru, <a href="https://en.wikipedia.org/w/index.php?title=Uluru&oldid=297882194">' +
//    "https://en.wikipedia.org/w/index.php?title=Uluru</a> " +
//    "(last visited June 22, 2009).</p>" +
//    "</div>" +
//    "</div>";
//    // Create an array of alphabetical characters used to label the markers.
////  const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
//  // Add some markers to the map.
//  // Note: The code uses the JavaScript Array.prototype.map() method to
//  // create an array of markers based on a given "locations" array.
//  // The map() method here has nothing to do with the Google Maps API.
//  const infowindow = new google.maps.InfoWindow({
//    content: contentString,
//  });
////  const marker = locations.map((location, i) => {
////    return new google.maps.Marker({
////      position: location,
////      label: labels[i % labels.length],
////    });
////  });
////  // Add a marker clusterer to manage the markers.
////  new MarkerClusterer(map, markers, {
////    imagePath:
////      "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
////  });
//  const marker = new google.maps.Marker({
//    position: uluru,
//    map: map,
//    title: "Uluru (Ayers Rock)",
//  });
//  marker.addListener("click", () => {
//    infowindow.open({
//      anchor: marker,
//      map: map,
//      shouldFocus: false,
//    });
//  });
//}
////const locations = [
////  { lat: 51.5028, lng: 0.0877 },
////];