"""
Creates new objects in database (primarily Text model and related models)
using data from an Excel spreadsheet.

Note, the spreadsheet must contain columns that match the field names in this script.

The spreadsheet must be called 'data.xlsx' and stored in a directory called 'data' in this 'dataimport' directory, which is ignored from Git.

cd to main django dir and run the script directly using shell: python manage.py shell < corpus/dataimport/import-texts.py
"""


from django.conf import settings
from django.utils import timezone
from corpus import models
from account import models as account_models
import pandas as pd
import os
import math


def clean(value):
    """
    Cleans a provided value from the spreadsheet to make it suitable for use in database
    """
    if str(value) == 'nan':
        value = None
    if isinstance(value, str):
        value = value.strip()
    return value


# Get data from Excel spreadsheet, use pandas to store as a dictionary
records = pd.read_excel(
    os.path.join(settings.BASE_DIR, 'corpus', 'dataimport', 'data', 'data.xlsx')
).to_dict('records')

# Loop through each record
for i, record in enumerate(records):
    # Print progress (in 10% steps)
    progress_percentage = math.floor(((i + 1) / len(records)) * 100)
    if progress_percentage % 10 == 0:
        print(f'{i + 1} / {len(records)} ({progress_percentage}%)')

    # Create new Text object with mandatory fields
    text_obj = models.Text.objects.create(
        collection=models.SlTextCollection.objects.get_or_create(name=record['collection'])[0],
        shelfmark=clean(record['shelfmark']),
        primary_language=models.SlTextLanguage.objects.get_or_create(
            name=record['primary_language'],
            script=models.SlTextScript.objects.get_or_create(name=record['primary_language__script'])[0]
        )[0],
    )

    # Add Optional fields (if they exist) and save object
    # User fields (e.g. editors, created by, etc)
    text_obj.admin_principal_editor = account_models.User.objects.get(username=record['admin_principal_editor'])
    text_obj.admin_principal_data_entry_person = account_models.User.objects.get(username=record['admin_principal_data_entry_person'])
    text_obj.meta_created_by = account_models.User.objects.get(username=record['meta_created_by'])
    # Approval fields
    if isinstance(record['public_review_approved_by'], str):
        text_obj.public_review_notes = "This Text was approved automatically during a data import from a spreadsheet"
        text_obj.public_review_approved_by = account_models.User.objects.get(username=record['public_review_approved_by'])
        text_obj.public_review_approved = True
        text_obj.public_review_approved_datetime = timezone.now()
    # General fields
    if isinstance(record['admin_classification'], str):
        text_obj.admin_classification = models.SlTextClassification.objects.get_or_create(name=record['admin_classification'])[0]
    if isinstance(record['corpus'], str):
        text_obj.corpus = models.SlTextCorpus.objects.get_or_create(name=record['corpus'])[0]
    if isinstance(record['type'], str):
        text_obj.type = models.SlTextType.objects.get_or_create(
            defaults={'name': record['type']},  # needed as __iexact is used below, as data in wrong case
            name__iexact=record['type'],
            category=models.SlTextTypeCategory.objects.get_or_create(name=record['type__category'])[0]
        )[0]
    text_obj.summary_of_content = clean(record['summary_of_content'])
    text_obj.commentary = clean(record['commentary'])
    # Gregorian date fields
    text_obj.gregorian_date_text = clean(record['gregorian_date_text'])
    text_obj.gregorian_date = clean(record['gregorian_date'])
    if isinstance(record['gregorian_date_century'], str):
        text_obj.gregorian_date_century = models.SlTextGregorianCentury.objects.get(name__istartswith=record['gregorian_date_century'])
    # Writing support fields
    text_obj.writing_support_details_additional = clean(record['writing_support_details_additional'])
    if isinstance(record['writing_support'], str):
        text_obj.writing_support = models.SlTextWritingSupport.objects.get_or_create(name=record['writing_support'])[0]
    # Height and Width fields
    # Must be a float, but spreadsheet includes int, float, and range as strings (e.g. "10-13") so get highest number in range
    height = clean(record['dimensions_height'])
    if isinstance(height, (str, int, float)):
        if '-' in str(height):
            height = height.split('-')[-1]
        text_obj.dimensions_height = height
    width = clean(record['dimensions_width'])
    if isinstance(width, (str, int, float)):
        if '-' in str(width):
            width = width.split('-')[-1]
        text_obj.dimensions_width = width

    # Save the changes made to text object before adding related data
    text_obj.save()

    # Create M2M relationship with this new Text
    if isinstance(record['additional_languages'], str):
        # Loop through each language, separated by "; " in data
        for additional_language in record['additional_languages'].split('; '):
            # Separate language and script, e.g. "Sanskrit (Brahmi script)"
            language = additional_language.split(' (')[0].strip()
            script = additional_language.split(' (')[-1].replace(' script)', '').strip()
            if len(language) > 3 and len(script) > 3:
                # Get/create language
                additional_language_obj = models.SlTextLanguage.objects.get_or_create(
                    name=language,
                    script=models.SlTextScript.objects.get_or_create(name=script)[0]
                )[0]
                # Add M2M relationship to new text
                text_obj.additional_languages.add(additional_language_obj)

    # Create child object values of this new Text

    # TextDate
    if isinstance(record['text_dates__calendar'], str):
        calendar = models.SlCalendar.objects.get_or_create(name=record['text_dates__calendar'])[0]
        date_text = clean(record['text_dates__date_text']) if isinstance(record['text_dates__date_text'], str) else None
        models.TextDate.objects.create(
            text=text_obj,
            calendar=calendar,
            date_text=date_text,
        )

    # TextRelatedPublication
    if isinstance(record['text_related_publications__publication'], str):
        publications = record['text_related_publications__publication'].split('\n')
        for pub in publications:
            publication = models.SlTextPublication.objects.get_or_create(name=pub)[0]
            # Create link between Text and Publication
            models.TextRelatedPublication.objects.create(
                text=text_obj,
                publication=publication,
                pages=clean(record['text_related_publications__pages']),
                catalogue_number=clean(record['text_related_publications__catalogue_number'])
            )
