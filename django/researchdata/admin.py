from django.contrib import admin
from django.utils import timezone
from django.db.models import ManyToManyField, ForeignKey
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from . import models

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
admin.site.register(models.SlDocumentType, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeLegalTransactions, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeAdministrativeInternalCorrespondence, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeAdministrativeTaxReceipts, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeAdministrativeListsAndAccounting, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeLandMeasurementUnits, GenericSlAdminView)
admin.site.register(models.SlDocumentTypePeopleAndProcessesAdmin, GenericSlAdminView)
admin.site.register(models.SlDocumentTypePeopleAndProcessesLegal, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeDocumentation, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeGeographicAdministrativeUnits, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeLegalAndAdministrativeStockPhrases, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeFinanceAndAccountancyPhrases, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeAgriculturalProduce, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeCurrenciesAndDenominations, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeMarkings, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeReligion, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeToponymBamiyan, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeToponymFiruzkuh, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeToponymPersianKhalili, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeToponymBactrian, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeToponymKhurasan, GenericSlAdminView)
admin.site.register(models.SlDocumentTypeToponymMiddlePersian, GenericSlAdminView)
admin.site.register(models.SlKeyword, GenericSlAdminView)
admin.site.register(models.SlFunder, GenericSlAdminView)
admin.site.register(models.SlUnitOfMeasurement, GenericSlAdminView)
admin.site.register(models.SlDocumentCollection, GenericSlAdminView)
admin.site.register(models.SlDocumentClassification, GenericSlAdminView)
admin.site.register(models.SlDocumentCorrespondence, GenericSlAdminView)
admin.site.register(models.SlDocumentWritingSupport, GenericSlAdminView)
admin.site.register(models.SlDocumentScript, GenericSlAdminView)
admin.site.register(models.SlDocumentLanguage, GenericSlAdminView)
admin.site.register(models.SlTranslationLanguage, GenericSlAdminView)
admin.site.register(models.SlCountry, GenericSlAdminView)
admin.site.register(models.SlMaterial, GenericSlAdminView)
admin.site.register(models.SlMaterialInk, GenericSlAdminView)
admin.site.register(models.SlPublicationStatement, GenericSlAdminView)
admin.site.register(models.SlCalendar, GenericSlAdminView)
admin.site.register(models.SlPersonInDocumentType, GenericSlAdminView)
admin.site.register(models.SlDocumentTransType, GenericSlAdminView)
admin.site.register(models.SlM2MPersonToPersonRelationshipType, GenericSlAdminView)


#
# 3. Inlines
#


class PersonInDocumentTabularInline(admin.TabularInline):
    """
    A subform/inline form for PersonInDocument to be used in DocumentAdminView
    """
    model = models.PersonInDocument
    extra = 0
    classes = ['collapse']
    autocomplete_fields = ('person', 'type')


class DocumentDateTabularInline(admin.TabularInline):
    """
    A subform/inline form for DocumentDate to be used in DocumentAdminView
    """
    model = models.DocumentDate
    extra = 0
    classes = ['collapse']


class M2MPersonToPerson1Inline(admin.TabularInline):
    model = models.Person.person.through
    fk_name = "person_2"
    classes = ['collapse']
    autocomplete_fields = ('person_1', 'relationship_type')


class M2MPersonToPerson2Inline(admin.TabularInline):
    model = models.Person.person.through
    fk_name = "person_1"
    classes = ['collapse']
    autocomplete_fields = ('person_2', 'relationship_type')


#
# 4. Main model admin views
#


@admin.register(models.Document)
class DocumentAdminView(GenericAdminView):
    """
    Customise the Document section of the admin dashboard
    """

    list_display = (
        'id',
        'title',
        'collection',
        'shelfmark',
        'language',
        'correspondence',
        'country',
        'public_approved',
        'admin_classification',
    )
    list_display_links = ('id',)
    list_select_related = (
        'collection',
        'language',
        'correspondence',
        'country',
    )
    list_filter = (
        ('public_review_requests', RelatedDropdownFilter),
        ('admin_classification', RelatedDropdownFilter),
        ('collection', RelatedDropdownFilter),
        ('language', RelatedDropdownFilter),
        ('keywords', RelatedDropdownFilter),
        ('correspondence', RelatedDropdownFilter),
        ('country', RelatedDropdownFilter),
        ('materials', RelatedDropdownFilter),
    )
    search_fields = ('id', 'title', 'shelfmark')
    readonly_fields = (
        'public_approval_1_of_2_datetime',
        'public_approval_2_of_2_datetime',
        'meta_created_by',
        'meta_created_datetime',
        'meta_lastupdated_by',
        'meta_lastupdated_datetime',
    )
    fieldsets = (
        ('General', {
            'fields': (
                'title',
                'subject',
                'language',
                'correspondence',
                'keywords',
                'funders',
                'writing_support',
            )
        }),
        ('Document Types', {
            'fields': (
                'type',
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
                'toponym_bamiyan',
                'toponym_firuzkuh',
                'toponym_persian_khalili',
                'toponym_bactrian',
                'toponym_khurasan',
                'toponym_middle_persian'
            ),
            'classes': ['collapse in']
        }),
        ('Publication Statements', {
            'fields': (
                'publication_statement',
                'publication_statement_original',
                'publication_statement_republished',
            ),
            'classes': ['collapse in']
        }),
        ('Manuscript Identifier', {
            'fields': (
                'country',
                'collection',
                'shelfmark'
            ),
            'classes': ['collapse in']
        }),
        ('Physical Description', {
            'fields': (
                'materials',
                'material_details',
                'dimensions_unit',
                'dimensions_height',
                'dimensions_width',
                'physical_additional_details'
            ),
            'classes': ['collapse in']
        }),
        ('Correspondance', {
            'fields': (
                'place',
            ),
            'classes': ['collapse in']
        }),
        ('Approve Document to Show on Public Website', {
            'fields': (
                'public_review_requests',
                'public_review_notes',
                'public_approval_1_of_2',
                'public_approval_1_of_2_datetime',
                'public_approval_2_of_2',
                'public_approval_2_of_2_datetime'
            ),
            'classes': ['collapse in']
        }),
        ('Admin', {
            'fields': (
                'admin_commentary',
                'admin_classification',
                'admin_owners',
                'admin_contributors',
                'admin_notes',
                'meta_created_by',
                'meta_created_datetime',
                'meta_lastupdated_by',
                'meta_lastupdated_datetime',
            ),
            'classes': ['collapse in']
        }),
    )
    inlines = (
        PersonInDocumentTabularInline,
        DocumentDateTabularInline
    )

    def save_model(self, request, obj, form, change):
        # Meta: created (if not yet set) or last updated by (if created already set)
        if obj.meta_created_by is None:
            obj.meta_created_by = request.user
            # meta_created_datetime default value set in model so not needed here
        else:
            obj.meta_lastupdated_by = request.user
            obj.meta_lastupdated_datetime = timezone.now()
        obj.save()

    class Media:
        js = ['js/custom_admin.js',]


@admin.register(models.Person)
class DocumentPersonAdminView(GenericAdminView):
    """
    Customise the DocumentPerson section of the admin dashboard
    """

    list_display = ('id', 'name')
    list_display_links = ('id',)
    search_fields = ('id', 'name')
    inlines = (
        M2MPersonToPerson1Inline,
        M2MPersonToPerson2Inline
    )


@admin.register(models.PersonInDocument)
class PersonInDocumentAdminView(GenericAdminView):
    """
    Customise the PersonInDocument section of the admin dashboard
    """

    list_display = ('id', 'document', 'person', 'type')
    list_display_links = ('id',)
    search_fields = ('id', 'name')


@admin.register(models.DocumentDate)
class DocumentDateAdminView(GenericAdminView):
    """
    Customise the DocumentDate section of the admin dashboard
    """

    list_display = (
        'id',
        'document',
        'calendar',
        'date',
        'date_not_before',
        'date_not_after',
        'date_text'
    )
    list_display_links = ('id',)
    search_fields = ('id', 'name')


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
