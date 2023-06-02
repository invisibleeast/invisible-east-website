// Load jQuery into admin dashboard
var jQueryScript = document.createElement('script');  
jQueryScript.setAttribute('src','https://ajax.googleapis.com/ajax/libs/jquery/3.7.0/jquery.min.js');
document.head.appendChild(jQueryScript);


$(document).ready(function(){

    // Move inlines to more appropriate place in the page
    $("#document_persons-group").detach().insertAfter(".field-place");
    $("#document_dates-group").detach().insertAfter("#document_persons-group");

});