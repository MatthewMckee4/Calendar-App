function reverseGeocode(lat, lng, elementId) {
    var geocoder = new google.maps.Geocoder();
    var latlng = { lat: parseFloat(lat), lng: parseFloat(lng) };

    geocoder.geocode({ location: latlng }, function (results, status) {
        if (status === "OK") {
            if (results[0]) {
                var placeName = "";
                for (var i = 0; i < results.length; i++) {
                    if (results[i].types.includes("locality")) {
                        placeName = results[i].formatted_address;
                        break;
                    }
                }
                placeName = placeName || results[0].formatted_address;
                document.getElementById(elementId).textContent =
                    "Location: " + placeName;
            } else {
                document.getElementById(elementId).textContent =
                    "Location: No results found";
            }
        } else {
            document.getElementById(elementId).textContent =
                "Location: Geocoder failed due to: " + status;
        }
    });
}

function updateLocation(lat, lng, elementId) {
    reverseGeocode(lat, lng, elementId);
}
