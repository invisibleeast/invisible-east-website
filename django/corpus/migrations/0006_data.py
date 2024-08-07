from django.db import migrations
from django.db.models import Q
from corpus import models


def source_of_data(apps, schema_editor):
    """
    Inserts data into the new SlTextSourceOfData model 'admin_source_of_data' and
    updates existing Text objects with values for the new 'admin_source_of_data' field
    that is an FK field to this new model

    So basically most of the "bamiyan papers" will be the first option, all of the firuzkuh papers will be the second option and all of the Arabic and Bactrian documents will be the third option. 
    """

    data = [
        {
            'source_of_data_name': 'The transcription and translation are the original work of the IEDC Team (as yet unpublished in peer-review print)',
            'texts_queryset': models.Text.objects.filter(corpus__name='Bamiyan Papers')
        },
        {
            'source_of_data_name': 'The transcription has been revised from a previous publication (see Publications), the translation is the original work of the IEDC Team (as yet unpublished in peer-review print)',
            'texts_queryset': models.Text.objects.filter(corpus__name='Firuzkuh Papers')
        },
        {
            'source_of_data_name': 'The transcription and translation have been taken from a previous publication (see Publications)',
            'texts_queryset': models.Text.objects.filter(
                Q(corpus__name='Arabic Documents from Early Islamic Khurasan')
                |
                Q(corpus__name='Bactrian Documents from Northern Afghanistan')
            )
        },
    ]

    for instance in data:
        # Create SourceOfData object
        source_of_data_object = models.SlTextSourceOfData.objects.get_or_create(name=instance['source_of_data_name'])[0]
        # Set value of existing texts to this new object
        instance['texts_queryset'].update(admin_source_of_data=source_of_data_object)


def update_image_credit_custom(apps, schema_editor):
    """
    Inserts data into the new SlTextSourceOfData model 'admin_source_of_data' and
    updates existing Text objects with values for the new 'admin_source_of_data' field
    that is an FK field to this new model
    """
    models.Text.objects.filter(corpus__name='Firuzkuh Papers').update(image_credit_custom='Mirza Khwaja Muhammad')


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0005_sltextsourceofdata_text_image_credit_custom_and_more')
    ]

    operations = [
        migrations.RunPython(source_of_data),
        migrations.RunPython(update_image_credit_custom),
    ]
