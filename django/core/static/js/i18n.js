$(document).ready(function() {

    function getCookie(name) {
        // Convert cookies string to list
        var c_list = document.cookie.split("; "),
            i = 0,
            c,
            c_name,
            c_value;
        // Loop through cookies list to find a match
        for (i = 0; i < c_list.length; i++) {
            // Find cookie
            c = c_list[i].split('=');
            c_name = c[0];
            c_value = c[1];
            // Return cookie value if cookie name matches
            if (c_name === name) {
                return c_value;
            }
        }
        // If no cookie found with given name, return null
        return null;
    }

    // Language / Translation / i18n

    // Add link to current page in specified language
    // The a tag must have a data-langcode="(code)" attribute
    $('a[data-langcode]').each(function(){
        var urlCurrent = window.location.pathname.split('/');
        var langCode = $(this).attr('data-langcode');
        // Add 'active' class if this is the current language
        if(urlCurrent[1] === langCode) $(this).addClass('active');
        // If language is default (English) remove language codes from URL start
        if (langCode === 'en'){
            if (['fa', 'en'].includes(urlCurrent[1])) urlCurrent.splice(1, 1);
        }
        // If language is not default (so not English) then add language code to URL start
        else if (urlCurrent[1] !== langCode){
            urlCurrent.splice(1, 0, langCode);
        }
        // Set href for this language link
        $(this).attr('href', urlCurrent.join('/') + window.location.search);
    });

    $('a[data-langcode]').on('click', function(e){
        e.preventDefault();
        // Set the languageHasBeenSetManually cookie if not yet set, to show the user has at some point set the language
        if(getCookie('languageHasBeenSetManually') != '1'){
            document.cookie = "languageHasBeenSetManually=1; expires=Mon, 31 Dec 2080 23:59:59 GMT; path=/;";
        }
        window.location.href = $(this).attr('href');
    });

    $('#nav-languagelinks-toggle').on('click', function(){
        var langCode = $(this).attr('data-langcode');
        if (langCode == 'en') langCode = 'fa';
        else langCode = 'en';
        $(`a[data-langcode="${langCode}"]`).trigger('click');
    });

    // Redirect the user automatically to Persian if timezone is in Asia
    // unless the user has already manually set the language (via the cookie languageHasBeenSetManually)
    let timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (
        getCookie('languageHasBeenSetManually') != '1'
        && timezone.startsWith("Asia/")
        && !window.location.pathname.startsWith('/fa/')
    ){
        window.location.href = `/fa${window.location.pathname}`;
    }

});