// config mapbox gl access token
mapboxgl.accessToken = 'pk.eyJ1IjoidGVrbm9sb2ciLCJhIjoiSThJdmhyRSJ9.zq2xC8EwFXLPixOdVza98A';


var map = new mapboxgl.Map({
    container: 'map', // container id
    style: 'mapbox://styles/mapbox/streets-v9', //stylesheet location
    center: [-122.4351, 37.7612], // starting position
    zoom: 12 // starting zoom
});

function draw_points(data_points) {
    // console.log(JSON.stringify(data_points));
    map.addSource('points', {
        "type": "geojson",
        "data": data_points
    });

    map.addLayer({
        "id": "points",
        "type": "circle",
        "paint": {
            "circle-radius": 8,
            "circle-color": "#007cbf"
        },
        "source": "points"
    });
}

map.on('load', function () {
    $.ajax ({
        url: "http://localhost:5000/v1/hello", // <--- returns valid json if accessed in the browser
        type: "GET",
        dataType: "json",
        cache: false,
        contentType: "application/json",
        success: function(data) {
            draw_points(data);
            console.log("success");

        },
        error: function(data) {
            alert("Somthing is wrong, please check your console!");
            console.log(data);
        }
    });

    function animateMarker() {

        $.ajax ({
            url: "http://localhost:5000/v1/hello", // <--- returns valid json if accessed in the browser
            type: "GET",
            dataType: "json",
            cache: false,
            contentType: "application/json",
            success: function(data) {
                map.getSource('points').setData(data);
                console.log("success");

            },
            error: function(data) {
                alert("Somthing is wrong, please check your console!");
                console.log(data);
            }});
    
        // Request the next frame of the animation.
        setTimeout(function() {
            requestAnimationFrame(animateMarker);
        }, 1500);
    }

    // Start the animation.
    setTimeout(function () { animateMarker(); }, 1500);
});

// map.on('load', function () {
//     $.getJSON( "http://localhost:5000/v1/hello?jsoncallback=?", function( data ) {
//         console.log(data);

//         map.addLayer({
//             "id": "points",
//             "type": "symbol",
//             "source": {
//                 "type": "geojson",
//                 "data": {
//                     "type": "FeatureCollection",
//                     "features": [{
//                         "type": "Feature",
//                         "geometry": {
//                             "type": "Point",
//                             "coordinates": [-122.477, 37.7312]
//                         },
//                         "properties": {
//                             "title": "request",
//                             "icon": "monument"
//                         }
//                     }, {
//                         "type": "Feature",
//                         "geometry": {
//                             "type": "Point",
//                             "coordinates": [-122.43507, 37.76121]
//                         },
//                         "properties": {
//                             "title": "Mapbox SF",
//                             "icon": "harbor"
//                         }
//                     }]
//                 }
//             },
//             "layout": {
//                 "icon-image": "{icon}-15",
//                 "text-field": "{title}",
//                 "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
//                 "text-offset": [0, 0.6],
//                 "text-anchor": "top"
//             }
//         });
//     });
// });
