// Click mobile toggle button on corpus-text-list-options 
$('#corpus-text-list-options-toggler').on('click', function(){
    // Hide
    if ($(this).hasClass('active')){
        $('.corpus-text-list-options, .corpus-text-list-options-submitbuttons').animate({'right': '-23em'}, 270, function(){$(this).hide();});
        $(this).removeClass('active');
        // Icon
        $(this).find('#corpus-text-list-options-toggler-inactive').show();
        $(this).find('#corpus-text-list-options-toggler-active').hide();
    }
    // Show
    else {
        $('.corpus-text-list-options, .corpus-text-list-options-submitbuttons').show().animate({'right': '0'}, 270);
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

// Reset filters
$('#corpus-text-list-options .input-clear').on('click', function(){
    $(this).next('.corpus-text-list-options-filters-group-filter').val('').trigger('change');
});

// Show reset filter
$('.corpus-text-list-options-filters-group-filter').on('change', function(){
    let clearButton = $(this).prev('.input-clear');
    if ($(this).val() !== '') clearButton.show();
    else clearButton.hide();
});

// Add a search box
$('#corpus-text-list-options-search-fields-add').on('click', function(){
    let isFirstInstance = Boolean($('.corpus-text-list-options-search-fields-instance').length == 0);
    // Set HTML, but only include operator and remove buttons if this isn't the first instance
    let searchInputHtml = `<div class="corpus-text-list-options-search-fields-instance">` + (!isFirstInstance ? `<div class="corpus-text-list-options-search-fields-instance-operator" title="Click to toggle 'or'/'and'">` + multipleSearchesOperator + `</div>` : ``) + `<input type="text" title="search" placeholder="Search">` + (!isFirstInstance ? `<span title="Remove this search box"><i class="fas fa-minus"></i></span>` : ``) + `</div>`;
    // Append HTML
    $('#corpus-text-list-options-search-fields').append(searchInputHtml);
}).trigger('click');

// Remove a search box
$('#corpus-text-list-options').on('click', '.corpus-text-list-options-search-fields-instance span', function(){
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

    // Send multiple searches as a JSON encoded array of strings
    let searchArray = [];
    $('.corpus-text-list-options-search-fields-instance input').each(function(){
        if ($(this).val().length) searchArray.push($(this).val());
    })
    $('#corpus-text-list-options-search-values').val(JSON.stringify(searchArray));

    // Submit the list options form
    $('form#corpus-text-list-options').submit();

    // Show a loading indicator
    $('.corpus-text-list-options').html('<div class="spinner-container"><div class="spinner"></div><span>Searching...</span></div>')
    $('.corpus-text-list-options-submitbuttons button').prop('disabled', true);
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
    if (value) $('#' + formItemID).val(value);
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
        if (index > 0) $('#corpus-text-list-options-search-fields-add').trigger('click');
        // Set this search value in the most recent search box
        $('.corpus-text-list-options-search-fields-instance input').last().val(searchVal);
    });
}
// Sort
setFieldValueFromUrl('list-options-sort-by', 'sort_by');
setFieldValueFromUrl('list-options-sort-direction', 'sort_direction');
// Filters
new URL(window.location.href).searchParams.forEach(function(value, key){
    // If key starts with the 'filter_pre' (as defined in Django view get_context_data() method) then it's a filter
    if (key.startsWith('{{ filter_pre }}')) setFieldValueFromUrl(key, key);
});


//
// Filter dependency: show/hide one filter based on the value of another filter
// E.g. for 'Graphic Element Type' show the correct select list(s) for each type
//

$('select.corpus-text-list-options-filters-group-filter[data-dependencies]').on('change', function(){
    let dependencies = JSON.parse($(this).attr('data-dependencies'));
    let selected = $(this).find(':selected').text();

    dependencies.forEach(function(dependency){
        let dependency_select = $('#' + dependency.id);
        // Show filter if a valid option chosen and it's matching
        if (dependency.value === selected && selected !== '') dependency_select.parent().show();
        // Hide filter if not a match or no valid option chosen
        else {
            dependency_select.val('').parent().hide();
            dependency_select.prev('.input-clear').hide();
        }
    });
});


//
// Hierarchical data filters: selecting a particular value in one list changes available options in another based on related data
// E.g. Country > Town > Collection. When selecting a Country the options in Town and Collection should filter to only those from that country
//

// Children (when selecting an parent, limit options in the children)
$('select.corpus-text-list-options-filters-group-filter[data-hierarchy-children]').on('change', function(){
    let parentId = $(this).attr('data-hierarchy-id');
    let parentVal = $(this).val();
    let children = $(this).attr('data-hierarchy-children').split(' ');

    // Loop through child select lists
    children.forEach(function(child){
        let childSelect = 'select.corpus-text-list-options-filters-group-filter[data-hierarchy-id=' + child + ']';
        // Reset value of child, if not changing to default and the child option is hidden
        if (parentVal != '') $(childSelect).find(':selected:hidden').parent().val('');
        // Loop through child select lists' options
        $(childSelect + ' > option').each(function(){
            // Get parent data as a JSON object
            let parents = $(this).attr('data-hierarchy-parents-ids');
            // If parent & child data exists for this option
            if (parents && parentVal) {
                // Convert parents string to JSON object
                parents = JSON.parse(parents);
                // Show if this is a child (has a matching parent)
                if (parents[parentId] == parentVal) $(this).show();
                else $(this).hide();
            } else {
                $(this).show();  // Show by default
            }
        });
    });
});
// Parents (when selecting a child, hide the parent)
$('select.corpus-text-list-options-filters-group-filter[data-hierarchy-parents]').on('change', function(){
    let childVal = $(this).val();
    // Loop through parents
    $(this).attr('data-hierarchy-parents').split(' ').forEach(function(q){ 
        let parent = $('select.corpus-text-list-options-filters-group-filter[data-hierarchy-id=' + q + ']')
        let parentClearButton = parent.prev('.input-clear');
        // Disable parent if a child value provided, else enable parent
        if (childVal !== ''){
            parent.val('').attr('disabled', 'disabled');  // Select
            parent.closest('div').addClass('disabled');  // Container
            parentClearButton.hide();
        }
        else {
            parent.removeAttr('disabled').trigger('change');  // Select
            parent.closest('div').removeClass('disabled');  // Container
        }
    });
});

// Trigger change on all filters on page load
$('.corpus-text-list-options-filters-group-filter').trigger('change');