//
// URL Parameters
//

function getUrlParameter(parameter) {
    return new URLSearchParams(window.location.search).get(parameter);
}

function setUrlParameter(parameter, value) {
    let urlParams = new URLSearchParams(window.location.search);
    urlParams.set(parameter, value);
    history.replaceState(null, null, "?" + urlParams.toString());
}


//
// Tabs
//

// Tabbed sections
$('#corpus-text-detail-content-tabs li').on('click', function(){
    // Show/hide the appropriate sections
    var activeTabId = $(this).attr('id');
    $('article.tabbed#corpus-text-detail-content-' + activeTabId).scrollTop(0).addClass('active');
    $('article.tabbed:not(#corpus-text-detail-content-' + activeTabId + ')').removeClass('active');
    // Alter active state of tab button
    $('#corpus-text-detail-content-tabs li').removeClass('active');
    $(this).addClass('active');
    // Set URL parameter
    setUrlParameter('tab', activeTabId);
    // Scroll to top
    window.scrollTo(0, 0);
    // Alter the 'only show' image parts select list when opening certain tabs
    let onlyShowSelect = $('#corpus-text-detail-images-controls-onlyshowcertainimageparts select');
    if (activeTabId === 'tags') onlyShowSelect.val('tags-all');
    // If going to any of the trans tabs, load transcription lines of text in the 'only show'
    else if (activeTabId === 'transcription') onlyShowSelect.val('lines-transcription');
    else if (activeTabId === 'translation') onlyShowSelect.val('lines-transcription');
    else if (activeTabId === 'transliteration') onlyShowSelect.val('lines-transcription');
    else onlyShowSelect.val('');
    onlyShowSelect.trigger('change');
})

// Get tab from url params and load tab (if no tab in URl then default to first tab)
function setTabFromUrl(){
    var tab_value = getUrlParameter('tab');
    var valid_tab_values = []
    $("#corpus-text-detail-content-tabs li").each(function(){ valid_tab_values.push($(this).attr('id')); })
    var tab = (!valid_tab_values.includes(tab_value) ? valid_tab_values[0] : tab_value);
    $('#corpus-text-detail-content-tabs li#' + tab).trigger('click');
}
setTabFromUrl();  // Set initial tab on page load

// On print show all tabs
$(window).bind("beforeprint", function(){
    $('article.tabbed').show();
});

// After print show just the active tab
$(window).bind("afterprint", function(){
    $('#corpus-text-detail-content-tabs li.active').trigger('click');
});


//
// Detail
//

// Hide a section if it's empty (otherwise the h3 section title will show but with no content)
$('.corpus-text-detail-content-details-datagroup').each(function(){
    if ($(this).find('div').length < 1) $(this).hide();
});


//
// Folios
//

// Load folio when clicking on it
$('.corpus-text-detail-content-folios-folio-imagecontainer').on('click', function(){
    let folioId = $(this).closest('.corpus-text-detail-content-folios-folio').attr('data-folio');
    $('#corpus-text-detail-images-controls-chooseimage select').val(folioId).trigger('change');
});

// Load folio in another tab
$('.corpus-text-detail-content-folios-folio-links div').on('click', function(){
    let folioId = $(this).closest('.corpus-text-detail-content-folios-folio').attr('data-folio');
    let tab = $(this).attr('data-tab');
    // Select this folio in the specified trans tab
    $(`#corpus-text-detail-content-tabs #${tab}`).trigger('click');
    $(`article#corpus-text-detail-content-${tab}`).find('.corpus-text-detail-folio-select').val(folioId).trigger('change');
});

// Select folio (this appears in other tabs, e.g. tags, transcription, etc)
$('.corpus-text-detail-folio-select').on('change', function(){
    let folioId = $(this).val();
    // Show only this folio in the tags tab
    $('.corpus-text-detail-content-tags-folio').hide();
    $(`.corpus-text-detail-content-tags-folio[data-folio="${folioId}"`).show();
    // Set this as the folio in the tag create form
    $('#corpus-text-detail-content-tags-textfoliotag-form input[name="textfolio"]').val(folioId);
    // Show only this folio across all trans tabs
    $('.folio-lines').hide();
    $(`.folio-lines[data-folio="${folioId}"]`).show();
    // Update all other folio select values to this value
    $('.corpus-text-detail-folio-select').val(folioId);
    // Show this folio in image
    let imageSelect = $('#corpus-text-detail-images-controls-chooseimage select');
    if (imageSelect.val() != folioId) imageSelect.val(folioId).trigger('change');
}).trigger('change');


//
// Tags
//

// Show/hide 'create a tag' form
$('#corpus-text-detail-content-tags-showtagcreate').on('change', function(){
    let tagCreate = $('#corpus-text-detail-content-tags-textfoliotag-form');
    if ($(this).is(':checked')) tagCreate.show();
    else tagCreate.hide();
}).trigger('change');

// Show/hide tags based on their category
$('#corpus-text-detail-content-tags-textfoliotag-form select[name="category"]').on('change', function(){
    let tagExistingSelect = $('#corpus-text-detail-content-tags-textfoliotag-form select[name="tag_existing"]');
    tagExistingSelect.val('').trigger('change');
    tagExistingSelect.find('option:not(:first)').hide();
    tagExistingSelect.find(`option[data-tagcategory="${$(this).val()}"]`).show();
}).trigger('change');

// Show/hide the new tag input if an existing tag is chosen
$('#corpus-text-detail-content-tags-textfoliotag-form select[name="tag_existing"]').on('change', function(){
    let tagNew = $('#corpus-text-detail-content-tags-textfoliotag-form input[name="tag_new"]');
    if ($(this).val() !== '') tagNew.val('').parent().hide();
    else tagNew.parent().show();
}).trigger('change');

// Show/hide the existing tag select if the new tag text field has content
$('#corpus-text-detail-content-tags-textfoliotag-form input[name="tag_new"]').on('input', function(){
    let tagExisting = $('#corpus-text-detail-content-tags-textfoliotag-form select[name="tag_existing"]');
    if ($(this).val() !== '') tagExisting.val('').parent().hide();
    else tagExisting.parent().show();
}).trigger('change');

// Clicking on a tag when linking text will create a link to that tag
$('.corpus-text-detail-content-tags-folio-tagcategory-tag').on('click', function(){
    if (linkTransTextToTagData){
        // Add this text folio tag ID to the data and submit form
        linkTransTextToTagData.textFolioTagExistingId = $(this).attr('data-textfoliotag');
        $('#corpus-text-detail-content-tags-textfoliotag-form input[name="linktranstexttotag"]').val(JSON.stringify(linkTransTextToTagData));
        $('#corpus-text-detail-content-tags-textfoliotag-form').submit();
    }
});

// Hovering over a tag will highlight it in the tag list and on the image
$('.corpus-text-detail-content-tags-folio-tagcategory-tag, .corpus-text-detail-images-image-parts-part').on('mouseover', function(){
    let tagId = $(this).attr('data-textfoliotag');
    $(`.corpus-text-detail-content-tags-folio-tagcategory-tag[data-textfoliotag="${tagId}"], .corpus-text-detail-images-image-parts-part[data-textfoliotag="${tagId}"]`).addClass('active');
}).on('mouseout', function(){
    let tagId = $(this).attr('data-textfoliotag');
    $(`.corpus-text-detail-content-tags-folio-tagcategory-tag[data-textfoliotag="${tagId}"], .corpus-text-detail-images-image-parts-part[data-textfoliotag="${tagId}"]`).removeClass('active');
});

// Link from tag in tags tab to tag in trans text
$('.corpus-text-detail-content-tags-folio-tagcategory-tag-links-link').on('click', function(){
    let trans = $(this).attr('data-trans');
    let textfoliotag = $(this).closest('.corpus-text-detail-content-tags-folio-tagcategory-tag').attr('data-textfoliotag');
    $(`#corpus-text-detail-content-tabs li#${trans}`).trigger('click');
    $(`article[data-trans="${trans}"]`).find('.corpus-text-detail-trans-linktranstexttotag-checkbox').prop('checked', false).trigger('change');
    $(`article[data-trans="${trans}"]`).find(`var[data-textfoliotag="${textfoliotag}"]`).addClass('active');
});


//
// Trans fields (i.e. transcription, translation, transliteration)
//

// Options: Show related trans
$('.corpus-text-detail-inline-trans-checkbox').on('change', function(){
    related_trans_lines = $(this).closest('article').find(`.related-lines[data-trans="${$(this).attr('data-trans')}"]`);
    if ($(this).is(':checked')) related_trans_lines.show();
    else related_trans_lines.hide();
}).each(function(){
    // Ensure all checkboxes are unchecked on page load
    $(this).prop('checked', false);
});

// Options: Show links to tags
$('.corpus-text-detail-trans-linktranstexttotag-checkbox').on('change', function(){
    links = $(this).closest('article').find(`var[data-textfoliotag]`);
    if ($(this).is(':checked')) links.addClass('active');
    else links.removeClass('active');
}).each(function(){
    // Ensure all checkboxes are unchecked on page load
    $(this).prop('checked', false);
});

// Add related trans lines to trans lines (e.g. add related translation and transliteration to the transcription lines)
var transFields = ['transcription', 'translation', 'transliteration'];
transFields.forEach(function(transField){
    $(`article[data-trans="${transField}"] .folio-lines-line`).each(function(i, trans){
        var transMainLineNumbers = $(trans).attr('data-linenumbers').split(',');
        var transFolio = $(trans).attr('data-folio');
        transFields.forEach(function(transFieldRelated){
            if (transField !== transFieldRelated){
                $(`article[data-trans="${transFieldRelated}"] .folio-lines-line[data-folio="${transFolio}"]`).each(function(i, transRelated){
                    var transRelatedLineNumbers = $(transRelated).attr('data-linenumbers').split(',');
                    if (transRelatedLineNumbers.some(transRelatedLineNumber => transMainLineNumbers.includes(transRelatedLineNumber))){
                        var relatedLineHtml = `<div class="related-lines-line">${$(transRelated).html()}</div>`;
                        $(trans).parent().find(`.related-lines[data-trans="${transFieldRelated}"]`).append(relatedLineHtml);
                    }
                });
            }
        });
    });
});

// Hovering over a line of trans text will highlight it in the trans text section and on the image
$('body').on('mouseover', '.folio-lines-line, .corpus-text-detail-images-image-parts-part', function(){
    // Add 'active' class if no others are currently active (can only have 1 at a time)
    if (!$('.folio-lines-line-draw-start.active').length){
        let folio = $(this).attr('data-folio');
        let lineIndex = $(this).attr('data-lineindex');
        let trans = $(this).attr('data-trans');
        $(`.folio-lines-line[data-folio="${folio}"][data-lineindex="${lineIndex}"][data-trans="${trans}"], .corpus-text-detail-images-image-parts-part[data-folio="${folio}"][data-lineindex="${lineIndex}"][data-trans="${trans}"]`).addClass('active');
    }
}).on('mouseout', '.folio-lines-line, .corpus-text-detail-images-image-parts-part', function(){
    // If the line isn't being drawn on image then remove the active class
    if (!$(this).find('.folio-lines-line-draw-start').is(':checked')){
        let folio = $(this).attr('data-folio');
        let lineIndex = $(this).attr('data-lineindex');
        let trans = $(this).attr('data-trans');
        $(`.folio-lines-line[data-folio="${folio}"][data-lineindex="${lineIndex}"][data-trans="${trans}"], .corpus-text-detail-images-image-parts-part[data-folio="${folio}"][data-lineindex="${lineIndex}"][data-trans="${trans}"]`).removeClass('active');
    }
});

// When admin user highlights/selects text within the trans text
var linkTransTextToTagData;
$('.folio-lines').on('mouseup', function(){
    let selection = window.getSelection();
    let linkTransTextToTag = $(this).closest('article').find('.corpus-text-detail-trans-linktranstexttotag')

    // Only text within the same node can be tagged (e.g. can't span lines or have tags within tags)
    if (selection.type == 'Range' && selection.anchorNode === selection.focusNode){

        // Set the index start and end of selected text
        let textSelectedIndexStart = selection.anchorOffset;
        let textSelectedIndexEnd = selection.focusOffset;
        // If user selects text backwards then index end < index start, so ensure start always < end
        if (textSelectedIndexStart > textSelectedIndexEnd){
            [textSelectedIndexStart, textSelectedIndexEnd] = [textSelectedIndexEnd, textSelectedIndexStart]
        }

        // Set the text
        let textWholeLine = selection.anchorNode.textContent;
        let textSelected = textWholeLine.substring(textSelectedIndexStart, textSelectedIndexEnd);

        // Get count of this instance of the textSelected in the TextWholeLine
        // Essential if textSelected repeats multiple times in a TextWholeLine, to know which instance to handle
        // E.g. if line is "the apple is smaller than the tree" if user highlighted "the", to which "the" are they referring?
        let textSelectedInstanceCountInLine = (textWholeLine.substring(0, textSelectedIndexStart).match(new RegExp(textSelected, 'g')) || []).length;

        // Build object with the above data from the selection object
        // Used elsewhere in JS and to be passed to back-end
        linkTransTextToTagData = {
            'textSelectedIndexStart': textSelectedIndexStart,
            'textSelectedIndexEnd': textSelectedIndexEnd,
            'textWholeLine': textWholeLine,
            'textSelected': textSelected,
            'textSelectedInstanceCountInLine': textSelectedInstanceCountInLine,
            'textTrans': $(this).closest('article').attr('data-trans'),
            'textTransLineIndex': selection.anchorNode.parentElement.parentElement.attributes["data-lineindex"].nodeValue
        }

        // Show the linktranstexttotag button
        linkTransTextToTag.show();
    }
    // 
    else {
        linkTransTextToTagData = undefined;
        linkTransTextToTag.hide();
    }

});

// Take user to choose a tag (new or existing) to link the selected text to
$('.corpus-text-detail-trans-linktranstexttotag').on('click', function(){
    if (linkTransTextToTagData){
        // Go to the 'tags' tab
        $('#corpus-text-detail-content-tabs li#tags').trigger('click');
        // Show the create a tag and pass the data to its hidden field
        $('#corpus-text-detail-content-tags-showtagcreate').prop('checked', true).trigger('change');
        $('#corpus-text-detail-content-tags-textfoliotag-form input[name="linktranstexttotag"]').val(JSON.stringify(linkTransTextToTagData));
        // Populate content of the 'linking text to tag' box and show it
        $('#corpus-text-detail-content-tags-textfoliotag-linktranstexttotag').html(`
            <p>
                Link a Tag to the ${$(this).attr('data-trans')} text: <strong>&ldquo;${linkTransTextToTagData.textSelected}&rdquo;</strong> from the line <strong>&ldquo;${linkTransTextToTagData.textWholeLine}&rdquo;</strong>
            </p>
            <p>
                To link a NEW tag, complete the 'Create a Tag' form and click Save.
            </p>
            <p>
                To link an EXISTING tag, simply click on the tag in the list below.
            </p>
        `).show();
    }
});

// Link from tag in trans text to tag in tags tab
$('var[data-textfoliotag]').on('click', function(){
    if ($(this).hasClass('active')){
        let textfoliotag = $(this).attr('data-textfoliotag');
        $('#corpus-text-detail-content-tabs li#tags').trigger('click');
        $(`.corpus-text-detail-content-tags-folio-tagcategory-tag[data-textfoliotag="${textfoliotag}"]`).trigger('mouseover');
    }
});

// Show tag in image
$('var[data-textfoliotag]').on('mouseover', function(){
    let tagId = $(this).attr('data-textfoliotag')
    $(`.corpus-text-detail-images-image-parts-part[data-textfoliotag="${tagId}"]`).addClass('active');
}).on('mouseout', function(){
    let tagId = $(this).attr('data-textfoliotag')
    $(`.corpus-text-detail-images-image-parts-part[data-textfoliotag="${tagId}"]`).removeClass('active');
});


//
// Images
//

// Rotation (used below for rotating the Text Folio image)
// Degrees by which Text Folio images can be rotated
const ROTATIONS = [0, 90, 180, 270];

// Reset the rotation (i.e. remove all rotation classes) of the specified DOM object
function rotationReset(objectToRotate){
    for (rotationIndex in ROTATIONS){
        rotationClass = `rotate-${ROTATIONS[rotationIndex]}`;
        objectToRotate.removeClass(rotationClass);
    }
}

// Set the rotation (i.e. add the correct rotation class) of the specified DOM object
function rotationSet(objectToRotate, clockwise=false){
    for (let rotationIndex in ROTATIONS){
        let rotationClass = `rotate-${ROTATIONS[rotationIndex]}`;

        // Choose next rotation (clockwise vs anticlockwise
        let newRotationIndex = 0;
        // Clockwise
        if (clockwise){
            // Loop back to start if reached end
            newRotationIndex = (parseInt(rotationIndex) + 1 < ROTATIONS.length ? parseInt(rotationIndex) + 1 : 0);
        }
        // Anticlockwise
        else {
            // Loop back to end if reached start
            newRotationIndex = (parseInt(rotationIndex) > 0 ? parseInt(rotationIndex) - 1 : ROTATIONS.length - 1);
        }
        let newRotationClass = `rotate-${ROTATIONS[newRotationIndex]}`;

        // Apply new rotation
        if (objectToRotate.hasClass(rotationClass)){
            objectToRotate.removeClass(rotationClass).addClass(newRotationClass);
            break;
        }
        // If reached end of loop and hasn't found rotation, then apply default rotation (e.g. 90 clockwise, 270 anticlockwise)
        else if (parseInt(rotationIndex) + 1 === ROTATIONS.length){
            // Clockwise default (2nd rotation, e.g. 90)
            if (clockwise) objectToRotate.addClass(`rotate-${ROTATIONS[1]}`);
            // Anticlockwise default (last rotation, e.g. 270)
            else objectToRotate.addClass(`rotate-${ROTATIONS[ROTATIONS.length - 1]}`);
        }
    }
}

// Panzoom
var panzoom;
var panzoomParent;
var panzoomElement;
var panzoomImageId;
var panzoomOptions = {
    cursor: 'move',
    maxScale: 13,
    minScale: 0.13,
    disablePan: false,
    disableZoom: false,
    step: 0.13,
    handleStartEvent: function(e) {
        // The following 2 lines were default but stopped drawing new parts from working
        // e.preventDefault();
        // e.stopPropagation();
    }
};

// Calculate the start scale (e.g. so image width matches container width by default)
function setPanzoomStartScale(){
    var image = $('#corpus-text-detail-images-image-' + panzoomImageId).find('img');
    var imageContainer = $('#corpus-text-detail-images-container');
    // If image is taller than it is wide, set start scale by height to fill vertical space
    if (image.height() > image.width()) var startScale = (imageContainer.height() / image.height());
    // If image is wider than it is tall (or square), set start scale by height to fill vertical space
    else var startScale = (imageContainer.width() / image.width());
    panzoomOptions.startScale = startScale;
    // Reset the rotation
    rotationReset($('#corpus-text-detail-images-image-' + panzoomImageId + ' .corpus-text-detail-images-image-rotatelayer'));
}

// Activate Panzoom on the current panzoomImageId image
function setPanzoomOnImage(){
    if (panzoom !== undefined) panzoom.destroy();
    panzoomElement = document.getElementById('corpus-text-detail-images-image-' + panzoomImageId);
    if ($(`#corpus-text-detail-images-image-${panzoomImageId}`).find('img').attr('src')){
        panzoom = Panzoom(panzoomElement, panzoomOptions);
        panzoomParent = panzoomElement.parentElement
        panzoomParent.addEventListener('wheel', panzoom.zoomWithWheel);
    }
}

// Text Folio Image Controls

// jQuery UI - set tooltips (the popup labels) for the image control to the bottom
$('#corpus-text-detail-images-controls div').attr('data-placement', 'bottom').tooltip();

// Choose image select list (set default value, change event, trigger on load)
$('#corpus-text-detail-images-controls-chooseimage select').on('change', function(){
    var imageId = $(this).find(":selected").val();
    panzoomImageId = imageId;
    // Remove 'active' from existing image
    $('.corpus-text-detail-images-image.active').removeClass('active');
    // Mark this image as 'active'
    $('#corpus-text-detail-images-image-' + imageId).addClass('active');
    // Update folio select lists in trans tabs
    $('.corpus-text-detail-folio-select').val(imageId).trigger('change');
    // Set the 'Download image' link location
    var imageUrl = $('#corpus-text-detail-images-image-' + imageId).find('img').attr('src');
    $('#corpus-text-detail-images-controls-downloadimage a').attr('href', imageUrl);
    // Set Panzoom
    setPanzoomStartScale();
    setPanzoomOnImage();
}).trigger('change');  // Show the first image by default on page load

// Only Show Certain Image Parts
$('#corpus-text-detail-images-controls-onlyshowcertainimageparts select').on('change', function(){
    let allParts = '.corpus-text-detail-images-image-parts-part';
    let onlyShow = $(this).val();
    let onlyShowGroup = onlyShow.split('-')[0]
    let onlyShowOption = onlyShow.split('-')[1]

    // Start by hiding all parts, then show only the chosen parts below
    $(allParts).addClass('hidden');

    // Show:
    // Default (no option selected)
    if (onlyShow === '') $(allParts).removeClass('hidden');
    // Lines
    else if (onlyShowGroup === 'lines'){
        if (onlyShow.endsWith('-all')) $(`${allParts}[data-trans]`).removeClass('hidden');
        else $(`${allParts}[data-trans="${onlyShowOption}"]`).removeClass('hidden');
    }
    // Tags
    else if (onlyShowGroup === 'tags'){
        if (onlyShow === 'tags-all') $(`${allParts}[data-textfoliotag]`).removeClass('hidden');
        else $(`${allParts}[data-category="${onlyShowOption}"]`).removeClass('hidden');
    }
});

// Images can cause load delay (especially on live server),
// meaning Panzoom settings have been added before it's loaded
// and images appeared much wider than expected.
// The following block applies Panzoom again once images are all loaded,
// to ensure they're presented correctly
$(window).on("load", function(){
    setPanzoomStartScale();
    setPanzoomOnImage();
});

// Show all parts
$('#corpus-text-detail-images-controls-revealparts').on('click', function(){
    $('.corpus-text-detail-images-image-parts-part').toggleClass('reveal');
});

// Reset image viewer to default
$('#corpus-text-detail-images-controls-reset').on('click', function(){
    setPanzoomStartScale();
    panzoom.reset();
});

// Rotate image (anticlockwise)
$('#corpus-text-detail-images-controls-rotate-anticlockwise').on('click', function(){
    rotationSet(
        objectToRotate=$('#corpus-text-detail-images-image-' + panzoomImageId + ' .corpus-text-detail-images-image-rotatelayer'),
        clockwise=false
    );
});

// Rotate image (clockwise)
$('#corpus-text-detail-images-controls-rotate-clockwise').on('click', function(){
    rotationSet(
        objectToRotate=$('#corpus-text-detail-images-image-' + panzoomImageId + ' .corpus-text-detail-images-image-rotatelayer'),
        clockwise=true
    );
});

// Text Folio Image Part controls (e.g. add, delete)

var canDrawNewTextFolioImagePart = false;
var isDrawingNewTextFolioImagePart = false;  // User is in the process of drawing (mousedown starts, mouseup ends)
var newTextFolioImagePartPosition;  // Top, left, width, height values of the new part

// Can start drawing rectangle
$('#corpus-text-detail-content-tags-textfoliotag-form-draw-start, .folio-lines-line-draw-start').on('change', function(){
    // Remove any new parts that may have been drawn
    $('.corpus-text-detail-images-image-parts-part.new').remove();
    // If can draw state is active, deactivate it
    if(!$(this).is(':checked')){
        $(this).removeClass('active');
        canDrawNewTextFolioImagePart = false;
        $('.corpus-text-detail-images-image').removeClass('drawable');
        // Change panzoom options
        panzoomOptions.disablePan = false;
        panzoomOptions.cursor = 'move';
        panzoom.setOptions(panzoomOptions);
        // Enable rotation
        $('#detail-images-controls-rotate-clockwise, #detail-images-controls-rotate-anticlockwise').show();
    }
    // If can draw state is deactive, activate it
    else {
        $(this).addClass('active');
        canDrawNewTextFolioImagePart = true;
        $('.corpus-text-detail-images-image').addClass('drawable');
        // Change panzoom options
        panzoomOptions.disablePan = true;
        panzoomOptions.cursor = 'crosshair';
        panzoom.setOptions(panzoomOptions);
        // Ensure no other of this class are still selected
        $('.folio-lines-line-draw-start').not(this).prop('checked', false).trigger('mouseout');
        // Reset rotation and disable rotation
        rotationReset($('#detail-images-image-' + panzoomImageId + ' .corpus-text-detail-images-image-rotatelayer'));
        $('#detail-images-controls-rotate, #detail-images-controls-rotate-anticlockwise').hide();
    }
});

// Start drawing rectangle
$('.corpus-text-detail-images-image').on('mousedown', function(e){
    // Only allow to draw a rectangle if a current annotation isn't already happening
    if(canDrawNewTextFolioImagePart){
        // Remove existing new parts, if any exist
        $('.corpus-text-detail-images-image-parts-part.new').remove();
        // Reset position values
        newTextFolioImagePartPosition = {left: 0, top: 0, width: 0, height: 0}
        // Set new position values
        newTextFolioImagePartPosition.left = (e.pageX - $(this).offset().left) / panzoom.getScale();
        newTextFolioImagePartPosition.top = (e.pageY - $(this).offset().top) / panzoom.getScale();
        // Create and append the new rectangle
        let newTextFolioImagePartHtml = `<div class="corpus-text-detail-images-image-parts-part new" style="height: 2px; width: 2px; left: ` + newTextFolioImagePartPosition.left + `px; top: ` + newTextFolioImagePartPosition.top + `px;"></div>`;
        $(this).find('.corpus-text-detail-images-image-parts').first().append(newTextFolioImagePartHtml);
        // Activate drawing boolean
        isDrawingNewTextFolioImagePart = true;
    }
});

// Drawing size of rectangle
$('.corpus-text-detail-images-image').on('mousemove', function(e){
    if (isDrawingNewTextFolioImagePart){
        newTextFolioImagePartPosition.width = ((e.pageX - $(this).offset().left) / panzoom.getScale()) - newTextFolioImagePartPosition.left;
        newTextFolioImagePartPosition.height = ((e.pageY - $(this).offset().top) / panzoom.getScale()) - newTextFolioImagePartPosition.top;
        $('.corpus-text-detail-images-image-parts-part.new').first().css({'height': newTextFolioImagePartPosition.height + 'px', 'width': newTextFolioImagePartPosition.width + 'px'})
    }
});

// Finish drawing rectangle
$('.corpus-text-detail-images-image').on('mouseup', function(){
    if (isDrawingNewTextFolioImagePart){
        isDrawingNewTextFolioImagePart = false;

        // drawlineonimage form
        if ($('.folio-lines-line-draw-start.active').length){
            let form = $('article.tabbed.active .corpus-text-detail-trans-drawlineonimage-form');
            // Set text folio
            let textFolio = $('#corpus-text-detail-images-controls-chooseimage select').val();
            form.find('input[name="textfolio"]').val(textFolio);
            // Set line index
            let line_index = $('.folio-lines-line.active').attr('data-lineindex');
            form.find('input[name="line_index"]').val(line_index);
            // Set image part position data
            form.find('input[name="image_part_left"]').val(newTextFolioImagePartPosition.left);
            form.find('input[name="image_part_top"]').val(newTextFolioImagePartPosition.top);
            form.find('input[name="image_part_width"]').val(newTextFolioImagePartPosition.width);
            form.find('input[name="image_part_height"]').val(newTextFolioImagePartPosition.height);
            // Submit the form
            form.submit();
        }

        // textfoliotag form
        else if ($('#corpus-text-detail-content-tags-textfoliotag-form-draw-start').is(':checked')){
            // Set image part position data
            $('#corpus-text-detail-content-tags-textfoliotag-form input[name="image_part_left"]').val(newTextFolioImagePartPosition.left);
            $('#corpus-text-detail-content-tags-textfoliotag-form input[name="image_part_top"]').val(newTextFolioImagePartPosition.top);
            $('#corpus-text-detail-content-tags-textfoliotag-form input[name="image_part_width"]').val(newTextFolioImagePartPosition.width);
            $('#corpus-text-detail-content-tags-textfoliotag-form input[name="image_part_height"]').val(newTextFolioImagePartPosition.height);
        }
    }
});

// Stop the Text Folio image img object from dragging/selecting when trying to draw a rectangle
$('.corpus-text-detail-images-image').bind('dragstart', function(){ return false; });

// Draw the Text Folio lines of text image parts
$('.folio-lines-line').each(function(){
    // Attempt to get attribute values
    let folio = $(this).attr('data-folio');
    let lineIndex = $(this).attr('data-lineindex');
    let lineNumbers = $(this).attr('data-linenumbers');
    let trans = $(this).attr('data-trans');
    let imagePartLeft = $(this).attr('data-imagepartleft');
    let imagePartTop = $(this).attr('data-imageparttop');
    let imagePartWidth = $(this).attr('data-imagepartwidth');
    let imagePartHeight = $(this).attr('data-imagepartheight');

    // If all required data attributes provided
    if (imagePartLeft && imagePartTop && imagePartWidth && imagePartHeight){
        $(`#corpus-text-detail-images-image-${folio} .corpus-text-detail-images-image-parts`).append(
            `<div class="corpus-text-detail-images-image-parts-part" data-folio="${folio}" data-lineindex="${lineIndex}" data-trans="${trans}" style="left: ${imagePartLeft}px; top: ${imagePartTop}px; width: ${imagePartWidth}px; height: ${imagePartHeight}px;"><label>Line ${lineNumbers}</label></div>`
        );
    }
});

// Click on an image part to show the relevant data
$('body').on('click', '.corpus-text-detail-images-image-parts-part.active', function(){
    // Determine tab to go to
    let tab;
    if ($(this).attr('data-trans')) tab = 'transcription'
    else if ($(this).attr('data-textfoliotag')) tab = 'tags'
    // Go to tab
    if (tab) $(`#corpus-text-detail-content-tabs li#${tab}:not(.active)`).trigger('click');
})
