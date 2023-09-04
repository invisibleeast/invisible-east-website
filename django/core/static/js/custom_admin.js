$(document).ready(function(){

    // Move inlines to more appropriate place in the page
    $('.inline-group').detach().insertBefore($('.field-commentary').parent());

    // Set automatic language direction of various elements
    // so English (etc) content will be left to right (ltr)
    // and Arabic (etc) will be right to left (rtl)
    $('input, textarea').attr('dir', 'auto');

});