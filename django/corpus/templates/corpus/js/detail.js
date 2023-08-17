// Functions for simplifying interacting with URL parameters
function getUrlParameter(parameter) {
    return new URLSearchParams(window.location.search).get(parameter);
}
function setUrlParameter(parameter, value) {
    let urlParams = new URLSearchParams(window.location.search);
    urlParams.set(parameter, value);
    history.replaceState(null, null, "?" + urlParams.toString());
}

// Tabbed sections
$('#corpus-text-detail-content-tabs li').on('click', function(){
    // Show/hide the appropriate sections
    var active_tab_id = $(this).attr('id');
    $('article.tabbed#corpus-text-detail-content-' + active_tab_id).show();
    $('article.tabbed:not(#corpus-text-detail-content-' + active_tab_id + ')').hide();
    // Alter active state of tab button
    $('#corpus-text-detail-content-tabs li').removeClass('active');
    $(this).addClass('active');
    // Set URL parameter
    setUrlParameter('tab', active_tab_id);
    // Scroll to top
    window.scrollTo(0, 0);
});

// Get tab from url params and initiate above click event function
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

// On print show all tabs
$(window).bind("afterprint", function(){
    setTabFromUrl();
});






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
        // e.preventDefault();
        // e.stopPropagation();
    }
};
// Calculate the start scale (e.g. so image width matches container width by default)
function setPanzoomStartScale(){
    var imageWidth = $('#corpus-text-detail-images-image-' + panzoomImageId).find('img').width();
    var imageContainerWidth = $('#corpus-text-detail-images-container').width();
    var startScale = (imageContainerWidth / imageWidth);
    panzoomOptions.startScale = startScale;
    // Reset the rotation
    rotationReset($('#corpus-text-detail-images-image-' + panzoomImageId + ' .corpus-text-detail-images-image-rotatelayer'));
}
// Activate Panzoom on the current panzoomImageId image
function setPanzoomOnImage(){
    if (panzoom !== undefined) panzoom.destroy();
    panzoomElement = document.getElementById('corpus-text-detail-images-image-' + panzoomImageId);
    panzoom = Panzoom(panzoomElement, panzoomOptions);
    panzoomParent = panzoomElement.parentElement
    panzoomParent.addEventListener('wheel', panzoom.zoomWithWheel);
}

// Functions for simplifying interacting with URL parameters
function getUrlParameter(parameter) {
    return new URLSearchParams(window.location.search).get(parameter);
}
function setUrlParameter(parameter, value) {
    let urlParams = new URLSearchParams(window.location.search);
    urlParams.set(parameter, value);
    history.replaceState(null, null, "?" + urlParams.toString());
}

// Document Image Controls

// Choose image select list (set default value, change event, trigger on load)
$('#corpus-text-detail-images-controls-chooseimage select').val(
    getUrlParameter('image') ? getUrlParameter('image') : $('#corpus-text-detail-images-controls-chooseimage select').val()
).on('change', function(){
    // Go to the correct tab
    $('li#details').trigger('click');
    // Reset toggle for allowing to drawer new parts (if it's active)
    // if(canDrawNewDocumentImagePart) $('#transcription-exercise-controls-newdocumentimagepart').trigger('click');
    // Hide any existing dropdown content
    $('.transcription-exercise-controlsdropdown').hide();

    var imageId = $(this).find(":selected").val();
    panzoomImageId = imageId;
    // Update URL
    setUrlParameter('image', imageId);
    // Remove 'active' from existing image (and related content)
    $('.corpus-text-detail-images-image.active, .detail-controls-item.active, .transcription-exercise.active, .transcription-exercise-coreinfo-difficulty.active, .transcription-exercise-fullsolution-instance.active, .transcription-exercise-instructions-instruction.active, .newdocumentimagepart-form-addafterimagepartid.active, .newdocumentimagepart-form-newline.active, .deletedocumentimagepart-form-deleteimagepartid.active').removeClass('active');
    // Mark this image (and related content) as 'active'
    $('#corpus-text-detail-images-image-' + imageId + ', #transcription-exercise-' + imageId + ', #transcription-exercise-coreinfo-difficulty-' + imageId + ', #transcription-exercise-fullsolution-instance-' + imageId + ', #transcription-exercise-instructions-instruction-' + imageId + ', #newdocumentimagepart-form-addafterimagepartid-' + imageId + ', #newdocumentimagepart-form-newline-' + imageId + ', #deletedocumentimagepart-form-deleteimagepartid-' + imageId).addClass('active');
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