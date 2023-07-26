from django.contrib import admin
from django.utils import timezone
from django.forms import Textarea
from django.db.models import ManyToManyField, ForeignKey, TextField
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
admin.site.register(models.SlTextCategory, GenericSlAdminView)
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


class TextFolioLineTabularInline(admin.TabularInline):
    """
    A subform/inline form for TextFolioLine to be used in TextFolioAdminView
    """
    model = models.TextFolioLine
    extra = 1
    exclude = ('position_in_image',)
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 35, 'style': 'height: 4em;'})},
    }


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
        'category',
        'type',
        'correspondence',
        'country',
        'id_khan',
        'id_nicholas_simms_williams',
        'public_approved',
        'admin_classification',
    )
    list_display_links = ('id',)
    list_select_related = (
        'collection',
        'correspondence',
        'country',
        'category',
    )
    list_filter = (
        ('public_review_requests', RelatedDropdownFilter),
        ('admin_classification', RelatedDropdownFilter),
        ('category', RelatedDropdownFilter),
        ('collection', RelatedDropdownFilter),
        ('languages', RelatedDropdownFilter),
        ('correspondence', RelatedDropdownFilter),
        ('country', RelatedDropdownFilter),
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
                'shelfmark',
                'collection',
                'category',
                'type',
                'correspondence',
                'description',
                'id_khan',
                'id_nicholas_simms_williams',
                'country',
                'languages',
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
        ('Approve Text to Show on Public Website', {
            'fields': (
                'public_review_requests',
                'public_review_notes',
                'public_approval_1_of_2',
                'public_approval_1_of_2_datetime',
                'public_approval_2_of_2',
                'public_approval_2_of_2_datetime'
            ),
            'classes': ['collapse']
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
                'meta_lastupdated_datetime'
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


@admin.register(models.TextFolio)
class TextFolioAdminView(GenericAdminView):
    """
    Customise the TextFolio section of the admin dashboard
    """

    list_display = ('id', 'text')
    list_display_links = ('id',)
    search_fields = (
        'text__id',
        'text__title',
        'side__name'
    )
    inlines = (
        TextFolioLineTabularInline,
        TextFolioAnnotationTabularInline
    )

    # Hide this AdminView from sidebar
    def get_model_perms(self, request):
        return {}


@admin.register(models.TextFolioLine)
class TextFolioLineAdminView(GenericAdminView):
    """
    Customise the TextFolio section of the admin dashboard
    """

    list_display = ('id', 'text_folio')
    list_display_links = ('id',)
    search_fields = ('id',)

    # Hide this AdminView from sidebar
    def get_model_perms(self, request):
        return {}


@admin.register(models.Person)
class TextPersonAdminView(GenericAdminView):
    """
    Customise the TextPerson section of the admin dashboard
    """

    list_display = ('id', 'name')
    list_display_links = ('id',)
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
