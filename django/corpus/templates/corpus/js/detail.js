//
// Tabs
//

// Tabbed sections
$('#corpus-text-detail-content-tabs li').on('click', function(){
    // Show/hide the appropriate sections
    var active_tab_id = $(this).attr('id');
    $('article.tabbed#corpus-text-detail-content-' + active_tab_id).show();
    $('article.tabbed:not(#corpus-text-detail-content-' + active_tab_id + ')').hide();
    // Alter active state of tab button
    $('#corpus-text-detail-content-tabs li').removeClass('active');
    $(this).addClass('active');
    // Scroll to top
    window.scrollTo(0, 0);
}).first().trigger('click');

// On print show all tabs
$(window).bind("beforeprint", function(){
    $('article.tabbed').show();
});

// On print show just the active tab
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

$('.corpus-text-detail-content-folios-folio-textlinks div').on('click', function(){
    let folioId = $(this).closest('.corpus-text-detail-content-folios-folio').attr('data-folio');
    let trans = $(this).attr('data-trans');
    // Select this folio in the specified trans tab
    $(`#corpus-text-detail-content-tabs #${trans}`).trigger('click');
    $(`article#corpus-text-detail-content-${trans}`).find('.corpus-text-detail-folio-select').val(folioId).trigger('change');
});


//
// Trans fields (i.e. transcription, translation, transliteration)
//

// Options: Select folio
$('.corpus-text-detail-folio-select').on('change', function(){
    let folioId = $(this).val();
    // Show only this folio across all trans tabs
    $('.folio-lines').hide();
    $(`.folio-lines[data-folio="${folioId}"]`).show();
    // Update all other folio select values to this value
    $('.corpus-text-detail-folio-select').val(folioId);
    // Show this folio in image
    let imageSelect = $('#corpus-text-detail-images-controls-chooseimage select');
    if (imageSelect.val() != folioId) imageSelect.val(folioId).trigger('change');
}).trigger('change');

// Options: Show translation
$('.corpus-text-detail-inline-trans-checkbox').on('change', function(){
    related_trans_lines = $(this).closest('article').find(`.related-lines[data-trans="${$(this).attr('data-trans')}"]`);
    if ($(this).is(':checked')) related_trans_lines.show();
    else related_trans_lines.hide();
}).each(function(){
    // Ensure all checkboxes are unchecked on page load
    $(this).prop('checked', false);
});

// Add related trans lines to trans lines (e.g. add related translation and transliteration to the transcription lines)
var transFields = ['transcription', 'translation', 'transliteration'];
transFields.forEach(function(transField){
    $(`.corpus-text-detail-content-${transField}-folio-lines-line`).each(function(i, trans){
        var transMainLineNumbers = $(trans).attr('data-linenumbers').split(',');
        var transFolio = $(trans).attr('data-folio');
        transFields.forEach(function(transFieldRelated){
            if (transField !== transFieldRelated){
                $(`.corpus-text-detail-content-${transFieldRelated}-folio-lines-line[data-folio="${transFolio}"]`).each(function(i, transRelated){
                    var transRelatedLineNumbers = $(transRelated).attr('data-linenumbers').split(',');
                    if (transRelatedLineNumbers.some(transRelatedLineNumber => transMainLineNumbers.includes(transRelatedLineNumber))){
                        var relatedLineHtml = `<div class="relatedline">${$(transRelated).html()}</div>`;
                        $(trans).parent().find(`.related-lines[data-trans="${transFieldRelated}"]`).append(relatedLineHtml);
                    }
                });
            }
        });
    });
});


//
// Images
//

// Rotation (used below for rotating the document image)
// Degrees by which document images can be rotated
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
        e.preventDefault();
        e.stopPropagation();
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

// Document Image Controls

// Choose image select list (set default value, change event, trigger on load)
$('#corpus-text-detail-images-controls-chooseimage select').on('change', function(){
    // Reset toggle for allowing to drawer new parts (if it's active)
    // if(canDrawNewDocumentImagePart) $('#transcription-exercise-controls-newdocumentimagepart').trigger('click');
    // Hide any existing dropdown content
    $('.transcription-exercise-controlsdropdown').hide();

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

// Images can cause load delay (especially on live server),
// meaning Panzoom settings have been added before it's loaded
// and images appeared much wider than expected.
// The following block applies Panzoom again once images are all loaded,
// to ensure they're presented correctly
$(window).on("load", function(){
    setPanzoomStartScale();
    setPanzoomOnImage();
});

// Reveal all parts
$('#corpus-text-detail-images-controls-revealallparts').on('click', function(){
    $('.corpus-text-detail-images-image-parts-part').toggleClass('revealall');
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