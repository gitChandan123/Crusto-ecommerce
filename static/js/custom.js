// to get current year
function getYear() {
    var yearElement = document.querySelector("#displayYear");
    if (yearElement) {
        var currentYear = new Date().getFullYear();
        yearElement.innerHTML = currentYear;
    } else {
        console.warn("⚠️ Element with ID 'displayYear' not found.");
    }
}

getYear();



// isotope js
$(window).on('load', function () {
    $('.filters_menu li').click(function () {
        $('.filters_menu li').removeClass('active');
        $(this).addClass('active');

        var data = $(this).attr('data-filter');
        $grid.isotope({
            filter: data
        })
    });

    var $grid = $(".grid").isotope({
        itemSelector: ".all",
        percentPosition: false,
        masonry: {
            columnWidth: ".all"
        }
    })
});

// nice select
$(document).ready(function() {
    $('select').niceSelect();
  });

/** google_map js **/
function myMap() {
    var mapDiv = document.getElementById("googleMap"); // Ensure element exists

    if (!mapDiv) {
        console.error("Error: Map container with ID 'googleMap' not found!");
        return;
    }

    var mapProp = {
        center: { lat: 40.712775, lng: -74.005973 }, // Simplified LatLng object
        zoom: 18,
    };

    try {
        var map = new google.maps.Map(mapDiv, mapProp);
    } catch (error) {
        console.error("Error initializing Google Map:", error);
    }
}

$(document).ready(function () {
    $(".client_owl-carousel").owlCarousel({
        loop: true,
        margin: 0,
        dots: false,
        nav: true,
        autoplay: true,
        autoplayHoverPause: true,
        navText: [
            '<i class="fa fa-angle-left" aria-hidden="true"></i>',
            '<i class="fa fa-angle-right" aria-hidden="true"></i>'
        ],
        responsive: {
            0: { items: 1 },
            768: { items: 2 },
            1000: { items: 2 }
        }
    });
});
