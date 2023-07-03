from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def pagination_go_to_page(context, page_number):
    """
    This template tag takes the page number of the desired page as an input
    and returns a new URL with all existing parameters (everything after ? in the full url)
    along with the new page number.

    It replaces the current page number param (if already exists)
    or appends a new page number param (if one is not yet set).
    """
    # All url parameters (everything after ? in the full url) as a list
    url_params = context['request'].GET.copy().urlencode().split('&')
    # Remove existing page and empty params, if exists
    for q in url_params:
        if 'page=' in q or q == '':
            url_params.remove(q)
    # Add the new page to start of query
    url_params.insert(0, f'page={page_number}')
    # Return new url
    return f"?{'&'.join(url_params)}"  # e.g. '?page=2&search=xxxx'
