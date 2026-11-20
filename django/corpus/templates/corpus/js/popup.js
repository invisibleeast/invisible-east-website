// Open popup (and set default content)
$('.popuptrigger').on('click', function(){
    let popupId = $(this).data('id');
    $(`.popup[data-id="${popupId}"]`).show();
});

// Close popup (by clicking close button)
$('.popup-content-close').on('click', function(){
    $('.popup').hide();
});

// Close popup (by clicking background)
$('.popup').on('click', function(e){
    if (e.target === this){
        $(this).hide();
    }
});
