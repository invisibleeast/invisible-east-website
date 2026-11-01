from django.db import migrations
from corpus import models


def insert_text_source_format(apps, schema_editor):
    """
    Inserts data into the new SlTextSourceFormat model
    """

    names = [
        'Document',
        'Manuscript codex',
        'Published book'
    ]

    for name in names:
        models.SlTextSourceFormat.objects.create(name=name)


def update_text_source_format(apps, schema_editor):
    """
    Updates all existing Text objects, setting their source format to Document
    """

    source_format = models.SlTextSourceFormat.objects.get(name='Document')
    models.Text.objects.all().update(source_format=source_format)


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0011_sltextsourceformat_alter_textfolio_options_and_more')
    ]

    operations = [
        migrations.RunPython(insert_text_source_format),
        migrations.RunPython(update_text_source_format),
    ]
