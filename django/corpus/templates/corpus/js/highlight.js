
// Highlight certain text terms on the page
// E.g. used to highlight search term in the search results on the page


// Loop through elements and highlight search terms
function highlightTermsInElements(searchTerms, elementsToSearchIn){
    if (searchTerms.length > 0){
        elementsToSearchIn.forEach(function(element){
            $(element).each(function(){
                let content = $(this).text();
                let hasChange = false;
                // Loop through each search term
                searchTerms.forEach(function(term){
                    // Skip empty strings to prevent infinite loops or errors
                    if (term && term.trim() !== ""){
                        // Create a Regex: 
                        // 'g' = global (find all matches), 
                        // 'i' = case insensitive
                        // We escape special regex characters just in case user searches for '?' or '.'
                        const cleanTerm = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                        const regex = new RegExp(`(${cleanTerm})`, 'gi');
                        // Check if match exists before replacing to save processing
                        if (regex.test(content)){
                            // Replace match with wrapped version. 
                            // $1 preserves the original text's case (e.g. Bird vs bird)
                            content = content.replace(regex, '<strong class="highlight" title="You searched for `$1`">$1</strong>');
                            hasChange = true;
                        }
                    }
                });
                // Only update the DOM if a change was actually made
                if (hasChange) $(this).html(content);
            });
        });
    }
}


// On page load, get search terms from 'search' param in URL and highlight these on page once
let searchTermsFromURL = JSON.parse(new URLSearchParams(location.search).get('search') || '[]');
let elements = [
    // List page
    '.corpus-text-list-items-item-text-title',
    '.corpus-text-list-items-item-text-details dd',
    '.corpus-text-list-items-item-text-details-summary',
    // Detail page
    '.corpus-text-detail-content-details-datagroup-dataitem span',
    '.folio-lines-line-text',
]
highlightTermsInElements(searchTermsFromURL, elements);


// As user is searching within a highlightsearchterm input class, update highlighted text
$('input.highlightsearchterm').on('input', function(){
    $('.highlight').contents().unwrap();
    elements = [
        // Tags search page
        '.corpus-textfoliotag-list-tags-tag .name'
    ]
    let searchTerms = $('input.highlightsearchterm').map(function(){return $(this).val().trim();}).get();
    highlightTermsInElements(searchTerms, elements);
});
