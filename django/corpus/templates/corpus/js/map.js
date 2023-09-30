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

// Loop through toponym tags that have coordinates data, adding popup markers containing links to all texts
{% for tag in tags_list %}
    {% if tag.latitude and tag.longitude %}

        // Start popup html with the tag name
        var markerPopupHtml = `<div class="map-taggedtexts-popup-title">{{ tag.name }}</div>`;

        // Add urls html (if exists)
        {% if tag.urls_as_html_links %}
            markerPopupHtml += '<div class="map-taggedtexts-popup-subtitle">Links</div>{{ tag.urls_as_html_links }}';
        {% endif %}

        // Loop through all Text Folio Tags and add their grandparent Text to list of texts
        var texts = [];
        {% for text_folio_tag in tag.text_folio_tags.all %}
            text_obj = {
                'id': '{{ text_folio_tag.text_folio.text.id }}',
                'label': '{{ text_folio_tag.text_folio.text }}'
            }
            texts.push(text_obj);
        {% endfor %}

        // Tidy list:
        texts = texts.filter((v,i,a)=>a.findIndex(v2=>(v2.id===v.id))===i)  // Remove duplicates
        texts.sort((a, b) => a.label.localeCompare(b.label));  // Sort by label

        // Add subtitle for texts, if there are any
        if (texts.length) markerPopupHtml += '<div class="map-taggedtexts-popup-subtitle">Texts</div>';

        // Create and append popup html for each text
        texts.forEach(function(text){
            markerPopupHtml += `<a href="/corpus/${text.id}/" class="map-taggedtexts-popup-text">${text.label}</a>`;
        });

        // Add a marker for this toponym tag on the map, with a popup containing the HTML created above
        L.marker([{{ tag.latitude }}, {{ tag.longitude }}]).addTo(map).bindPopup(markerPopupHtml);

    {% endif %}
{% endfor %}

// Fix map
$('#corpus-text-detail-content-tabs li#map').on('click', function(){
    map.invalidateSize(true);
});