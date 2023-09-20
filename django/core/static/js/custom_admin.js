$(document).ready(function(){

    // Move inlines to more appropriate place in the page
    $('.inline-group').detach().insertBefore($('.field-commentary').parent());

    // Set automatic language direction of various elements
    // so English (etc) content will be left to right (ltr)
    // and Arabic (etc) will be right to left (rtl)
    $('input, textarea').attr('dir', 'auto');

    // Warn users when they're leaving the page if there are any unsaved changes to the data
    var formHasSubmitted = false;
    function warnUsersLeavingActiveForm(){
        var form = $('#content-main form').first();
        var origForm = form.serialize();
        var formHasChanged = false;
        // If the form has changed, update the var to True (or if form has not changed reset to False)
        $('#content-main form :input').on('change input', function() { formHasChanged = form.serialize() !== origForm; });
        // Show an alert to stay on/leave the page if the form has changed
        $(window).on('beforeunload', function(){ if (formHasChanged && !formHasSubmitted) return "Leaving the page will lose unsaved changes"; });
    }
    // Execute above function on page load
    warnUsersLeavingActiveForm();
    // If certain actions taken then cancel the beforeunload event of warning users
    // If the main form is submitted
    $('#content-main form').first().on('submit', function(){ formHasSubmitted = true; });
    // If the user tries to delete the object
    $('.deletelink').on('click', function(){ formHasSubmitted = true; });

    // Open certain links in new tabs
    $('a.viewsitelink, a.related-widget-wrapper-link').attr('target', '_blank');

    // Customise the default option text for select lists (set as an empty string)
    $('select option[value=""]').text('')

    // Limit options in "Document Subtype" based on value of "Type"
    $('#id_type').on('change', function(){
        let textType = $(this).find('option:selected').text();
        let documentSubtype = $('#id_document_subtype');
        let documentSubtypeContainer = $('.field-document_subtype');
        // If selecting Administrative type
        if (textType.startsWith('Administrative')){
            documentSubtypeContainer.show();
            documentSubtype.find('option').each(function(){
                if ($(this).text().startsWith('Administrative')) $(this).show();
                else $(this).hide();
            });
            if (!documentSubtype.find('option:selected').text().startsWith('Administrative')) documentSubtype.val('');
        }
        // If selecting Legal type
        else if (textType.startsWith('Legal')){
            documentSubtypeContainer.show();
            documentSubtype.find('option').each(function(){
                if ($(this).text().startsWith('Legal')) $(this).show();
                else $(this).hide();
            });
            if (!documentSubtype.find('option:selected').text().startsWith('Legal')) documentSubtype.val('');
        }
        // If selecting none of the above
        else {
            documentSubtypeContainer.hide();
            documentSubtype.val('');
        }
    }).trigger('change');

});