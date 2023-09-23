// Click mobile toggle button on corpus-text-list-options 
$('#corpus-text-list-options-toggler').on('click', function(){
    // Hide
    if ($(this).hasClass('active')){
        $('#corpus-text-list-options').animate({'left': '-23em'}, 270, function(){$(this).hide();});
        $(this).removeClass('active');
        // Icon
        $(this).find('#corpus-text-list-options-toggler-inactive').show();
        $(this).find('#corpus-text-list-options-toggler-active').hide();
    }
    // Show
    else {
        $('#corpus-text-list-options').show().animate({'left': '0'}, 270);
        $(this).addClass('active');
        // Icon
        $(this).find('#corpus-text-list-options-toggler-inactive').hide();
        $(this).find('#corpus-text-list-options-toggler-active').show();
    }
});

// Reset form
$('.reset-form').on('click', function(e){
    e.preventDefault();
    // Go to the current URL but without any parameters (remove everything after ? in url)
    window.location.replace(window.location.href.split('?')[0]);
});

// Reset individual filter
$('#corpus-text-list-options .input-clear').on('click', function(){
    $(this).next('.corpus-text-list-options-filters-group-filter').val('').trigger('change');
});

// Show reset individual filter button
function showFilterResetButton(filter){
    let clearButton = filter.prev('.input-clear');
    if (filter.val() !== '') clearButton.show();
    else clearButton.hide();
}

// Add a search box
function addSearchBox(){
    let isFirstInstance = Boolean($('.corpus-text-list-options-search-fields-instance').length == 0);
    // Set HTML, but only include operator and remove buttons if this isn't the first instance
    let searchInputHtml = `<div class="corpus-text-list-options-search-fields-instance">` + (!isFirstInstance ? `<div class="corpus-text-list-options-search-fields-instance-operator" title="Click to toggle 'or'/'and'">` + multipleSearchesOperator + `</div>` : ``) + `<input type="text" title="search" placeholder="Search">` + (!isFirstInstance ? `<span title="Remove this search box" class="corpus-text-list-options-search-fields-instance-remove"><i class="fas fa-minus"></i></span>` : `<span id="corpus-text-list-options-search-fields-instance-add" title="Add search box"><i class="fas fa-plus"></i></span>`) + `</div>`;
    // Append HTML
    $('#corpus-text-list-options-search-fields').append(searchInputHtml);
}

// Add initial search box on page load
addSearchBox();

// Add search box when clicking button
$('body').on('click', '#corpus-text-list-options-search-fields-instance-add', function(){
    addSearchBox();
});

// Remove a search box
$('#corpus-text-list-options').on('click', '.corpus-text-list-options-search-fields-instance-remove', function(){
    $(this).parent().remove();
});

// Toggle search operator (or / and)
$('#corpus-text-list-options').on('click', '.corpus-text-list-options-search-fields-instance-operator', function(){
    // Swap between 
    if (multipleSearchesOperator === 'or') multipleSearchesOperator = 'and';
    else multipleSearchesOperator = 'or';
    // Set the text of each instance
    $('.corpus-text-list-options-search-fields-instance-operator').text(multipleSearchesOperator);
});

// Swap related greater than/less than values if not in order. So if gt > lt
// E.g. if Date (from) = 2nd Century and Date (to) = 1st Century, then swap
$('.{{ filter_pre_gt }}, .{{ filter_pre_lt }}').on('change', function(){

    // Find the gt element of this relationship
    // E.g. find 'Date (from)' in the relationship: 'Date (from)' -> 'Date (to)'
    let gt = $('#' + $(this).attr('id').replace('{{ filter_pre_lt }}', '{{ filter_pre_gt }}'));

    // Find matching 'less than' element
    // E.g. if this is 'Date (from)' find matching 'Date (to)'
    let lt = $('#' + $(this).attr('id').replace('{{ filter_pre_gt }}', '{{ filter_pre_lt }}'));

    // If a matching gt & lt pair found
    if (gt && lt){
        // Get their current values (as integers, for proper comparison)
        let gtVal = parseInt(gt.val());
        let ltVal = parseInt(lt.val());
        // If both have valid values and gt is more than lt, swap their values
        if (gtVal !== '' && ltVal !== '' && gtVal > ltVal){
            gt.val(ltVal);
            lt.val(gtVal);
        }
    }
});

// Submit form (after performing certain functions)
$('#corpus-text-list-options-submit').on('click', function(e){
    e.preventDefault();  // Stop form from submitting before below steps occur

    // Set the multiple searches operator (and / or)
    $('#corpus-text-list-options-search-operator').val(multipleSearchesOperator);

    // Remove the document subtype if it's not a child of the text type
    let textType = $('#filter_fk_type option:selected').text().split(' ')[0];
    let documentSubtypeCategory = $('#filter_fk_document_subtype option:selected').text().split(': ')[0];
    if (textType !== documentSubtypeCategory) $('#filter_fk_document_subtype').val('');

    // Send multiple searches as a JSON encoded array of strings
    let searchArray = [];
    $('.corpus-text-list-options-search-fields-instance input').each(function(){
        if ($(this).val().length) searchArray.push($(this).val());
    })
    $('#corpus-text-list-options-search-values').val(JSON.stringify(searchArray));

    // Submit the list options form
    $('form#corpus-text-list-options').submit();

    // Disable submit to prevent repeat clicks
    $(this).prop('disabled', true);
});

// Submit the form upon change of value of certain form elements
$('.corpus-text-list-options-filters-group-filter, #corpus-text-list-options-sort-by, #corpus-text-list-options-sort-direction').on('change', function(){
    $('#corpus-text-list-options-submit').trigger('click');
});

// If hitting the enter key on an input (e.g. a search box) then trigger above function before submitting
$('body').on('keydown', 'form#corpus-text-list-options input', function(e){
    if (e.keyCode == 13) $('#corpus-text-list-options-submit').trigger('click');
});


//
// Set form field values on page load from URL parameters
//

function setFieldValueFromUrl(formItemID, urlParameter, triggerChange=false) {
    var value = new URL(window.location.href).searchParams.get(urlParameter);
    // If a valid value found
    if (value){
        // Checkboxes (check the box)
        if (urlParameter.startsWith('{{ filter_pre_bl }}')) $('#' + formItemID).prop('checked', 'checked')
        // Select List (set correct option)
        else $('#' + formItemID).val(value);
    }
    if (triggerChange) $('#' + formItemID).trigger('change');
}
// Set Multiple Search Operator (or/and) from URL
var multipleSearchesOperator = new URL(window.location.href).searchParams.get('search_operator');
if (!multipleSearchesOperator) multipleSearchesOperator = 'or';  // Set to 'or' if not in URL
// Search - Includes multiple searches, so can't use setFieldValueFromUrl() function
urlSearchesStr = new URL(window.location.href).searchParams.get('search');
urlSearchesArray = JSON.parse(urlSearchesStr);
if (urlSearchesArray){
    urlSearchesArray.forEach(function(searchVal, index){
        // Create a new search box, if this isn't the first item (as there's already 1 by default)
        if (index > 0) addSearchBox();
        // Set this search value in the most recent search box
        $('.corpus-text-list-options-search-fields-instance input').last().val(searchVal);
    });
}
// Sort
setFieldValueFromUrl('corpus-text-list-options-sort-by', 'sort_by');
setFieldValueFromUrl('corpus-text-list-options-sort-direction', 'sort_direction');
// Filters
new URL(window.location.href).searchParams.forEach(function(value, key){
    // If key starts with the 'filter_pre' (as defined in Django view get_context_data() method) then it's a filter
    if (key.startsWith('{{ filter_pre }}')) setFieldValueFromUrl(key, key);
});


//
// Filter Relationships (i.e. changing visibility/options in one filter based on value of another filter)
//

// 'Type' and 'Document Subtype'
function filterRelationshipTypeAndDocumentSubtype(){
    let textType = $('#filter_fk_type').find('option:selected').text();
    let documentSubtype = $('#filter_fk_document_subtype');
    let documentSubtypeContainer = $('#filter_fk_document_subtype').closest('.corpus-text-list-options-filters-group-filter-container');
    // If selecting Administrative type
    if (textType.startsWith('Administrative')){
        documentSubtypeContainer.show();
        documentSubtype.find('option').each(function(){
            if ($(this).text().startsWith('Administrative')) $(this).removeClass('hidden');
            else $(this).addClass('hidden');
        });
    }
    // If selecting Legal type
    else if (textType.startsWith('Legal')){
        documentSubtypeContainer.show();
        documentSubtype.find('option').each(function(){
            if ($(this).text().startsWith('Legal')) $(this).removeClass('hidden');
            else $(this).addClass('hidden');
        });
    }
    // If selecting none of the above
    else {
        documentSubtypeContainer.hide();
        documentSubtype.val('');
    }
}

filterRelationshipTypeAndDocumentSubtype();


//
// Must occur at end of script
//

// Show/hide all individual filter reset buttons on page load
$('.corpus-text-list-options-filters-group-filter').each(function(){
    showFilterResetButton($(this));
});
