from django.views.generic import (DetailView, ListView)
from . import models


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

    def get_queryset(self):
        # Start with all objects
        queryset = self.model.objects.filter(public_review_approved=True)

        # Improve performance
        queryset = queryset.select_related(
            'type',
            'collection'
        )

        # # Search
        # # Name (must concat headname and headnumber so can search for specific person)
        # search_name = self.request.GET.get('search-name', None)
        # queryset = queryset.annotate(
        #     name=Concat('headname', Value(' '), 'headnumber', output_field=CharField())
        # ).filter(name__icontains=search_name) if search_name else queryset

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

        # # Sort
        # sort_field = self.request.GET.get('sort-field', 'nameinfo__name')
        # sort_direction = self.request.GET.get('sort-direction', '')
        # sort = sort_direction + sort_field  # desc would be "-field" asc would be "field"
        # queryset = queryset.order_by(sort, 'nameinfo__name', 'headnumber')

        # Return queryset, removing duplicates
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_all_texts'] = self.model.objects.all().count()
        # context['count_all_texts'] = self.model.objects.filter(public_review_approved=True).count()  // TODO - replace above line with this when live
        return context
