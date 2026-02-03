
// Highlight certain text on the page
// E.g. used to highlight search term in the search results on the page


// 1. Get the list of search strings from URL params
const searchTerms = JSON.parse(new URLSearchParams(location.search).get('search') || '[]');

// 2. Define the elements you want to search within
const elements = [
    // List page
    '.corpus-text-list-items-item-text-title',
    '.corpus-text-list-items-item-text-details dd',
    '.corpus-text-list-items-item-text-details-summary',
    // Detail page
    '.corpus-text-detail-content-details-datagroup-dataitem span',
    '.folio-lines-line-text',
]

// 3. Loop through elements and highlight terms
if (searchTerms.length > 0){
    elements.forEach(function(element){
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
