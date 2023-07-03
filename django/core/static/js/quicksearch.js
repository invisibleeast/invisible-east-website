$(document).ready(function() {

    // Quick search
    // Searches a list of data on client, using data currently on page, with no server interaction
    // Pros: quick and simple
    // Cons: no support for pagination, basic search only
    // Not suitable for thorough searching with lots of items, etc. but useful for filtering small lists

    // Function to perform a quick search on a list
    function quickSearchList(searchTextInput, itemClass){
        var searchText = searchTextInput.val().toUpperCase();
        $(itemClass).each(function(){
            if($(this).text().toUpperCase().indexOf(searchText) != -1) $(this).show();
            else $(this).hide();
        });
    }

    // Apply above quickSearchList function to the various lists

    // Help list
    $("#help-list-head-search").on('keyup', function(){ quickSearchList($(this), ".help-list-items-item") });

});