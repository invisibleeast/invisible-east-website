from django.contrib import admin
from django.utils import timezone
from django.db.models import ManyToManyField, ForeignKey
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from bs4 import BeautifulSoup
from . import models
import logging

logger = logging.getLogger(__name__)


admin.site.site_header = 'Invisible East Digital Corpus: Admin Dashboard'

# Three main sections:
# 1. Reusable code
# 2. Inlines
# 3. Select List Models
# 4. Main model admin views


#
# 1. Reusable code
#


def get_manytomany_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of many to many fields of a model
    To ignore certain fields, provide a list of such field names (as strings) using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) == ManyToManyField and f.name not in exclude)


def get_foreignkey_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of foreign key fields of a model
    To ignore certain fields, provide a list of such field names (as strings) using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) == ForeignKey and f.name not in exclude)


class GenericAdminView(admin.ModelAdmin):
    """
    This is a generic class that can be applied to most models to customise their inclusion in the Django admin.

    This class can either be inherited from to customise, e.g.:
    class [ModelName]AdminView(GenericAdminView):

    Or if you don't need to customise it just register a model, e.g.:
    admin.site.register([model name], GenericAdminView)
    """
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 100
    search_fields = ('name',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all many to many fields to display the filter_horizontal widget
        self.filter_horizontal = get_manytomany_fields(self.model)
        # Set all foreign key fields to display the autocomplete widget
        self.autocomplete_fields = get_foreignkey_fields(self.model)

    class Media:
        css = {'all': ('/static/css/custom_admin.css',)}


class GenericSlAdminView(GenericAdminView):
    """
    This is a generic admin view to be used by Select List models
    e.g. admin.site.register(models.SlArchive, GenericSlAdminView)
    """
    pass


#
# 2. Inlines
#


class PersonInTextForTextTabularInline(admin.TabularInline):
    """
    A subform/inline form for PersonInText to be used in TextAdminView
    """
    model = models.PersonInText
    extra = 1
    classes = ['collapse']
    autocomplete_fields = ('person', 'person_role_in_text')


class PersonInTextForTextPersonTabularInline(admin.TabularInline):
    """
    A subform/inline form for PersonInText to be used in TextPersonAdminView
    """
    model = models.PersonInText
    extra = 0
    autocomplete_fields = ('text', 'person_role_in_text')


class TextDateStackedInline(admin.StackedInline):
    """
    A subform/inline form for TextDate to be used in TextAdminView
    """
    model = models.TextDate
    extra = 0
    classes = ['collapse']


class TextRelatedPublicationStackedInline(admin.StackedInline):
    """
    A subform/inline form for TextRelatedPublication to be used in TextAdminView
    """
    model = models.TextRelatedPublication
    extra = 0
    classes = ['collapse']
    autocomplete_fields = ('publication',)


class TextFolioStackedInline(admin.StackedInline):
    """
    A subform/inline form for TextFolio to be used in TextAdminView
    """
    model = models.TextFolio
    extra = 0
    classes = ['collapse']
    show_change_link = True
    fields = (
        'side',
        'open_state',
        'image',
        'image_small',
        'image_medium',
        'image_large',
        'image_preview',
        ('transcription', 'translation'),
        'transliteration'
    )
    readonly_fields = ('image_small', 'image_medium', 'image_large', 'image_preview')


class TextSealStackedInline(admin.StackedInline):
    """
    A subform/inline form for Seal to be used in TextAdminView
    """
    model = models.Seal
    extra = 0
    classes = ['collapse']
    show_change_link = True
    fields = (
        'type',
        'details',
        'inscription',
        'measurements',
        'descriptions',
        'colours',
        'imprints',
        'image',
        'image_preview',
    )
    readonly_fields = ('image_small', 'image_preview')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all many to many fields to display the filter_horizontal widget
        self.filter_horizontal = get_manytomany_fields(self.model)
        # Set all foreign key fields to display the autocomplete widget
        self.autocomplete_fields = get_foreignkey_fields(self.model)


class M2MPersonToPerson1Inline(admin.TabularInline):
    """
    A subform/inline form for Person 1 to be used in PersonAdminView
    Data is read only, to show relationships set in the related person
    """
    model = models.Person.persons.through
    fk_name = "person_2"
    readonly_fields = ('person_1', 'relationship_type', 'relationship_details')
    can_delete = False
    max_num = 0
    extra = 0
    verbose_name = 'Related persons that have defined a relationship with this person'
    verbose_name_plural = verbose_name


class M2MPersonToPerson2Inline(admin.TabularInline):
    """
    A subform/inline form for Person 2 to be used in PersonAdminView
    """
    model = models.Person.persons.through
    fk_name = "person_1"
    autocomplete_fields = ('person_2', 'relationship_type')
    verbose_name = 'Related Person'


class M2MTextToText1Inline(admin.TabularInline):
    """
    A subform/inline form for Text 1 to be used in TextAdminView
    Data is read only, to show relationships set in the related text
    """
    model = models.Text.texts.through
    fk_name = "text_2"
    readonly_fields = ('text_1', 'relationship_type', 'relationship_details')
    can_delete = False
    max_num = 0
    extra = 0
    classes = ['collapse']
    verbose_name = 'Related Shelfmarks (that have defined a relationship with this Text)'
    verbose_name_plural = verbose_name


class M2MTextToText2Inline(admin.TabularInline):
    """
    A subform/inline form for Text 2 to be used in TextAdminView
    """
    model = models.Text.texts.through
    fk_name = "text_1"
    extra = 1
    autocomplete_fields = ('text_2', 'relationship_type')
    classes = ['collapse']
    verbose_name = 'Related Shelfmarks'
    verbose_name_plural = verbose_name


class M2MSlToponymToTextInline(admin.TabularInline):
    """
    A subform/inline form for Text 1 to be used in TextAdminView
    Data is read only, to show relationships set in the related text
    """
    model = models.Text.toponyms.through
    extra = 0
    verbose_name = 'Texts that this Toponym appears in'
    verbose_name_plural = verbose_name


#
# 3. Select List admin views
#

# Register Select List models (most use GenericSlAdminView)
admin.site.register(models.SlTextTypeCategory, GenericSlAdminView)
admin.site.register(models.SlTextType, GenericSlAdminView)
admin.site.register(models.SlTextDocumentSubtypeCategory, GenericSlAdminView)
admin.site.register(models.SlTextGregorianCentury, GenericSlAdminView)
admin.site.register(models.SlTextCollection, GenericSlAdminView)
admin.site.register(models.SlTextCorpus, GenericSlAdminView)
admin.site.register(models.SlTextClassification, GenericSlAdminView)
admin.site.register(models.SlTextScript, GenericSlAdminView)
admin.site.register(models.SlTextLanguage, GenericSlAdminView)
admin.site.register(models.SlTranslationLanguage, GenericSlAdminView)
admin.site.register(models.SlTextWritingSupport, GenericSlAdminView)
admin.site.register(models.SlTextWritingSupportDetail, GenericSlAdminView)
admin.site.register(models.SlTextPublication, GenericSlAdminView)
admin.site.register(models.SlCalendar, GenericSlAdminView)
admin.site.register(models.SlTextFolioSide, GenericSlAdminView)
admin.site.register(models.SlTextFolioOpen, GenericSlAdminView)
admin.site.register(models.SlTextFolioTagCategory, GenericSlAdminView)
admin.site.register(models.SlPersonInTextRole, GenericSlAdminView)
admin.site.register(models.SlSealDescription, GenericSlAdminView)
admin.site.register(models.SlSealColour, GenericSlAdminView)
admin.site.register(models.SlSealImprint, GenericSlAdminView)
admin.site.register(models.SlPersonGender, GenericSlAdminView)
admin.site.register(models.SlM2MPersonToPersonRelationshipType, GenericSlAdminView)
admin.site.register(models.SlM2MTextToTextRelationshipType, GenericSlAdminView)


@admin.register(models.SlTextDocumentSubtype)
class SlTextDocumentSubtypeAdminView(GenericSlAdminView):
    """
    Customise the SlTextDocumentSubtype, in addition to GenericSlAdminView
    """
    search_fields = ('id', 'name', 'category__name')


@admin.register(models.SlTextFolioTag)
class SlTextFolioTagAdminView(GenericSlAdminView):
    """
    Customise the SlTextFolioTag, in addition to GenericSlAdminView
    """
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')


@admin.register(models.SlTextToponym)
class SlTextToponymAdminView(GenericSlAdminView):
    """
    Customise the SlTextToponym, in addition to GenericSlAdminView
    """
    list_display = ('name', 'alternative_readings', 'alternative_pronunciations', 'latitude', 'longitude', 'urls_as_html_links')
    search_fields = ('name', 'alternative_readings', 'alternative_pronunciations', 'urls')
    fields = ('name', 'alternative_readings', 'alternative_pronunciations', 'latitude', 'longitude', 'urls')
    inlines = (M2MSlToponymToTextInline,)


#
# 4. Main model admin views
#


@admin.register(models.Text)
class TextAdminView(GenericAdminView):
    """
    Customise the Text section of the admin dashboard
    """

    list_display = (
        'id',
        'shelfmark',
        'collection',
        'primary_language',
        'type',
        'count_text_folios',
        'public_review_reviewer',
        'public_review_approved',
        'public_review_approved_by',
        'admin_classification',
    )
    list_display_links = ('id', 'shelfmark')
    list_filter = (
        'public_review_approved',
        ('public_review_reviewer', RelatedDropdownFilter),
        ('public_review_approved_by', RelatedDropdownFilter),
        ('admin_principal_editor', RelatedDropdownFilter),
        ('admin_principal_data_entry_person', RelatedDropdownFilter),
        ('admin_classification', RelatedDropdownFilter),
        ('collection', RelatedDropdownFilter),
        ('primary_language', RelatedDropdownFilter),
        ('additional_languages', RelatedDropdownFilter),
        ('gregorian_date_century', RelatedDropdownFilter),
        ('writing_support', RelatedDropdownFilter),
        ('persons_in_texts__person', RelatedDropdownFilter),
    )
    search_fields = (
        'id',
        'collection__name',
        'shelfmark',
    )
    fieldsets = (
        ('Admin', {
            'fields': (
                'admin_classification',
                'admin_principal_editor',
                'admin_principal_data_entry_person',
                'admin_contributors',
                'meta_created_by',
                'meta_created_datetime',
                'meta_lastupdated_by',
                'meta_lastupdated_datetime'
            )
        }),
        ('General', {
            'fields': (
                'shelfmark',
                'collection',
                'corpus',
                'primary_language',
                'additional_languages',
                'type',
                'document_subtype',
                'toponyms',
            )
        }),
        ('Physical Description', {
            'fields': (
                'writing_support',
                'writing_support_details',
                'writing_support_details_additional',
                'dimensions_height',
                'dimensions_width',
                'fold_lines_count',
                'fold_lines_alignment',
                'fold_lines_details',
            ),
            'classes': ['collapse']
        }),
        ('Content', {
            'fields': (
                'summary_of_content',
            ),
            'classes': ['collapse']
        }),
        ('Gregorian Date (Converted from Original Dates)', {
            'fields': (
                'gregorian_date_text',
                'gregorian_date',
                'gregorian_date_range_start',
                'gregorian_date_range_end',
                'gregorian_date_century',
            ),
            'classes': ['collapse']
        }),
        ('Commentary', {
            'fields': (
                'commentary',
            ),
            'classes': ['collapse']
        }),
        ('Review and Approve to Show this Corpus Text on Public Website', {
            'fields': (
                'public_review_reviewer',
                'public_review_notes',
                'public_review_approved',
                'public_review_approved_by',
                'public_review_approved_datetime'
            ),
            'classes': ['collapse']
        }),
    )
    inlines = (
        TextDateStackedInline,
        TextFolioStackedInline,
        TextRelatedPublicationStackedInline,
        TextSealStackedInline,
        PersonInTextForTextTabularInline,
        M2MTextToText2Inline,
        M2MTextToText1Inline,
    )

    def get_readonly_fields(self, request, obj):
        readonly_fields = [
            'public_review_reviewer',
            'public_review_notes',
            'public_review_approved',
            'public_review_approved_by',
            'public_review_approved_datetime',
            'meta_created_by',
            'meta_created_datetime',
            'meta_lastupdated_by',
            'meta_lastupdated_datetime',
        ]
        # Only allow reviewer or approver to add/remove approval
        if (obj and obj.public_review_reviewer and request.user == obj.public_review_reviewer) or (obj and obj.public_review_approved_by and request.user == obj.public_review_approved_by):
            readonly_fields.remove('public_review_approved')
        # Allow only data entry, principal editor, or the reviewer to modify review fields
        if obj and request.user in [obj.admin_principal_editor, obj.admin_principal_data_entry_person, obj.public_review_reviewer] and not obj.public_review_approved:
            readonly_fields.remove('public_review_reviewer')
            readonly_fields.remove('public_review_notes')
        return readonly_fields

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Prefetch related (multiple related data)
        queryset = queryset.prefetch_related(
            'text_folios',
        )
        # Select related (single related data)
        queryset = queryset.select_related(
            'collection',
            'primary_language__script',
            'type__category',
            'document_subtype__category'
        )
        return queryset

    def has_manage_permission(self, request, obj):
        """
        Determine if this obj can be managed (edited/deleted) by current user
        This method must be called in both has_change_permission() and has_delete_permission() below
        """
        if obj:
            # Specify users (by email address) who can always manage all texts (e.g. software dev + project lead)
            if request.user.email in settings.USERS_WHO_CAN_MANAGE_ALL_TEXTS:
                return True
            # Allow changes if neither Principal Editor and Principal Data Entry Person have been set
            elif not obj.admin_principal_editor and not obj.admin_principal_data_entry_person:
                return True
            # Allow changes if a Principal Editor has been set and is the current user
            elif obj.admin_principal_editor and obj.admin_principal_editor == request.user:
                return True
            # Allow changes if a Principal Data Entry has been set and is the current user
            elif obj.admin_principal_data_entry_person and obj.admin_principal_data_entry_person == request.user:
                return True
        return False

    def has_change_permission(self, request, obj=None):
        return self.has_manage_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_manage_permission(request, obj)

    def save_model(self, request, obj, form, change):
        # Get current object, so can access values before this save
        obj_old = self.model.objects.filter(id=obj.id).first()

        # If a new Reviewer has been chosen, email the Reviewer
        if (obj and not obj_old and obj.public_review_reviewer) or (obj and obj_old and obj.public_review_reviewer not in [None, obj_old.public_review_reviewer]):

            # Build email body content
            email_link_obj = request.build_absolute_uri(reverse('admin:corpus_text_change', args=[obj.id]))
            email_link_list = request.build_absolute_uri(reverse('admin:corpus_text_changelist') + f'?public_review_reviewer__id__exact={obj.public_review_reviewer.id}')
            email_body = f"Dear {obj.public_review_reviewer.name},\n\n\nA corpus text ({str(obj)}) has been marked as ready to review by {request.user.name}.\n\nYou can view this corpus text here: {email_link_obj}\n\nYou are the Reviewer of this corpus text, meaning you are required to review and approve it. Once approved it will be visible to all users on the public website.\n\nTo approve it, simply go to the above link, scroll to the bottom of the page, tick the 'Approved' box and click save."
            if len(obj.public_review_notes):
                email_body += f"\n\nThe current review notes for this corpus text are:\n------------------------------\n{obj.public_review_notes}\n------------------------------"
            email_body += f"\n\nYou can also see all corpus texts ready for you to review and approve here: {email_link_list}\n\n\nThanks,\nInvisible East Digital Corpus team"

            # Send the email
            try:
                send_mail(
                    'Invisible East Digital Corpus: A corpus text is ready to review',
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    (obj.public_review_reviewer.email,),
                    fail_silently=False
                )
            except Exception:
                logger.exception("Failed to send email")

        # Set public review approval
        if ((obj_old and obj_old.public_review_approved is False) or obj_old is None) and obj.public_review_approved is True:
            # Set the user and datetime of the approval
            obj.public_review_approved_by = request.user
            obj.public_review_approved_datetime = timezone.now()
            obj.public_review_reviewer = None
            # Email the project team for every 100th approved text (e.g. 100, 200, 300, ...)
            count_approved_texts = len(self.model.objects.filter(public_review_approved=True)) + 1
            if count_approved_texts % 100 == 0:
                try:
                    send_mail(
                        f'Invisible East Digital Corpus: The {count_approved_texts}th text has been approved!',
                        f"A new corpus text ({str(obj)}) has been approved to show on the public website, which marks the {count_approved_texts}th publicly visible text in the Invisible East Digital Corpus!",
                        settings.DEFAULT_FROM_EMAIL,
                        (settings.MAIN_CONTACT_EMAIL, settings.ADMINS[0][1]),
                        fail_silently=False
                    )
                except Exception:
                    logger.exception("Failed to send email")
        # If removing public review approval, update relevant fields
        elif obj_old and obj_old.public_review_approved is True and obj.public_review_approved is False:
            obj.public_review_reviewer = request.user
            obj.public_review_approved_by = None
            obj.public_review_approved_datetime = None

        # Set principal data entry person as the current user (if it's not yet set)
        if obj_old and obj_old.admin_principal_data_entry_person is None:
            obj.admin_principal_data_entry_person = request.user

        # Set meta created data (if adding a new object)
        if obj.id is None:
            obj.meta_created_by = request.user
            # meta_created_datetime default value set in model so not needed here
        # Set last updated data (if editing existing object)
        else:
            obj.meta_lastupdated_by = request.user
            obj.meta_lastupdated_datetime = timezone.now()

        super().save_model(request, obj, form, change)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all many to many fields to display the filter_horizontal widget
        self.filter_horizontal = get_manytomany_fields(self.model)
        # Set all foreign key fields to display the autocomplete widget
        self.autocomplete_fields = get_foreignkey_fields(
            model=self.model,
            exclude=['type', 'document_subtype', 'fold_lines_alignment']
        )

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.7.0/jquery.min.js',  # jQuery (must load before custom script)
            'js/custom_admin.js',  # custom script
        )


@admin.register(models.TextFolio)
class TextFolioAdminView(GenericAdminView):
    """
    Customise the TextFolio section of the admin dashboard
    """

    list_display = ('id', 'text', 'name_short', 'transcription', 'translation')
    list_display_links = ('id',)
    search_fields = (
        'text__id',
        'text__title',
        'side__name',
        'transcription',
        'translation'
    )
    fields = (
        'side',
        'open_state',
        'image',
        'image_small',
        'image_medium',
        'image_large',
        'image_preview',
        ('transcription', 'translation'),
        'transliteration'
    )
    readonly_fields = ('image_small', 'image_medium', 'image_large', 'image_preview')

    # Hide this AdminView from sidebar
    def get_model_perms(self, request):
        return {}


@admin.register(models.TextFolioTag)
class TextFolioTagAdminView(GenericAdminView):
    """
    Customise the TextFolioTag section of the admin dashboard
    """

    list_display = ('id', 'text_folio', 'tag', 'details', 'is_drawn_on_text_folio_image')
    list_display_links = ('id',)
    search_fields = (
        'id',
        'tag__name',
        'text_folio__text__shelfmark',
        'details'
    )
    readonly_fields = ('meta_created_datetime', 'meta_created_by', 'meta_lastupdated_datetime', 'meta_lastupdated_by')

    def save_model(self, request, obj, form, change):
        # Set meta created data (if adding a new object)
        if obj.id is None:
            obj.meta_created_by = request.user
            # meta_created_datetime default value set in model so not needed here
        # Set last updated data (if editing existing object)
        else:
            obj.meta_lastupdated_by = request.user
            obj.meta_lastupdated_datetime = timezone.now()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Remove the tag from the trans text
        for trans in ['transcription', 'translation', 'transliteration']:
            if getattr(obj, f'is_in_text_folio_{trans}'):
                trans_field = getattr(obj.text_folio, trans)
                trans_html = BeautifulSoup(trans_field, features="html.parser")
                for tag_element in trans_html.find_all('var', {'data-textfoliotag': obj.id}):
                    # Unwrap element (remove outer tag but leave contents)
                    # e.g. <var data-textfoliotag="1">XXXX</var> would now be XXXX
                    tag_element.unwrap()
                # Set new HTML string of the TextFolio trans field
                setattr(obj.text_folio, trans, str(trans_html))

        # Save parent TextFolio object
        obj.text_folio.save()
        # Delete TextFolioTag object
        super().delete_model(request, obj)


@admin.register(models.Person)
class TextPersonAdminView(GenericAdminView):
    """
    Customise the TextPerson section of the admin dashboard
    """

    list_display = ('id', 'name', 'gender', 'profession')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    inlines = (
        PersonInTextForTextPersonTabularInline,
        M2MPersonToPerson2Inline,
        M2MPersonToPerson1Inline
    )


@admin.register(models.PersonInText)
class PersonInTextAdminView(GenericAdminView):
    """
    Customise the PersonInText section of the admin dashboard
    """

    list_display = ('id', 'text', 'person', 'person_role_in_text')
    list_display_links = ('id',)
    search_fields = ('id', 'name')

    # Hide this AdminView from sidebar
    def get_model_perms(self, request):
        return {}


@admin.register(models.TextDate)
class TextDateAdminView(GenericAdminView):
    """
    Customise the TextDate section of the admin dashboard
    """

    list_display = (
        'id',
        'text',
        'calendar',
        'date',
        'date_range_start',
        'date_range_end',
        'date_text'
    )
    list_display_links = ('id',)
    search_fields = (
        'id',
        'text__shelfmark',
        'calendar__name',
        'date',
        'date_range_start',
        'date_range_end',
        'date_text'
    )

    # Hide this AdminView from sidebar
    def get_model_perms(self, request):
        return {}


@admin.register(models.TextRelatedPublication)
class TextRelatedPublicationAdminView(GenericAdminView):
    """
    Customise the TextRelatedPublication section of the admin dashboard
    """

    list_display = ('id', 'text', 'publication', 'pages', 'catalogue_number')
    list_display_links = ('id',)
    search_fields = ('id', 'text__shelfmark', 'publication__name', 'pages', 'catalogue_number')

    # Hide this AdminView from sidebar
    def get_model_perms(self, request):
        return {}


@admin.register(models.M2MPersonToPerson)
class M2MPersonToPersonAdminView(GenericAdminView):
    """
    Customise the M2MPersonToPerson section of the admin dashboard
    """

    list_display = (
        'id',
        'person_1',
        'relationship_type',
        'person_2',
    )
    list_display_links = ('id',)
    list_filter = ('relationship_type',)
    search_fields = (
        'id',
        'person_1__name',
        'person_2__name',
        'relationship_type__name'
    )

    # Hide this AdminView from sidebar
    def get_model_perms(self, request):
        return {}
