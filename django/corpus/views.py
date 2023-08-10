from django.views.generic import (DetailView, ListView)
from django.db.models.functions import Lower
from django.db.models import (Count, Q, CharField, TextField)
from functools import reduce
from operator import (or_, and_)
from . import models
import json


class TextDetailView(DetailView):
    """
    Class-based view for Text detail template
    """
    template_name = 'corpus/text-detail.html'
    model = models.Text

    def get_queryset(self):
        return self.model.objects.filter(public_review_approved=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['xxx'] = '...'

        return context



class TextListView(ListView):
    """
    Class-based view for Text list template
    """
    template_name = 'corpus/text-list.html'
    model = models.Text
    paginate_by = 30

    # Special starts to the values & labels of options in 'filter' select lists
    filter_pre = 'filter_'
    filter_pre_mm = f'{filter_pre}mm_'  # Many to Many relationship
    filter_pre_fk = f'{filter_pre}fk_'  # Foreign Key relationship
    filter_pre_gt = f'{filter_pre}gt_'  # Greater than (or equal to) filter, e.g. "Date (from)"
    filter_pre_lt = f'{filter_pre}lt_'  # Less than (or equal to) filter, e.g. "Date (to)"

    # Special starts to the values & labels of options in 'sort by' select lists, used in below sort() function and within views scripts
    sort_pre_count_value = 'count_'
    sort_pre_count_label = 'Number of '

    def get_field_type(self, field_name, queryset):
        """
        Return the type of a field
        E.g. used in sort() to see if case insensitivity is needed (if field is a CharField/TextField)
        """
        try:
            stripped_field_name = field_name.lstrip('-')
            if stripped_field_name in queryset.query.annotations:
                return queryset.query.annotations[stripped_field_name].output_field
            return queryset.model._meta.get_field(stripped_field_name)
        except Exception:
            return CharField  # If it fails, assume it's a CharField by default

    def get_queryset(self):
        # Start with all objects
        queryset = self.model.objects.filter(public_review_approved=True)

        # Improve performance
        queryset = queryset.select_related(
            'type',
            'collection'
        )

        # Search
        searches = json.loads(self.request.GET.get('search', '[]'))
        field_names_to_search = ['shelfmark', 'collection__name']
        # Set list of search options
        if searches not in [[''], []]:
            operator = or_ if self.request.GET.get('search_operator', '') == 'or' else and_
            queries = []
            for search in searches:
                # Uses 'or_' as the search term could appear in any field, so 'and_' wouldn't be suitable
                queries.append(reduce(or_, (Q((f'{field_name}__icontains', search)) for field_name in field_names_to_search)))
            # Connect the individual search queries via the user-defined operator (or_ / and_)
            queries = reduce(operator, queries)
            # Filter the queryset using the completed search query
            queryset = queryset.filter(queries)


        # # Filter
        # # Description
        # search_description = self.request.GET.get('search-description', None)
        # queryset = queryset.filter(description__icontains=search_description) if search_description else queryset
        # # Vill
        # search_vill = self.request.GET.get('search-vill', None)
        # queryset = queryset.filter(tenant__property_fk__vill__name__icontains=search_vill) if search_vill else queryset
        # # Shire
        # search_shire = self.request.GET.get('search-shire', None)
        # queryset = queryset.filter(tenant__property_fk__shire__icontains=search_shire) if search_shire else queryset

        # Sort
        # Establish the sort direction (asc/desc) and the field to sort by, from the self.request
        sort_dir = self.request.GET.get('sort_direction', '')
        sort_by = self.request.GET.get('sort_by', 'id')
        sort = sort_dir + sort_by
        sort_pre_length = len(f"{sort_dir}{self.sort_pre_count_value}")  # e.g. '-numerical_' for descending numerical
        # Count sorting (e.g. sort by count of related items)
        if sort.startswith(sort_dir + self.sort_pre_count_value):
            sort_by = sort_dir + 'countitems'  # '-countitems' if descending, 'countitems' if ascending
            # Try to apply the admin_published=True constraint
            sort_field = sort[sort_pre_length:]
            queryset = queryset.annotate(countitems=Count(sort_field)).order_by(sort_by)
        # Standard sort
        else:
            # Sort descending (Z-A)
            if sort_dir == '-':
                # Convert CharField and TextField values to lowercase, for case insensitivity
                if isinstance(self.get_field_type(sort, queryset), (CharField, TextField)):
                    queryset = queryset.order_by(Lower(sort[1:]).desc())
                else:
                    queryset = queryset.order_by(sort)
            # Sort ascending (A-Z)
            else:
                # Convert CharField and TextField values to lowercase, for case insensitivity
                if isinstance(self.get_field_type(sort, queryset), (CharField, TextField)):
                    queryset = queryset.order_by(Lower(sort))
                else:
                    queryset = queryset.order_by(sort)

        # return queryset, removing duplicates
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Count of all published texts
        context['count_all_texts'] = self.model.objects.filter(public_review_approved=True).count()
        # Filter pre values
        context['filter_pre'] = self.filter_pre
        context['filter_pre_gt'] = self.filter_pre_gt
        context['filter_pre_lt'] = self.filter_pre_lt

        # Options: Sort By 
        # Alphabetical
        context['options_sortby_alphabetical'] = [
            {'value': 'shelfmark', 'label': 'Shelfmark'},
            {'value': 'collection__name', 'label': 'Collection'}
        ]
        # Numerical
        context['options_sortby_numerical'] = [
            {
                'value': f'{self.sort_pre_count_value}text_folios',
                'label': f'{self.sort_pre_count_label}Folios'
            },
        ]

        return context
