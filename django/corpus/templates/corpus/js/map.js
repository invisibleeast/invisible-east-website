// Create a map object
var map = L.map(
    '{{ map_id }}', {scrollWheelZoom: false, attributionControl: false}
).setView(['32.1331', '49.0672'], 6);

// Set tile layer style
L.tileLayer(
    `https://api.mapbox.com/styles/v1/mapbox/light-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoibmlja255ciIsImEiOiJjajduNGptZWQxZml2MndvNjk4eGtwbDRkIn0.L0aWwfHlFJVGa-WOj7EHaA`,
    {
        maxZoom: 12,
        minZoom: 4,
        id: 'default',
    }
).addTo(map);

// Loop through toponyms that have coordinates data, adding popup markers containing details of each toponym (e.g. urls and links to all texts)
{% for toponym in toponyms_list %}
    {% if toponym.latitude and toponym.longitude %}

        // Start popup html with the tag name
        var markerPopupHtml = `<div class="map-iedctoponyms-popup-title">{{ toponym.name }}</div>`;

        // Add alternative readings
        {% if toponym.alternative_readings %}
            markerPopupHtml += '<div class="map-iedctoponyms-popup-subtitle">Alternative Readings</div>{{ toponym.alternative_readings }}';
        {% endif %}

        // Add alternative pronunciations
        {% if toponym.alternative_pronunciations %}
            markerPopupHtml += '<div class="map-iedctoponyms-popup-subtitle">Alternative Pronunciations</div>{{ toponym.alternative_pronunciations }}';
        {% endif %}

        // Add urls html (if exists)
        {% if toponym.urls_as_html_links %}
            markerPopupHtml += '<div class="map-iedctoponyms-popup-subtitle">Links</div>{{ toponym.urls_as_html_links }}';
        {% endif %}

        // Add texts
        {% if toponym.texts.all %}
            // Add subtitle for texts, if there are any
            markerPopupHtml += '<div class="map-iedctoponyms-popup-subtitle">Texts</div>';
            // Loop through all Texts to build list of texts
            {% for text in toponym.texts.all %}
                markerPopupHtml += `<a href="/corpus/{{ text.id }}/" class="map-iedctoponyms-popup-text">{{ text }}</a>`;
            {% endfor %}
        {% endif %}

        // Inject a marker for this toponym on the map, with a popup containing the HTML created above
        L.marker([{{ toponym.latitude }}, {{ toponym.longitude }}]).addTo(map).bindPopup(markerPopupHtml);

    {% endif %}
{% endfor %}

// Fix map
$('#corpus-text-detail-content-tabs li#map').on('click', function(){
    map.invalidateSize(true);
});