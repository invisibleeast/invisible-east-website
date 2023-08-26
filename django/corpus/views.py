from django.views.generic import (DetailView, ListView)
from django.db.models.functions import Lower
from django.db.models import (Count, Q, CharField, TextField, Prefetch)
from django.urls import reverse
from functools import reduce
from operator import (or_, and_)
from . import models
import datetime
import json


# Special starts to the values & labels of options in 'filter' select lists
filter_pre = 'filter_'
filter_pre_mm = f'{filter_pre}mm_'  # Many to Many relationship
filter_pre_fk = f'{filter_pre}fk_'  # Foreign Key relationship
filter_pre_gt = f'{filter_pre}gt_'  # Greater than (or equal to) filter, e.g. "Date (from)"
filter_pre_lt = f'{filter_pre}lt_'  # Less than (or equal to) filter, e.g. "Date (to)"
filter_pre_hs = f'{filter_pre}hs_'  # Has content filter, e.g. "Has transcription"


def clean_date_from_datetime(datetime_obj):
    """
    Return a clean date in format DD/MM/YYYY (e.g. 31/01/2023) from a datetime object
    """
    return datetime_obj.strftime('%m/%d/%Y') if datetime_obj else None


def html_details_link_to_text_list_filtered(filter_id, filter_object):
    """
    Returns a HTML anchor tag <a> that will link to the Corpus Text List page
    and filter on the object being clicked.
    E.g. if clicking 'Bactrian' in the detail then the user can see all other Bactrian Corpus Texts
    """
    return f'<a href="{reverse("corpus:text-list")}?{filter_id}={filter_object.id}">{filter_object}</a>' if filter_object else None


def html_details_list_items(filter_id, object_list):
    """
    Return a HTML string of a list of objects (i.e. a queryset) for use in the 'Details' tab of an item page.
    E.g. showing ManyToMany and reverse FK objects
    """

    if len(object_list):
        object_links_list = [html_details_link_to_text_list_filtered(filter_id, obj) for obj in object_list]

        # Multiple objects
        if len(object_list) > 1:
            list_items = '</li><li>'.join(object_links_list)
            return f'<ul><li>{list_items}</li></ul>'
        # 1 object
        elif len(object_list) == 1:
            return object_links_list[0]

    # No objects
    return None


class TextDetailView(DetailView):
    """
    Class-based view for Text detail template
    """
    template_name = 'corpus/text-detail.html'
    model = models.Text

    def get_queryset(self):
        queryset = self.model.objects.all() #filter(public_review_approved=True) TODO

        # Improve performance
        queryset = queryset.select_related(
            'primary_language__script',
            'type__category',
            'century',
            'collection',
        ).prefetch_related(
            'text_folios',
            'texts'
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['text_folios'] = self.object.text_folios.all().select_related('side', 'open_state')
        context['data_items'] = [

            # General
            {
                'section_header': 'Details'
            },
            {
                'label': 'Shelfmark', 'value': self.object.shelfmark},
            {
                'label': 'Collection',
                'value': html_details_link_to_text_list_filtered(
                    f'{filter_pre_fk}collection',
                    self.object.collection
                )
            },
            {
                'label': 'Corpus',
                'value': html_details_link_to_text_list_filtered(
                    f'{filter_pre_fk}corpus',
                    self.object.corpus
                )
            },
            {
                'label': 'Primary Language',
                'value': html_details_link_to_text_list_filtered(
                    f'{filter_pre_fk}primary_language',
                    self.object.primary_language
                )
            },
            {
                'label': 'Additional Languages',
                'value': html_details_list_items(
                    f'{filter_pre_mm}additional_languages',
                    self.object.additional_languages.all()
                )
            },
            {
                'label': 'Type',
                'value': html_details_link_to_text_list_filtered(
                    f'{filter_pre_fk}type',
                    self.object.type
                )
            },
            {
                'label': 'Document Subtype',
                'value': html_details_link_to_text_list_filtered(
                    f'{filter_pre_fk}document_subtype',
                    self.object.document_subtype
                )
            },

            # Dates
            {
                'section_header': 'Dates'
            },
            {
                'label': 'Century',
                'value': html_details_link_to_text_list_filtered(
                    f'{filter_pre_fk}century',
                    self.object.century
                )
            },

            # Physical Description
            {
                'section_header': 'Physical Description'
            },
            {
                'label': 'Writing Support',
                'value': html_details_link_to_text_list_filtered(
                    f'{filter_pre_fk}writing_support',
                    self.object.writing_support
                )
            },
            {
                'label': 'Writing Support Details',
                'value': self.object.writing_support_details
            },
            {
                'label': 'Height (cm)',
                'value': self.object.dimensions_height
            },
            {
                'label': 'Width (cm)',
                'value': self.object.dimensions_width
            },
            {
                'label': 'Fold Lines Details',
                'value': self.object.fold_lines_details
            },
            {
                'label': 'Physical Additional Details',
                'value': self.object.physical_additional_details
            },

            # Content
            {
                'section_header': 'Content'
            },
            {
                'label': 'Summary of Content',
                'value': self.object.summary_of_content
            },

            # Tags of Terms in Text
            {'section_header': 'Tags of Terms in Text'},
            {
                'label': 'Land Measurement Units',
                'value': html_details_list_items(
                    f'{filter_pre_mm}land_measurement_units',
                    self.object.land_measurement_units.all()
                )
            },
            {
                'label': 'People and Processes Involved in Public Administration, Tax, Trade, and Commerce',
                'value': html_details_list_items(
                    f'{filter_pre_mm}people_and_processes_admins',
                    self.object.people_and_processes_admins.all()
                )
            },
            {
                'label': 'People and Processes Involved in Legal and Judiciary System',
                'value': html_details_list_items(
                    f'{filter_pre_mm}people_and_processes_legal',
                    self.object.people_and_processes_legal.all()
                )
            },
            {
                'label': 'Documentations',
                'value': html_details_list_items(
                    f'{filter_pre_mm}documentations',
                    self.object.documentations.all()
                )
            },
            {
                'label': 'Geographic Administrative Units',
                'value': html_details_list_items(
                    f'{filter_pre_mm}geographic_administrative_units',
                    self.object.geographic_administrative_units.all()
                )
            },
            {
                'label': 'Legal and Administrative Stock Phrases',
                'value': html_details_list_items(
                    f'{filter_pre_mm}legal_and_administrative_stock_phrases',
                    self.object.legal_and_administrative_stock_phrases.all()
                )
            },
            {
                'label': 'Finance and Accountancy Phrases',
                'value': html_details_list_items(
                    f'{filter_pre_mm}finance_and_accountancy_phrases',
                    self.object.finance_and_accountancy_phrases.all()
                )
            },
            {
                'label': 'Agricultural Produce',
                'value': html_details_list_items(
                    f'{filter_pre_mm}agricultural_produce',
                    self.object.agricultural_produce.all()
                )
            },
            {
                'label': 'Currencies and Denominations',
                'value': html_details_list_items(
                    f'{filter_pre_mm}currencies_and_denominations',
                    self.object.currencies_and_denominations.all()
                )
            },
            {
                'label': 'Markings',
                'value': html_details_list_items(
                    f'{filter_pre_mm}markings',
                    self.object.markings.all()
                )
            },
            {
                'label': 'Religions',
                'value': html_details_list_items(
                    f'{filter_pre_mm}religions',
                    self.object.religions.all()
                )
            },
            {
                'label': 'Toponyms',
                'value': html_details_list_items(
                    f'{filter_pre_mm}toponyms',
                    self.object.toponyms.all()
                )
            },
            # Metadata
            {
                'section_header': 'Metadata'
            },
            {
                'label': 'Added to IE Corpus',
                'value': clean_date_from_datetime(self.object.meta_created_datetime)
            },
            {
                'label': 'Last Updated in IE Corpus',
                'value': clean_date_from_datetime(self.object.meta_lastupdated_datetime)
            },

        ]

        return context


class TextListView(ListView):
    """
    Class-based view for Text list template
    """
    template_name = 'corpus/text-list.html'
    model = models.Text
    paginate_by = 30

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
        queryset = self.model.objects.all() #filter(public_review_approved=True) TODO

        # Improve performance
        queryset = queryset.select_related(
            'primary_language__script',
            'type__category',
            'century',
            'collection',
        ).prefetch_related(
            'text_folios'
        )

        # Search
        searches = json.loads(self.request.GET.get('search', '[]'))
        field_names_to_search = [
            'shelfmark',
            'collection__name',
            'corpus__name',
            'primary_language__name',
            'primary_language__script__name',
            'type__name',
            'summary_of_content',
        ]
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

        # Filter
        for filter_key in [k for k in list(self.request.GET.keys()) if k.startswith(filter_pre)]:
            filter_value = self.request.GET.get(filter_key, '')
            if filter_value != '':
                # Many to Many relationship (uses __in comparison and filter_value is a list)
                if filter_key.startswith(filter_pre_mm):
                    filter_field = filter_key.replace(filter_pre_mm, '')
                    queryset = queryset.filter(**{f'{filter_field}__in': [filter_value]})
                # Foreign Key relationship
                elif filter_key.startswith(filter_pre_fk):
                    filter_field = filter_key.replace(filter_pre_fk, '')
                    queryset = queryset.filter(**{filter_field: filter_value})
                # Greater than or equal to
                elif filter_key.startswith(filter_pre_gt):
                    filter_field = filter_key.replace(filter_pre_gt, '')
                    queryset = queryset.filter(**{f'{filter_field}__gte': filter_value})
                # Less than or equal to
                elif filter_key.startswith(filter_pre_lt):
                    filter_field = filter_key.replace(filter_pre_lt, '')
                    queryset = queryset.filter(**{f'{filter_field}__lte': filter_value})
                # Has content (e.g. field is not null or empty string)
                elif filter_key.startswith(filter_pre_hs):
                    filter_field = filter_key.replace(filter_pre_hs, '')
                    if filter_value == 'on':
                        queryset = queryset.exclude(**{f'{filter_field}__isnull': True})  # remove null values
                        queryset = queryset.exclude(**{f'{filter_field}__exact': ''})  # remove empty strings

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
        context['filter_pre'] = filter_pre
        context['filter_pre_gt'] = filter_pre_gt
        context['filter_pre_lt'] = filter_pre_lt
        context['filter_pre_hs'] = filter_pre_hs

        # Options: Sort By
        # Alphabetical
        context['options_sortby_alphabetical'] = [
            {'value': 'shelfmark', 'label': 'Shelfmark'},
            {'value': 'century__century_number', 'label': 'Date'},
            {'value': 'meta_created_datetime', 'label': 'IE Input Date'}
        ]
        # Numerical
        context['options_sortby_numerical'] = [
            {
                'value': f'{self.sort_pre_count_value}text_folios',
                'label': f'{self.sort_pre_count_label}Folios'
            },
        ]

        # Reused querysets in below filters (specified here to avoid duplicate SQL queries)
        filter_queryset_languages = models.SlTextLanguage.objects.all().select_related('script')
        filter_queryset_centuries = models.SlTextCentury.objects.all()

        # Filters
        context['options_filters'] = [
            # Has Content
            [
                {
                    'filter_id': f'{filter_pre_hs}text_folios__image',
                    'filter_name': 'Has an Image'
                },
                {
                    'filter_id': f'{filter_pre_hs}text_folios__transcription',
                    'filter_name': 'Has a Transcription'
                },
                {
                    'filter_id': f'{filter_pre_hs}text_folios__translation',
                    'filter_name': 'Has a Translation'
                },
                {
                    'filter_id': f'{filter_pre_hs}text_folios__transliteration',
                    'filter_name': 'Has a Transliteration'
                },
            ],
            # Languages
            [
                {
                    'filter_id': f'{filter_pre_fk}primary_language',
                    'filter_name': 'Primary Language',
                    'filter_options': filter_queryset_languages
                },
                {
                    'filter_id': f'{filter_pre_fk}additional_languages',
                    'filter_name': 'Additional Languages',
                    'filter_options': filter_queryset_languages
                },
            ],
            # Dates
            [
                {
                    'filter_id': f'{filter_pre_gt}century__century_number',
                    'filter_classes': filter_pre_gt,
                    'filter_name': 'Date (from)',
                    'filter_options': filter_queryset_centuries
                },
                {
                    'filter_id': f'{filter_pre_lt}century__century_number',
                    'filter_classes': filter_pre_lt,
                    'filter_name': 'Date (to)',
                    'filter_options': filter_queryset_centuries
                }
            ],
            # Important Fields
            [
                {
                    'filter_id': f'{filter_pre_fk}collection',
                    'filter_name': 'Collection',
                    'filter_options': models.SlTextCollection.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_fk}type',
                    'filter_name': 'Type',
                    'filter_options': models.SlTextType.objects.all().select_related('category')
                },
                {
                    'filter_id': f'{filter_pre_fk}writing_support',
                    'filter_name': 'Writing Support',
                    'filter_options': models.SlTextWritingSupport.objects.all()
                },
            ],
            # Subjects
            [
                {
                    'filter_id': f'{filter_pre_mm}land_measurement_units',
                    'filter_name': 'Land Measurement Units',
                    'filter_options': models.SlTextTagLandMeasurementUnits.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_mm}people_and_processes_admins',
                    'filter_name': 'People and processes involved in public administration, tax, trade, and commerce',
                    'filter_options': models.SlTextTagPeopleAndProcessesAdmin.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_mm}people_and_processes_legal',
                    'filter_name': 'People and processes involved in legal and judiciary system',
                    'filter_options': models.SlTextTagPeopleAndProcessesLegal.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_mm}documentations',
                    'filter_name': 'Documentations',
                    'filter_options': models.SlTextTagDocumentation.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_mm}geographic_administrative_units',
                    'filter_name': 'Geographic Administrative Units',
                    'filter_options': models.SlTextTagGeographicAdministrativeUnits.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_mm}legal_and_administrative_stock_phrases',
                    'filter_name': 'Legal and Administrative Stock Phrases',
                    'filter_options': models.SlTextTagLegalAndAdministrativeStockPhrases.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_mm}finance_and_accountancy_phrases',
                    'filter_name': 'Finance and Accountancy Phrases',
                    'filter_options': models.SlTextTagFinanceAndAccountancyPhrases.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_mm}agricultural_produce',
                    'filter_name': 'Agricultural Produce',
                    'filter_options': models.SlTextTagAgriculturalProduce.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_mm}currencies_and_denominations',
                    'filter_name': 'Currencies and Denominations',
                    'filter_options': models.SlTextTagCurrenciesAndDenominations.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_mm}markings',
                    'filter_name': 'Markings',
                    'filter_options': models.SlTextTagMarkings.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_mm}religions',
                    'filter_name': 'Religions',
                    'filter_options': models.SlTextTagReligion.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_mm}toponyms',
                    'filter_name': 'Toponyms',
                    'filter_options': models.SlTextTagToponym.objects.all()
                },
            ]
        ]

        return context
