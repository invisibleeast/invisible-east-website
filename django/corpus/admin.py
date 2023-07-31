from django.contrib import admin
from django.utils import timezone
from django.db.models import ManyToManyField, ForeignKey
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from . import models
import logging

logger = logging.getLogger(__name__)


admin.site.site_header = 'Invisible East: Admin Dashboard'

# Three main sections:
# 1. Reusable code
# 2. Select List Models
# 3. Inlines
# 4. Main model admin views


#
# 1. Reusable code
#


def get_manytomany_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of many to many fields of a model
    To ignore certain fields, provide a list of such fields using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) == ManyToManyField and f.name not in exclude)


def get_foreignkey_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of foreign key fields of a model
    To ignore certain fields, provide a list of such fields using the exclude parameter
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


class GenericSlAdminView(GenericAdminView):
    """
    This is a generic admin view to be used by Select List models
    e.g. admin.site.register(models.SlArchive, GenericSlAdminView)
    """
    pass


#
# 2. Select List admin views
#

# Register Select List models (most, if not all, use GenericSlAdminView)
admin.site.register(models.SlTextTypeCategory, GenericSlAdminView)
admin.site.register(models.SlTextType, GenericSlAdminView)
admin.site.register(models.SlTextSubjectLegalTransactions, GenericSlAdminView)
admin.site.register(models.SlTextSubjectAdministrativeInternalCorrespondence, GenericSlAdminView)
admin.site.register(models.SlTextSubjectAdministrativeTaxReceipts, GenericSlAdminView)
admin.site.register(models.SlTextSubjectAdministrativeListsAndAccounting, GenericSlAdminView)
admin.site.register(models.SlTextSubjectLandMeasurementUnits, GenericSlAdminView)
admin.site.register(models.SlTextSubjectPeopleAndProcessesAdmin, GenericSlAdminView)
admin.site.register(models.SlTextSubjectPeopleAndProcessesLegal, GenericSlAdminView)
admin.site.register(models.SlTextSubjectDocumentation, GenericSlAdminView)
admin.site.register(models.SlTextSubjectGeographicAdministrativeUnits, GenericSlAdminView)
admin.site.register(models.SlTextSubjectLegalAndAdministrativeStockPhrases, GenericSlAdminView)
admin.site.register(models.SlTextSubjectFinanceAndAccountancyPhrases, GenericSlAdminView)
admin.site.register(models.SlTextSubjectAgriculturalProduce, GenericSlAdminView)
admin.site.register(models.SlTextSubjectCurrenciesAndDenominations, GenericSlAdminView)
admin.site.register(models.SlTextSubjectMarkings, GenericSlAdminView)
admin.site.register(models.SlTextSubjectReligion, GenericSlAdminView)
admin.site.register(models.SlTextSubjectToponym, GenericSlAdminView)
admin.site.register(models.SlFunder, GenericSlAdminView)
admin.site.register(models.SlUnitOfMeasurement, GenericSlAdminView)
admin.site.register(models.SlTextCollection, GenericSlAdminView)
admin.site.register(models.SlTextCorpus, GenericSlAdminView)
admin.site.register(models.SlTextClassification, GenericSlAdminView)
admin.site.register(models.SlTextCorrespondence, GenericSlAdminView)
admin.site.register(models.SlTextScript, GenericSlAdminView)
admin.site.register(models.SlTextLanguage, GenericSlAdminView)
admin.site.register(models.SlTranslationLanguage, GenericSlAdminView)
admin.site.register(models.SlCountry, GenericSlAdminView)
admin.site.register(models.SlTextWritingSupport, GenericSlAdminView)
admin.site.register(models.SlPublicationStatement, GenericSlAdminView)
admin.site.register(models.SlCalendar, GenericSlAdminView)
admin.site.register(models.SlTextFolioSide, GenericSlAdminView)
admin.site.register(models.SlTextFolioOpen, GenericSlAdminView)
admin.site.register(models.SlTextFolioAnnotationType, GenericSlAdminView)
admin.site.register(models.SlPersonInTextRole, GenericSlAdminView)
admin.site.register(models.SlPersonGender, GenericSlAdminView)
admin.site.register(models.SlM2MPersonToPersonRelationshipType, GenericSlAdminView)
admin.site.register(models.SlM2MTextToTextRelationshipType, GenericSlAdminView)


#
# 3. Inlines
#


class PersonInTextTabularInline(admin.TabularInline):
    """
    A subform/inline form for PersonInText to be used in TextAdminView
    """
    model = models.PersonInText
    extra = 1
    classes = ['collapse']
    autocomplete_fields = ('person', 'person_role_in_text')


class TextDateTabularInline(admin.TabularInline):
    """
    A subform/inline form for TextDate to be used in TextAdminView
    """
    model = models.TextDate
    extra = 1
    classes = ['collapse']


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
        ('transcription', 'translation'),
        'transliteration'
    )
    readonly_fields = ('image_small', 'image_medium', 'image_large',)


class TextFolioAnnotationTabularInline(admin.TabularInline):
    """
    A subform/inline form for TextFolioAnnotation to be used in TextFolioAdminView
    """
    model = models.TextFolioAnnotation
    extra = 1
    exclude = ('position_in_image',)


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
    verbose_name = 'Related Texts that have defined a relationship with this Text'
    verbose_name_plural = verbose_name


class M2MTextToText2Inline(admin.TabularInline):
    """
    A subform/inline form for Text 2 to be used in TextAdminView
    """
    model = models.Text.texts.through
    fk_name = "text_1"
    autocomplete_fields = ('text_2', 'relationship_type')
    classes = ['collapse']
    verbose_name = 'Related Text'


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
        'correspondence',
        'country',
        'id_khan',
        'id_nicholas_simms_williams',
        'public_review_ready',
        'public_review_approved',
        'public_review_approved_by',
        'admin_classification',
    )
    list_display_links = ('id', 'shelfmark')
    list_select_related = (
        'collection',
        'correspondence',
        'country',
        'primary_language',
    )
    list_filter = (
        'public_review_ready',
        'public_review_approved',
        ('public_review_approved_by', RelatedDropdownFilter),
        ('admin_principal_editor', RelatedDropdownFilter),
        ('admin_principal_data_entry_person', RelatedDropdownFilter),
        ('admin_classification', RelatedDropdownFilter),
        ('primary_language', RelatedDropdownFilter),
        ('collection', RelatedDropdownFilter),
        ('additional_languages', RelatedDropdownFilter),
        ('correspondence', RelatedDropdownFilter),
        ('country', RelatedDropdownFilter),
        ('persons_in_texts__person', RelatedDropdownFilter),
        ('writing_support', RelatedDropdownFilter),
    )
    search_fields = (
        'id',
        'collection__name',
        'country__name',
        'shelfmark',
        'id_khan',
        'id_nicholas_simms_williams',
    )
    fieldsets = (
        ('Admin', {
            'fields': (
                'admin_classification',
                'admin_principal_editor',
                'admin_principal_data_entry_person',
                'admin_contributors',
                'admin_commentary',
                'meta_created_by',
                'meta_created_datetime',
                'meta_lastupdated_by',
                'meta_lastupdated_datetime'
            ),
            'classes': ['collapse']
        }),
        ('General', {
            'fields': (
                'shelfmark',
                'collection',
                'corpus',
                'primary_language',
                'type',
                'correspondence',
                'description',
                'id_khan',
                'id_nicholas_simms_williams',
                'country',
                'additional_languages',
                'funders'
            )
        }),
        ('Subjects', {
            'fields': (
                'legal_transactions',
                'administrative_internal_correspondences',
                'administrative_tax_receipts',
                'administrative_lists_and_accounting',
                'land_measurement_units',
                'people_and_processes_admins',
                'people_and_processes_legal',
                'documentations',
                'geographic_administrative_units',
                'legal_and_administrative_stock_phrases',
                'finance_and_accountancy_phrases',
                'agricultural_produce',
                'currencies_and_denominations',
                'markings',
                'religions',
                'toponyms'
            ),
            'classes': ['collapse']
        }),
        ('Publication Statements', {
            'fields': (
                'publication_statement',
                'publication_statement_original',
                'publication_statement_republished'
            ),
            'classes': ['collapse']
        }),
        ('Physical Description', {
            'fields': (
                'writing_support',
                'writing_support_details',
                'dimensions_unit',
                'dimensions_height',
                'dimensions_width',
                'fold_lines_count_details',
                'fold_lines_count_total',
                'physical_additional_details'
            ),
            'classes': ['collapse']
        }),
        ('Review and Approve to Show this Corpus Text on Public Website', {
            'fields': (
                'public_review_ready',
                'public_review_notes',
                'public_review_approved',
                'public_review_approved_by',
                'public_review_approved_datetime'
            ),
            'classes': ['collapse']
        }),
    )
    inlines = (
        M2MTextToText2Inline,
        M2MTextToText1Inline,
        PersonInTextTabularInline,
        TextDateTabularInline,
        TextFolioStackedInline
    )

    def get_readonly_fields(self, request, obj):
        readonly_fields = [
            'public_review_approved_by',
            'public_review_approved_datetime',
            'meta_created_by',
            'meta_created_datetime',
            'meta_lastupdated_by',
            'meta_lastupdated_datetime',
        ]
        # Only allow principal editor to approve (when ready to review)
        if request.user != obj.admin_principal_editor or not obj.public_review_ready:
            readonly_fields.append('public_review_approved')
        # Once approved, review fields are read only
        if obj.public_review_approved or obj.admin_principal_editor is None:
            readonly_fields += ['public_review_ready', 'public_review_notes']
        return readonly_fields

    def save_model(self, request, obj, form, change):
        # Get current object, so can access values before this save
        obj_old = self.model.objects.filter(id=obj.id).first()

        # If marked as ready to review, email the Principal Editor
        if ((obj_old and obj_old.public_review_ready is False) or obj_old is None) and obj.public_review_ready is True:
            email_link_obj = request.build_absolute_uri(reverse('admin:corpus_text_change', args=[obj.id]))
            email_link_list = request.build_absolute_uri(reverse('admin:corpus_text_changelist') + f'?admin_principal_editor__id__exact={obj.admin_principal_editor.id}&public_review_ready__exact=1')
            try:
                send_mail(
                    'Invisible East: A corpus text is ready to review',
                    f"Dear {obj.admin_principal_editor.name},\n\nA corpus text ({str(obj)}) has been marked as ready to review by {request.user.name}.\n\nYou can view this corpus text here: {email_link_obj}\n\nYou are the Principal Editor of this corpus text, meaning you are required to review and approve it. Once approved it will be visible to all users on the public website.\n\nTo approve it, simply go to the above link, scroll to the bottom of the page, tick the 'Approved' box and click save.\n\nYou can also see all corpus texts ready for you to review and approve here: {email_link_list}\n\nThanks,\nInvisible East",  # NOQA
                    settings.DEFAULT_FROM_EMAIL,
                    (obj.admin_principal_editor.email,),
                    fail_silently=False
                )
            except Exception:
                logger.exception("Failed to send email")

        # Set public review approval
        if ((obj_old and obj_old.public_review_approved is False) or obj_old is None) and obj.public_review_approved is True:
            # Set the user and datetime of the approval
            obj.public_review_approved_by = request.user
            obj.public_review_approved_datetime = timezone.now()
            obj.public_review_ready = False
        # Remove public review approval
        elif obj_old and obj_old.public_review_approved is True and obj.public_review_approved is False:
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

        obj.save()

    class Media:
        js = ['js/custom_admin.js',]


@admin.register(models.TextFolio)
class TextFolioAdminView(GenericAdminView):
    """
    Customise the TextFolio section of the admin dashboard
    """

    list_display = ('id', 'text', 'transcription', 'translation')
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
        ('transcription', 'translation'),
        'transliteration'
    )
    readonly_fields = ('image_small', 'image_medium', 'image_large',)
    inlines = (TextFolioAnnotationTabularInline,)

    # Hide this AdminView from sidebar
    def get_model_perms(self, request):
        return {}


@admin.register(models.Person)
class TextPersonAdminView(GenericAdminView):
    """
    Customise the TextPerson section of the admin dashboard
    """

    list_display = ('id', 'name', 'gender', 'profession')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    inlines = (
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
        'date_not_before',
        'date_not_after',
        'date_text'
    )
    list_display_links = ('id',)
    search_fields = ('id', 'name')

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
