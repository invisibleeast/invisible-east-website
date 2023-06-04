from django.contrib import admin
from . import models
from django.contrib.admin import site


site.disable_action('delete_selected')


def publish(modeladmin, request, queryset):
    """
    Sets all selected items in queryset to published
    """
    queryset.update(admin_published=True)


publish.short_description = "Publish selected items (will appear on main site)"


def unpublish(modeladmin, request, queryset):
    """
    Sets all selected items in queryset to not published
    """
    queryset.update(admin_published=False)


unpublish.short_description = "Unpublish selected items (will not appear on main site)"


class HelpAdminView(admin.ModelAdmin):
    """
    Customise the admin interface: Script
    """
    list_display = ('name',
                    'description',
                    'link',
                    'image',
                    'video',
                    'pdf',
                    'admin_published')
    list_display_links = ('name',)
    list_filter = ('admin_published',)
    search_fields = ('name',
                     'description',
                     'link',
                     'image',
                     'video',
                     'pdf',
                     'admin_notes')
    actions = (publish, unpublish)
    ordering = ('name',)


# Register admin views
admin.site.register(models.HelpItem, HelpAdminView)
