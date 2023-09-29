from django.views.generic import (DetailView, ListView, TemplateView, View)
from django.db.models.functions import Lower
from django.db.models import (Count, Q, CharField, TextField, Prefetch)
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from functools import reduce
from operator import (or_, and_)
from bs4 import BeautifulSoup
from . import models
import json
import datetime
import re


# Special starts to the values & labels of options in 'filter' select lists
filter_pre = 'filter_'
filter_pre_mm = f'{filter_pre}mm_'  # Many to Many relationship
filter_pre_fk = f'{filter_pre}fk_'  # Foreign Key relationship
filter_pre_gt = f'{filter_pre}gt_'  # Greater than (or equal to) filter, e.g. "Date (from)"
filter_pre_lt = f'{filter_pre}lt_'  # Less than (or equal to) filter, e.g. "Date (to)"
filter_pre_bl = f'{filter_pre}hs_'  # Boolean, e.g. "Has transcription"


def clean_date_from_datetime(datetime_obj):
    """
    Return a clean date in format DD/MM/YYYY (e.g. 31/01/2023) from a datetime object
    """
    return datetime_obj.strftime('%d/%m/%Y') if datetime_obj else None


def replace_nth(string, sub, wanted, nth):
    """
    Replace only the nth instance of a substring in a string
    """

    where = [m.start() for m in re.finditer(sub, string)][nth]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    new_string = before + after

    return new_string


def html_details_link_to_text_list_filtered(filter_id, filter_object, link_text=None):
    """
    Returns a HTML anchor tag <a> that will link to the Corpus Text List page
    and filter on the object being clicked.
    E.g. if clicking 'Bactrian' in the detail then the user can see all other Bactrian Corpus Texts
    If link_text is not provided then it will automatically show the object's str as the link text
    """
    # If no link text is provided, use the object str by default
    if not link_text:
        link_text = filter_object
    # Return the complete HTML anchor tag
    return f'<a href="{reverse("corpus:text-list")}?{filter_id}={filter_object.id}">{link_text}</a>' if filter_object else None


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


def request_post_get_safe(request, name):
    """
    Gets a value from a POST request
    Returns None if an empty value is found
    """

    value = request.POST.get(name)
    return value if value and len(value) else None


def text_initial_queryset(user):
    """
    Returns the initially filtered list of Text objects used in get_queryset() methods of views below, e.g. TextDetailView and TextListView
    """

    # Show all Text objects if user can manage all
    if not user.is_anonymous and user.email in settings.USERS_WHO_CAN_MANAGE_ALL_TEXTS:
        return models.Text.objects.all()

    # If user isn't allowed to manage all
    else:
        # If the user is logged in only show published objects, unless user is the principal editor or data entry person of this Text (so they can preview it)
        if not user.is_anonymous:
            text_filter = Q(public_review_approved=True) | Q(admin_principal_editor=user) | Q(admin_principal_data_entry_person=user)
        # If user is not logged in only show published objects
        else:
            text_filter = Q(public_review_approved=True)

        # Return the filtered queryset of Text objects
        return models.Text.objects.filter(text_filter)


class TextDetailView(DetailView):
    """
    Class-based view for Text detail template
    """
    template_name = 'corpus/text-detail.html'
    model = models.Text

    def get_queryset(self):
        # Start with the initial queryset of Text objects
        queryset = text_initial_queryset(self.request.user)

        # Improve performance
        queryset = queryset.select_related(
            'primary_language__script',
            'type__category',
            'century',
            'collection',
        ).prefetch_related(
            'text_folios',
            'texts',
            'text_related_publications',
            'text_dates',
            'persons_in_texts'
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['text_folios'] = self.object.text_folios.all().select_related(
            'side',
            'open_state'
        ).prefetch_related(
            Prefetch(
                'text_folio_tags',
                models.TextFolioTag.objects.all().select_related('tag__category')
            )
        )
        context['text_folio_tag_categories'] = models.SlTextFolioTagCategory.objects.all().prefetch_related('tags__text_folio_tags')
        context['text_folio_tags'] = models.SlTextFolioTag.objects.all().select_related('category')
        context['permalink'] = self.request.build_absolute_uri().split('?')[0]
        context['toponym_tags'] = models.SlTextFolioTag.objects.filter(category__name='Toponyms', text_folio_tags__text_folio__text=self.object)\
            .select_related(
                'category',
            ).prefetch_related(
                Prefetch(
                    'text_folio_tags',
                    models.TextFolioTag.objects.all().select_related(
                        'text_folio__text__primary_language',
                        'text_folio__text__collection',
                    )
                )
            )
        context['data_items'] = [

            # General
            {
                'section_header': 'Details'
            },
            {
                'label': 'Shelfmark/Title', 'value': self.object.shelfmark
            },
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
                'label': 'Classification',
                'value': self.object.admin_classification.name_full
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
                    self.object.type,
                    self.object.type.name
                )
            },
            {
                'label': 'Document Subtype',
                'value': html_details_link_to_text_list_filtered(
                    f'{filter_pre_fk}document_subtype',
                    self.object.document_subtype
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
                'value': html_details_list_items(
                    f'{filter_pre_mm}writing_support_details',
                    self.object.writing_support_details.all()
                )
            },
            {
                'label': 'Writing Support Notes',
                'value': self.object.writing_support_details_additional
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
                'label': 'Fold Lines',
                'value': self.object.fold_lines_count
            },
            {
                'label': 'Fold Lines',
                'value': html_details_link_to_text_list_filtered(
                    f'{filter_pre_fk}fold_lines_alignment',
                    self.object.fold_lines_alignment
                )
            },
            {
                'label': 'Fold Lines',
                'value': self.object.fold_lines_details
            },

            # Content
            {
                'section_header': 'Content'
            },
            {
                'label': 'Summary of Content',
                'value': self.object.summary_of_content
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
            {
                'label': 'Date Added to IE Corpus',
                'value': clean_date_from_datetime(self.object.meta_created_datetime)
            },
            {
                'label': 'Date Last Updated in IE Corpus',
                'value': clean_date_from_datetime(self.object.meta_lastupdated_datetime)
            },

            # People
            {
                'section_header': 'People'
            },
            {
                'html': self.object.details_html_person_in_text
            },

            # Publications
            {
                'section_header': 'Publications'
            },
            {
                'html': self.object.details_html_publications
            },

            # Related Shelfmarks
            {
                'section_header': 'Related Shelfmarks'
            },
            {
                'html': self.object.details_html_texts
            },

            # Citations
            {
                'section_header': 'Citations'
            },
            {
                'label': 'Suggested Citation',
                'value': f'<a href="{reverse("general:about-cite")}">See \'How to Cite\'</a>'
            },
            {
                'label': 'Permalink',
                'value': f'<a href="{context["permalink"]}">{context["permalink"]}</a>'
            },
            {
                'label': 'Image Permission Statement',
                'value': self.object.image_permission_statement
            },
            {
                'label': 'Contact Editorial Team',
                'value': f'<a href="mailto:{settings.MAIN_CONTACT_EMAIL}?subject=Invisible East Digital Corpus&body=This email relates to Text {self.object.id} - {context["permalink"]}">{settings.MAIN_CONTACT_EMAIL}</a> <em>(Please include the above permalink when contacting the editorial team about this Text)</em>'
            }

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
        # Start with the initial queryset of Text objects
        queryset = text_initial_queryset(self.request.user)

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
            'text_folios__transcription',
            'text_folios__translation',
            'text_folios__transliteration',
            'text_folios__text_folio_tags__tag__name'
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
            # Remove the 'unique' data from the filter name (this is needed for unique id and name for filters that point to the same model)
            if '___unique_' in filter_key:
                filter_key = filter_key.split('___unique_')[0]
            # Perform the filter based on the type
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
                # Boolean content (e.g. field is not null or empty string)
                elif filter_key.startswith(filter_pre_bl):
                    filter_field = filter_key.replace(filter_pre_bl, '')
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
        context['filter_pre_bl'] = filter_pre_bl

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
            # Booleans
            [
                {
                    'filter_id': f'{filter_pre_bl}text_folios__image',
                    'filter_name': 'Has an Image'
                },
                {
                    'filter_id': f'{filter_pre_bl}text_folios__transcription',
                    'filter_name': 'Has a Transcription'
                },
                {
                    'filter_id': f'{filter_pre_bl}text_folios__translation',
                    'filter_name': 'Has a Translation'
                },
                {
                    'filter_id': f'{filter_pre_bl}text_folios__transliteration',
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
            # Collection
            [
                {
                    'filter_id': f'{filter_pre_fk}collection',
                    'filter_name': 'Collection',
                    'filter_options': models.SlTextCollection.objects.all()
                },
            ],
            # Type and subtype
            [
                {
                    'filter_id': f'{filter_pre_fk}type',
                    'filter_name': 'Type of Text',
                    'filter_options': models.SlTextType.objects.all().select_related('category')
                },
                {
                    'filter_id': f'{filter_pre_fk}document_subtype',
                    'filter_name': 'Document Subtype',
                    'filter_options': models.SlTextDocumentSubtype.objects.all().select_related('category')
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
            # Writing Support
            [
                {
                    'filter_id': f'{filter_pre_fk}writing_support',
                    'filter_name': 'Writing Support',
                    'filter_options': models.SlTextWritingSupport.objects.all()
                },
                {
                    'filter_id': f'{filter_pre_mm}writing_support_details',
                    'filter_name': 'Writing Support Details',
                    'filter_options': models.SlTextWritingSupportDetail.objects.all()
                },
            ],
            # Tags
            [
                {
                    'filter_group_name': 'Tags',
                },
                {
                    'filter_id': f'{filter_pre_fk}text_folios__text_folio_tags__tag___unique_ap',
                    'filter_name': 'Agricultural Produce',
                    'filter_options': models.SlTextFolioTag.objects.filter(category__name='Agricultural produce')
                },
                {
                    'filter_id': f'{filter_pre_fk}text_folios__text_folio_tags__tag___unique_cd',
                    'filter_name': 'Currencies and Denominations',
                    'filter_options': models.SlTextFolioTag.objects.filter(category__name='Currencies and denominations')
                },
                {
                    'filter_id': f'{filter_pre_fk}text_folios__text_folio_tags__tag___unique_dm',
                    'filter_name': 'Documentations',
                    'filter_options': models.SlTextFolioTag.objects.filter(category__name='Documentations')
                },
                {
                    'filter_id': f'{filter_pre_fk}text_folios__text_folio_tags__tag___unique_fa',
                    'filter_name': 'Finance and Accountancy Phrases',
                    'filter_options': models.SlTextFolioTag.objects.filter(category__name='Finance and accountancy phrases')
                },
                {
                    'filter_id': f'{filter_pre_fk}text_folios__text_folio_tags__tag___unique_ga',
                    'filter_name': 'Geographic Administrative Units',
                    'filter_options': models.SlTextFolioTag.objects.filter(category__name='Geographic administrative units')
                },
                {
                    'filter_id': f'{filter_pre_fk}text_folios__text_folio_tags__tag___unique_lm',
                    'filter_name': 'Land Measurement Units',
                    'filter_options': models.SlTextFolioTag.objects.filter(category__name='Land measurement units')
                },
                {
                    'filter_id': f'{filter_pre_fk}text_folios__text_folio_tags__tag___unique_la',
                    'filter_name': 'Legal and Administrative Stock Phrases',
                    'filter_options': models.SlTextFolioTag.objects.filter(category__name='Legal and administrative stock phrases')
                },
                {
                    'filter_id': f'{filter_pre_fk}text_folios__text_folio_tags__tag___unique_mk',
                    'filter_name': 'Markings',
                    'filter_options': models.SlTextFolioTag.objects.filter(category__name='Markings')
                },
                {
                    'filter_id': f'{filter_pre_fk}text_folios__text_folio_tags__tag___unique_lj',
                    'filter_name': 'People and processes involved in legal and judiciary system',
                    'filter_options': models.SlTextFolioTag.objects.filter(category__name='People and processes involved in legal and judiciary system')
                },
                {
                    'filter_id': f'{filter_pre_fk}text_folios__text_folio_tags__tag___unique_pa',
                    'filter_name': 'People and processes involved in public administration, tax, trade, and commerce',
                    'filter_options': models.SlTextFolioTag.objects.filter(category__name='People and processes involved in public administration, tax, trade, and commerce')
                },
                {
                    'filter_id': f'{filter_pre_fk}text_folios__text_folio_tags__tag___unique_rg',
                    'filter_name': 'Religions',
                    'filter_options': models.SlTextFolioTag.objects.filter(category__name='Religions')
                },
                {
                    'filter_id': f'{filter_pre_fk}text_folios__text_folio_tags__tag___unique_tp',
                    'filter_name': 'Toponyms',
                    'filter_options': models.SlTextFolioTag.objects.filter(category__name='Toponyms')
                },
            ]
        ]

        return context


class TextFolioTagCreateView(View):
    """
    Class-based view to create a TextFolioTag object in the database
    """

    def post(self, request):
        """
        Process the TextFolioTag object and related data objects
        """

        fail_response = HttpResponseRedirect(reverse('corpus:textfoliotag-failed'))

        try:

            text_folio_id = request_post_get_safe(request, 'textfolio')
            text_folio_obj = models.TextFolio.objects.get(id=text_folio_id)

            # Get an existing TextFolioTag object to link to a piece of trans text
            link_trans_text_to_tag = request_post_get_safe(request, 'linktranstexttotag')
            link_trans_text_to_tag = json.loads(link_trans_text_to_tag) if link_trans_text_to_tag else None
            if link_trans_text_to_tag and 'textFolioTagExistingId' in link_trans_text_to_tag:
                text_folio_tag = models.TextFolioTag.objects.get(id=int(link_trans_text_to_tag['textFolioTagExistingId']))

            else:
                # Get/Create SlTextFolioTag object
                tag_category = request_post_get_safe(request, 'category')
                tag_existing_id = request_post_get_safe(request, 'tag_existing')
                tag_new_name = request_post_get_safe(request, 'tag_new')
                if tag_existing_id:
                    tag = models.SlTextFolioTag.objects.get(id=tag_existing_id)
                elif tag_new_name:
                    tag = models.SlTextFolioTag.objects.create(
                        name=tag_new_name,
                        category=models.SlTextFolioTagCategory.objects.get(id=tag_category)
                    )
                else:
                    return fail_response

                # Create a TextFolioTag object (if a TextFolio obj is available)
                if text_folio_obj:
                    text_folio_tag = models.TextFolioTag.objects.create(
                        text_folio=text_folio_obj,
                        tag=tag,
                        details=request_post_get_safe(request, 'details'),
                        image_part_left=request_post_get_safe(request, 'image_part_left'),
                        image_part_top=request_post_get_safe(request, 'image_part_top'),
                        image_part_width=request_post_get_safe(request, 'image_part_width'),
                        image_part_height=request_post_get_safe(request, 'image_part_height'),
                        meta_created_by=request.user
                    )
                else:
                    return fail_response

            # Set the link to this text folio tag in the trans text, if this data exists
            if link_trans_text_to_tag:
                trans_text = getattr(text_folio_obj, link_trans_text_to_tag['textTrans'])
                trans_text_lines = trans_text.split('</li>')
                trans_text_line = trans_text_lines[int(link_trans_text_to_tag['textTransLineIndex'])]
                # Replaces only the required instance of the selected text (in case multiple instances)
                trans_text_line_new = replace_nth(
                    trans_text_line,
                    link_trans_text_to_tag['textSelected'],
                    f'<var data-textfoliotag="{text_folio_tag.id}">{link_trans_text_to_tag["textSelected"]}</var>',
                    int(link_trans_text_to_tag['textSelectedInstanceCountInLine'])
                )
                trans_text_lines[int(link_trans_text_to_tag['textTransLineIndex'])] = trans_text_line_new
                trans_text_new = '</li>'.join(trans_text_lines)
                # Update the TextFolio object with this new link in the trans text
                setattr(text_folio_obj, link_trans_text_to_tag['textTrans'], trans_text_new)
                text_folio_obj.save()

            # Return the user to the current page
            return HttpResponseRedirect(f"{reverse('corpus:text-detail', args=[request.POST.get('text')])}?tab=tags")

        except Exception as e:
            print(e)
            return fail_response


class TextFolioTagFailedTemplateView(TemplateView):
    """
    Class based view to show a template that tells user the attempt to save the TextFolioTag failed
    """

    template_name = 'corpus/textfoliotag-failed.html'


class TextFolioTransLineDrawnOnImageManageView(View):
    """
    Class-based view to manage (create/edit/delete) a drawing of a line of trans text from a text folio on an image
    """

    def post(self, request):
        """
        Process the drawing on image data for the specified trans field in the TextFolio object
        """

        fail_response = HttpResponseRedirect(reverse('corpus:textfoliotranslinedrawnonimage-failed'))

        try:
            # Get data from request
            text = request_post_get_safe(request, 'text')
            trans_field = request_post_get_safe(request, 'trans_field')
            line_index = request_post_get_safe(request, 'line_index')
            image_part_left = request_post_get_safe(request, 'image_part_left')
            image_part_top = request_post_get_safe(request, 'image_part_top')
            image_part_width = request_post_get_safe(request, 'image_part_width')
            image_part_height = request_post_get_safe(request, 'image_part_height')

            # Get the TextFolio object and specified trans field
            text_folio_id = request_post_get_safe(request, 'textfolio')
            text_folio_obj = models.TextFolio.objects.get(id=text_folio_id)
            text_folio_obj_trans_field = getattr(text_folio_obj, trans_field)

            # Use BS to add data attributes to the chosen li element (i.e. the line of text being drawn)
            text_folio_obj_trans_field_html = BeautifulSoup(text_folio_obj_trans_field, features="html.parser")
            trans_line = text_folio_obj_trans_field_html.find_all('li')[int(line_index)]
            trans_line['data-imagepartleft'] = image_part_left
            trans_line['data-imageparttop'] = image_part_top
            trans_line['data-imagepartwidth'] = image_part_width
            trans_line['data-imagepartheight'] = image_part_height

            setattr(text_folio_obj, trans_field, str(text_folio_obj_trans_field_html))
            text_folio_obj.save()

            # Return the user to the current page
            return HttpResponseRedirect(f"{reverse('corpus:text-detail', args=[text])}?tab={trans_field}")

        except Exception:
            return fail_response


class TextFolioTransLineDrawnOnImageFailedTemplateView(TemplateView):
    """
    Class based view to show a template that tells user the attempt to save the drawing of a line of text in a TextFolio failed
    """

    template_name = 'corpus/textfoliotranslinedrawnonimage-failed.html'


class MapTaggedTextsListView(ListView):
    """
    Class based view to show a map (of SlTextFolioTag objects) list template
    """

    template_name = 'corpus/map-taggedtexts.html'
    model = models.SlTextFolioTag

    def get_queryset(self):
        # Start with the initial queryset of SlTextFolioTag objects of category Toponym
        queryset = self.model.objects.filter(category__name='Toponyms')

        # Improve performance
        queryset = queryset.select_related(
            'category',
        ).prefetch_related(
            Prefetch(
                'text_folio_tags',
                models.TextFolioTag.objects.all().select_related(
                    'text_folio__text__primary_language',
                    'text_folio__text__collection',
                )
            )
        )

        return queryset


class MapFindSpotTemplateView(TemplateView):
    """
    Class based view to show a map (of find spots) template
    """

    template_name = 'corpus/map-findspots.html'


class MapPlacesMentionedInCorpusTextsTemplateView(TemplateView):
    """
    Class based view to show a map (of placed mentioned in texts) template
    """

    template_name = 'corpus/map-placesintexts.html'
