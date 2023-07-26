from django import template


register = template.Library()


@register.simple_tag()
def pagination_showing_per_page(per_page, current_page, count_total_pages, count_total_items, items_name):
    """
    This template tag calculates the list item counts per page and returns as a human readable string
    E.g. 'Showing 1-100 items per page'
    """
    # Calculate the start figure
    start = ((current_page - 1) * per_page) + 1
    # Calculate the end figure
    end = per_page * current_page
    end = end if count_total_items > end else count_total_items
    # Return the data as a human readable sentence
    return f'Showing {start} - {end} {items_name} (Page {current_page} of {count_total_pages})'
