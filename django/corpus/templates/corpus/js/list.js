// Language code (English or Persian)
var languageCode = (window.location.href.includes('/fa/') ? 'fa' : 'en');

// Tooltips
$('label[title], .corpus-text-list-options-search-type-button').attr('data-placement', 'bottom').tooltip();

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

$('#corpus-text-list-options-filters .info-alert').on('click', function(){
    let attrName = (languageCode == 'fa' ? 'data-alert-fa' : 'data-alert');
    alert($(this).attr(attrName));
});

// Reset form
$('.reset-form').on('click', function(e){
    e.preventDefault();
    // Go to the current URL but without any parameters (remove everything after ? in url)
    window.location.replace(window.location.href.split('?')[0]);
});

// Reset individual filter
$('#corpus-text-list-options .input-clear').on('click', function(){
    $(this).prev('.corpus-text-list-options-filters-filter').val('').trigger('change');
});

// Show reset individual filter button
function showFilterResetButton(filter){
    let clearButton = filter.next('.input-clear');
    if (filter.val() !== '') clearButton.show();
    else clearButton.hide();
}

// Set search type (i.e. general or regex)
$('.corpus-text-list-options-search-type-button').on('click', function(){
    // Active status
    $('.corpus-text-list-options-search-type-button').removeClass('active');
    $(this).addClass('active');
    // Form value
    let searchType = $(this).attr('data-type');
    $('#corpus-text-list-options-search-type').val(searchType);
    // Set placeholder text of search boxes
    let placeholder = (languageCode == 'en' ? 'Search all fields by keyword' : 'جستجوی تمامی داد‌ه‌ها با استفاده از کلیدواژه');
    if (searchType === 'regex') placeholder = 'Search all fields with RegEx'
    $('.corpus-text-list-options-search-fields-instance input').first().attr('placeholder', placeholder);
});

// Add a search box
function addSearchBox(){
    let isFirstInstance = Boolean($('.corpus-text-list-options-search-fields-instance').length == 0);
    // Set HTML, but only include operator and remove buttons if this isn't the first instance
    let searchInputHtml = `<div class="corpus-text-list-options-search-fields-instance">` + (!isFirstInstance ? `<div class="corpus-text-list-options-search-fields-instance-operator" title="Toggle or/and">` + multipleSearchesOperator + `</div>` : ``) + `<input type="text" title="search">` + (!isFirstInstance ? `<span title="Remove this search box" class="corpus-text-list-options-search-fields-instance-remove"><i class="fas fa-minus"></i></span>` : `<button id="corpus-text-list-options-submit" class="corpus-text-list-options-submitbuttons-primary" title="Search"><i class="fas fa-search"></i></button>`) + `</div>`;
    // Append HTML
    $('#corpus-text-list-options-search-fields').append(searchInputHtml);
}

// Add initial search box on page load
addSearchBox();

// Add search box when clicking button
$('body').on('click', '#corpus-text-list-options-search-addinstance', function(){
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

// Use Page Selector to go to specific page
$('#corpus-text-list-pagination-current-pageselector').on('change', function(){
    let newPage = $(this).val();
    let maxPage = $(this).attr('max');
    if (newPage > maxPage) newPage = maxPage;
    let url = new URL(window.location.href);
    url.searchParams.set('page', newPage);
    window.location.href = url.toString();
});

// Toggle visibility of section content when clicking on section title
$('.corpus-text-list-options-section-title').on('click', function(){
    $(this).next().toggle();
});

// Submit form (after performing certain functions)
$('#corpus-text-list-options-submit').on('click', function(e){
    e.preventDefault();  // Stop form from submitting before below steps occur

    // Set the multiple searches operator (and / or)
    $('#corpus-text-list-options-search-operator').val(multipleSearchesOperator);

    // Enable disabled values
    $('#corpus-text-list-options-filters select:disabled').prop('disabled', false);

    // Set the hidden sort value
    $('#corpus-text-list-options-sort').val($('#corpus-text-list-header-sort-select').val())    

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
$('.corpus-text-list-options-filters-filter, .corpus-text-list-options-includes-filter, #corpus-text-list-header-sort-select').on('change', function(){
    $('#corpus-text-list-options-submit').trigger('click');
});

// If hitting the enter key on an input (e.g. a search box) then trigger above function before submitting
$('body').on('keydown', 'form#corpus-text-list-options input', function(e){
    if (e.keyCode == 13) $('#corpus-text-list-options-submit').trigger('click');
});

//
// Set form field values on page load from URL parameters
//

function setFieldValueFromUrl(formItemID, urlParameter, triggerChange=false){
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
        $('.corpus-text-list-options-search-fields-instance input').last().val(searchVal).attr('data-value', searchVal);
    });
}
// Sort
setFieldValueFromUrl('corpus-text-list-header-sort-select', 'sort');
// Filters
new URL(window.location.href).searchParams.forEach(function(value, key){
    // If key starts with the 'filter_pre' (as defined in Django view get_context_data() method) then it's a filter
    if (key.startsWith('{{ filter_pre }}')) setFieldValueFromUrl(key, key);
});
// Search Type (i.e. regex or not)
if (new URL(window.location.href).searchParams.get('search_type') == 'regex'){
    $('#corpus-text-list-options-search-type-regex').trigger('click');
} else {
    $('#corpus-text-list-options-search-type-general').trigger('click');
}


//
// Tags
//

$('.corpus-text-list-items-item-text-tags-tag').on('click', function(e){
    e.preventDefault();  // Prevent the link to the Text from working
    let tagId = $(this).attr('data-tagid');
    $('#filter_fk_text_folios__text_folio_tags__tag').val(tagId).trigger('change');
});

$('.corpus-text-list-items-item-text-tags').each(function(){
    let tags = $(this).find('.corpus-text-list-items-item-text-tags-tag');
    let maxTags = 4;
    tags.slice(maxTags).addClass(`corpus-text-list-items-item-text-tags-extra`);
    if(tags.length > maxTags) $(this).append(`<span class="corpus-text-list-items-item-text-tags-extrashow">+${tags.length - maxTags}</span>`);
});

$('.corpus-text-list-items-item-text-tags-extrashow').on('click', function(e){
    e.preventDefault();  // Prevent the link to the Text from working
    $(this).parent().find('.corpus-text-list-items-item-text-tags-extra').removeClass('corpus-text-list-items-item-text-tags-extra');
    $(this).remove();
});




//
// Set search criteria details if no results found
//

function htmlSearchCriteriaItem(inputId, inputType, label, value){
    return `<div class="corpus-text-list-searchcriteria-content-item" data-input-id="${inputId}" data-input-type="${inputType}" data-input-value="${value}" title="Remove this search criteria"><i class="fas fa-times-circle"></i><strong>${label}:</strong> ${value} </div>`;
}

function htmlSearchCriteria(){
    let html = ""
    new URL(window.location.href).searchParams.forEach(function(value, key){
        if (key.startsWith('{{ filter_pre }}') && value.length){
            let input = $(`#${key}`);
            let label = input.attr('title');
            // Input type
            var inputType;
            if (input.is('input') && input.attr('type') == 'checkbox') inputType = 'checkbox';
            else if (input.is('input') && input.attr('type') == 'hidden') inputType = 'hidden';
            else if (input.is('select')) inputType = 'select';
            // Value to display
            var valueDisplay;
            if (inputType == 'hidden'){
                if (key === "filter_fk_text_folios__text_folio_tags__tag") valueDisplay = '{{ filter_active_tag }}'
            }
            else if (inputType == 'checkbox') valueDisplay = 'Yes';
            else if (inputType == 'select') valueDisplay = $(`#${key} option:selected`).text();
            // Append item
            html += htmlSearchCriteriaItem(key, inputType, label, valueDisplay);
        }
        else if (key == 'search'){
            JSON.parse(value).forEach(function(searchVal, index){
                html += htmlSearchCriteriaItem(key, 'search', 'Search', searchVal);
            });
        }
    });
    $('#corpus-text-list-searchcriteria-content').html(html)
}

htmlSearchCriteria();

$('body').on('click', '.corpus-text-list-searchcriteria-content-item', function(){
    let inputId = $(this).attr('data-input-id');
    let inputType = $(this).attr('data-input-type');
    let inputText = $(this).attr('data-input-value');
    if (inputType == 'checkbox') $(`#${inputId}`).prop('checked', false).trigger('change');
    else if (inputType == 'select' || inputType == 'hidden') $(`#${inputId}`).val('').trigger('change');
    else if (inputType == 'search'){
        $(`.corpus-text-list-options-search-fields-instance input[data-value="${inputText}"]`).val('');
        $('#corpus-text-list-options-submit').trigger('click');
    }
});


//
// Must occur at end of script
//

// Show/hide all individual filter reset buttons on page load
$('.corpus-text-list-options-filters-filter').each(function(){
    showFilterResetButton($(this));
});
