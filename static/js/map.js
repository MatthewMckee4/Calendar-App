function initMap(latitude, longitude, description) {
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: latitude, lng: longitude },
        zoom: 8,
    });

    const marker = new google.maps.Marker({
        map: map,
        posistion: { lat: latitude, lng: longitude },
        title: description,
    });
}
