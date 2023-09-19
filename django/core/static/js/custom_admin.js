$(document).ready(function(){

    // Move inlines to more appropriate place in the page
    $('.inline-group').detach().insertBefore($('.field-commentary').parent());

    // Set automatic language direction of various elements
    // so English (etc) content will be left to right (ltr)
    // and Arabic (etc) will be right to left (rtl)
    $('input, textarea').attr('dir', 'auto');

    // Warn users when they're leaving the page if there are any unsaved changes to the data
    function warnUsersLeavingActiveForm(){
        var form = $('#content-main form').first();
        var origForm = form.serialize();
        var formHasChanged = false;
        // If the form has changed, update the var to True (or if form has not changed reset to False)
        $('#content-main form :input').on('change input', function() { formHasChanged = form.serialize() !== origForm; });
        // Show an alert to stay on/leave the page if the form has changed
        $(window).on('beforeunload', function(){ if (formHasChanged) return "Leaving the page will lose unsaved changes. Are you sure you want to leave?"; });
    }
    warnUsersLeavingActiveForm();

    // Open certain links in new tabs
    $('a.viewsitelink, a.related-widget-wrapper-link').attr('target', '_blank');

    // Customise the default option text for select lists (set as an empty string)
    $('select option[value=""]').text('')

    // Limit options in select lists based on value of other input fields
    // Type > Document subtype
    $('#id_type').on('change', function(){
        // Show all subtype options
        $('#id_document_subtype').val('').find('option').hide();
        // If selecting Administrative type
        if ($(this).find('option:selected').text().startsWith('Administrative')) $('.field-document_subtype').show().find('#id_document_subtype option').filter(function(){return this.textContent.startsWith('Administrative')}).show();
        // If selecting Legal type
        else if ($(this).find('option:selected').text().startsWith('Legal')) $('.field-document_subtype').show().find('#id_document_subtype option').filter(function(){return this.textContent.startsWith('Legal')}).show();
        // If selecting none of the above
        else $('.field-document_subtype').hide();
    }).trigger('change');
});