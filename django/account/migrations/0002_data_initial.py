from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal
from django.db import transaction
from account import models
import sys

# Import initial_users.py, throwing an error if not found
try:
    from account.migrations.initial_users import initial_users  # NOQA
except ImportError:
    sys.exit('Unable to import initial_users.py in account/migrations (refer to initial_users.example.py for help)')


"""
This data migration adds default data for the following models:

- Group (collaborator_permissions_group)
- Permissions
- UserRoles

Note that they must come in this order due to dependencies
"""


def insert_groups(apps, schema_editor):
    """
    Inserts user Group
    Groups used for setting permissions
    This function must come before inserting users, as users get added to groups when saved
    """

    groups = [
        {
            "name": "collaborator_permissions_group"
        }
    ]

    Group = apps.get_model("auth", "Group")
    for group in groups:
        with transaction.atomic():
            Group(**group).save()


def add_group_permissions(apps,schema_editor):
    """
    Add relevant permissions to specified group

    As permissions are set following initial migration,
    the few bits of extra lines are needed to ensure that permissions have been created
    """

    # Ensure permissions and content types have been created.
    db_alias = schema_editor.connection.alias
    emit_post_migrate_signal(2, False, db_alias)

    # Recommended way to get Group and Permission (vs importing)
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model('auth', "Permission")

    # List of permissions (view, add, change, delete) for each model within each app for each group
    group_permissions_list = [
        {
            "group_name": "collaborator_permissions_group",
            "apps": [
                {
                    "app_name": "researchdata",
                    "models": [
                        {
                            "model_name": "document",
                            "permissions": ['view',]
                        },
                        {
                            "model_name": "person",
                            "permissions": ['view',]
                        },
                        {
                            "model_name": "documentdate",
                            "permissions": ['view',]
                        },
                    ]
                }
            ]
        }
    ]

    # Loop through group > app > model > permission to define all of the permissions set in group_permissions_list
    for group in group_permissions_list:
        g = Group.objects.get(name=group['group_name'])
        for app in group['apps']:
            a = app['app_name']
            for model in app['models']:
                m = model['model_name']
                for permission in model['permissions']:
                    g.permissions.add(Permission.objects.get(codename=f"{permission}_{m}", content_type__app_label=a))


def insert_user_roles(apps, schema_editor):
    """
    Inserts UserRole objects
    """

    roles = ['admin', 'collaborator']

    for role in roles:
        with transaction.atomic():
            models.UserRole(name=role).save()


def insert_users(apps, schema_editor):
    """
    Inserts default Users
    """

    for user in initial_users.INITIAL_USERS:
        with transaction.atomic():
            # Convert user role name into UserRole object
            user['role'] = models.UserRole.objects.get(name=user['role'])
            # Create user object
            models.User(**user).save()


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_groups),
        migrations.RunPython(add_group_permissions),
        migrations.RunPython(insert_user_roles),
        migrations.RunPython(insert_users)
    ]
