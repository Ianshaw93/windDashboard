// This example displays a marker at the center of Australia.
// When the user clicks the marker, an info window opens.

// This example displays a marker at the center of Australia.
// When the user clicks the marker, an info window opens.
var test_name = 42;
function initMap(test_name=45) {
  const uluru = { lat: 51.5028, lng: 0.0877 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: uluru,
  });
  const contentString =
    'The wind speed is ${test_name}';
  const infowindow = new google.maps.InfoWindow({
    content: contentString,
  });
  const marker = new google.maps.Marker({
    position: uluru,
    map,
    title: "Uluru (Ayers Rock)",
  });
  marker.addListener("click", () => {
    infowindow.open({
      anchor: marker,
      map,
      shouldFocus: false,
    });
  });
}