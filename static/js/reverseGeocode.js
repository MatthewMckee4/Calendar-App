let reverseGeocode;

document.addEventListener('DOMContentLoaded', function() {
    reverseGeocode = function(lat, lng, callback) {
        const geocoder = new google.maps.Geocoder();
        const location = { lat: parseFloat(lat), lng: parseFloat(lng) };

        geocoder.geocode({ 'location': location }, function(results, status) {
            if (status === 'OK') {
                if (results[0]) {
                    console.log(results[0].formatted_address);
                    callback(results[0].formatted_address);      
                } else {
                    console.error('No results found');
                    callback('No results found');
                }
            } else {
                console.error('Geocoder failed due to: ' + status);
                callback('Geocoder failed due to: ' + status);
            }
        });
    };
});
