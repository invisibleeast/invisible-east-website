// Load jQuery into admin dashboard
var jQueryScript = document.createElement('script');  
jQueryScript.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/3.7.0/jquery.min.js');
document.head.appendChild(jQueryScript);


$(document).ready(function(){

    // Move inlines to more appropriate place in the page
    $(".inline-group").detach().insertAfter($(".field-physical_additional_details").parent());

    // Set automatic language direction of various elements
    // so English (etc) content will be left to right (ltr)
    // and Arabic (etc) will be right to left (rtl)
    $('input, textarea').attr('dir', 'auto');

});