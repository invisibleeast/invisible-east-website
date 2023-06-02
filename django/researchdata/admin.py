from django.contrib import admin
from django.db.models import ManyToManyField, ForeignKey
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from . import models

admin.site.site_header = 'Invisible East: Admin Dashboard'

# Three main sections:
# 1. Reusable code
# 2. Select List Models
# 3. Main models


#
# 1. Reusable code
#

ADMIN_VIEW_LIST_PER_PAGE_DEFAULT = 100


def get_model_perms_dict(self, request):
    """
    This is the default get_model_perms permissions dictionary

    The method `get_model_perms(): return {}` is used to hide select list models from admin side bar

    However, some models need to be shown, so returning the following line to these ModelAdmins:
    `get_model_perms(): return get_model_perms_dict(self, request)`
    (which uses this function) will show these select list models in the sidebar
    """
    return {
        'add': self.has_add_permission(request),
        'change': self.has_change_permission(request),
        'delete': self.has_delete_permission(request),
        'view': self.has_view_permission(request)
    }


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
    list_per_page = ADMIN_VIEW_LIST_PER_PAGE_DEFAULT
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
admin.site.register(models.SlKeyword, GenericSlAdminView)
admin.site.register(models.SlFunder, GenericSlAdminView)
admin.site.register(models.SlUnitOfMeasurement, GenericSlAdminView)
admin.site.register(models.SlDocumentCollection, GenericSlAdminView)
admin.site.register(models.SlDocumentClassification, GenericSlAdminView)
admin.site.register(models.SlDocumentCorrespondence, GenericSlAdminView)
admin.site.register(models.SlDocumentLanguage, GenericSlAdminView)
admin.site.register(models.SlTranslationLanguage, GenericSlAdminView)
admin.site.register(models.SlCountry, GenericSlAdminView)
admin.site.register(models.SlMaterial, GenericSlAdminView)
admin.site.register(models.SlMaterialInk, GenericSlAdminView)
admin.site.register(models.SlPublicationStatement, GenericSlAdminView)
admin.site.register(models.SlCalendar, GenericSlAdminView)
admin.site.register(models.SlDocumentPersonType, GenericSlAdminView)
admin.site.register(models.SlDocumentTransType, GenericSlAdminView)


#
# 3. Main models (inlines + admin views)
#


class DocumentPersonAppearanceTabularInline(admin.TabularInline):
    """
    A subform/inline form for DocumentPersonAppearance to be used in DocumentAdminView
    """
    model = models.DocumentPersonAppearance
    extra = 0
    autocomplete_fields = ('person', 'type')


class DocumentDateTabularInline(admin.TabularInline):
    """
    A subform/inline form for DocumentDate to be used in DocumentAdminView
    """
    model = models.DocumentDate
    extra = 0

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
        'admin_classification',
        'admin_public'
    )
    list_display_links = ('id',)
    list_select_related = (
        'collection',
        'language',
        'correspondence',
        'country',
    )
    list_filter = (
        'admin_public',
        ('admin_classification', RelatedDropdownFilter),
        ('collection', RelatedDropdownFilter),
        ('language', RelatedDropdownFilter),
        ('keywords', RelatedDropdownFilter),
        ('correspondence', RelatedDropdownFilter),
        ('country', RelatedDropdownFilter),
        ('materials', RelatedDropdownFilter),
    )
    search_fields = ('id', 'title', 'shelfmark')
    fieldsets = (
        ('General', {
            'fields': (
                'title',
                'subject',
                'language',
                'correspondence',
                'keywords',
                'funders',
            )
        }),
        ('Publication Statements', {
            'fields': (
                'publication_statement',
                'publication_statement_original',
                'publication_statement_republished',
            )
        }),
        ('Manuscript Identifier', {
            'fields': (
                'country',
                'collection',
                'shelfmark'
            )
        }),
        ('Physical Description', {
            'fields': (
                'materials',
                'material_details',
                'dimensions_unit',
                'dimensions_height',
                'dimensions_width',
                'physical_additional_details'
            )
        }),
        ('Correspondance', {
            'fields': (
                'place',
            )
        }),
        ('Admin', {
            'fields': (
                'admin_classification',
                'admin_public',
                'admin_commentary',
                'admin_notes',
            )
        }),
    )
    inlines = (
        DocumentPersonAppearanceTabularInline,
        DocumentDateTabularInline
    )

    def get_model_perms(self, request):
        return get_model_perms_dict(self, request)

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    class Media:
        js = ['js/custom_admin.js',]


@admin.register(models.DocumentPerson)
class DocumentPersonAdminView(GenericAdminView):
    """
    Customise the DocumentPerson section of the admin dashboard
    """

    list_display = ('id', 'name')
    list_display_links = ('id',)
    search_fields = ('id', 'name')

    def get_model_perms(self, request):
        return get_model_perms_dict(self, request)

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(models.DocumentPersonAppearance)
class DocumentPersonAppearanceAdminView(GenericAdminView):
    """
    Customise the DocumentPersonAppearance section of the admin dashboard
    """

    list_display = ('id', 'document', 'person', 'type')
    list_display_links = ('id',)
    search_fields = ('id', 'name')

    def get_model_perms(self, request):
        return get_model_perms_dict(self, request)

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


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

    def get_model_perms(self, request):
        return get_model_perms_dict(self, request)

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
