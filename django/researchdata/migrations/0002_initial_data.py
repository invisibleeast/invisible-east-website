import xml.etree.ElementTree as ET
from pathlib import Path
from django.conf import settings
from django.db import migrations
from researchdata import models
from ast import literal_eval
from html.parser import HTMLParser
from io import StringIO
import os
import shutil


# Reusable functions/variables

PATH_OLD_DATA = os.path.join(settings.BASE_DIR, 'researchdata', 'migrations', 'old_data')


def set_related_values(data_file, main_model, relationship_type):
    """
    data_file = a .txt file containing a list of objects
    main_model = the model of the object for which the data is being set, e.g. models.Document
    relationship_type = 'fk' or 'm2m'
    """
    for object_dict in literal_eval(data_file.read()):
        # Get the main model object
        object = main_model.objects.get(id=object_dict['id'])
        # Loop through key/value pairs in object dictionary (other than the id field)
        for field, value in object_dict.items():
            if field != 'id':
                # Get the related object
                related_object = models.Document._meta.get_field(field).related_model.objects.get_or_create(name_en=value)[0]
                # Set related field value based on relationship type (either FK or M2m)
                if relationship_type == 'fk':
                    setattr(object, field, related_object)
                elif relationship_type == 'm2m':
                    getattr(object, field).add(related_object)
        # Save changes to the object
        object.save()


class MLStripper(HTMLParser):
    """
    Required by below strip_html_tags() function to remove HTML tags from a string
    """
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()


def strip_html_tags(html):
    """
    Removes HTML tags from strings, e.g. <p>xxxx</p> --> xxxx
    Used for fields that were a RichTextField in old db but a plain TextField in the new db
    """
    if html:
        # Add new lines to </p> tags before they're removed, to preserve new lines in output
        html = html.replace('<p>', '<p>\n')
        # Strip HTML tags from string and return
        stripper = MLStripper()
        stripper.feed(html)
        return stripper.get_data().strip()


# Migration functions


def insert_data_select_list_models(apps, schema_editor):
    """
    Inserts data into the new select list tables/models in this new database.
    FK data is also inserted below using get_or_create, but sometimes it's
    required to manually set additional values.
    """

    # SlDocumentLanguage
    for name in ['Arabic', 'Bactrian', 'New Persian']:
        models.SlDocumentLanguage.objects.create(name=name)

    # SlPublicationStatement
    models.SlPublicationStatement.objects.create(
        name='This document is published and distributed online by the Invisible East project, University of Oxford.'
    )

    # SlFunder
    models.SlFunder.objects.create(
        name='ERC',
        name_full='European Research Council'
    )

    # SlDocumentClassification
    for obj in [
        {'name': 'Gold', 'order': 3},
        {'name': 'Silver', 'order': 2},
        {'name': 'Bronze', 'order': 1}
    ]:
        models.SlDocumentClassification.objects.create(**obj)

    # SlCalendar
    for obj in [
        {'name': 'Gregorian', 'name_full': 'The Gregorian calendar'},
        {'name': 'Hijri', 'name_full': 'The Hijri calendar'},
        {'name': 'Bactrian', 'name_full': 'The calendar of the Bactrian era'}
    ]:
        models.SlCalendar.objects.create(**obj)


def insert_data_documents(apps, schema_editor):
    """
    Inserts data into the Document model
    """

    # Loop through all XML files found in input dir
    for root, dirs, input_files in os.walk(PATH_OLD_DATA):
        for input_file in input_files:
            if input_file.endswith(".xml"):

                # Progress monitoring
                print(f'importing: {input_file}')

                # Get XML from file as string and pre-process (e.g. remove unwanted parts)
                file_content = Path(os.path.join(root, input_file)).read_text()
                file_content = file_content.replace(' xmlns="http://www.tei-c.org/ns/1.0"', '')  # remove TEI namespace
                file_content = file_content.replace('xml:lang', 'lang')  # remove xml: namespace from lang attributes

                # Setup ET
                tree = ET.ElementTree(ET.fromstring(file_content))
                xml_root = tree.getroot()

                # Common elements that act as shortcuts
                header = xml_root.find('teiHeader')
                file_desc = header.find('fileDesc')
                profile_desc = header.find('profileDesc')
                corresp_action = profile_desc.find('correspDesc/correspAction')
                title_stmt = file_desc.find('titleStmt')
                ms_desc = file_desc.find('sourceDesc/msDesc')
                dimensions = ms_desc.find('physDesc/objectDesc/supportDesc/support/dimensions')
                body = xml_root.find('text/body')

                # Start creating data objects
                # Order based on relation (i.e. parent models, followed by child models)
                # E.g. Document (parent) comes before DocumentPerson (child)
                # Optional fields must be exception handled in case value is None or element doesn't exist in XML

                # Create Document object
                document_obj = models.Document()

                # title
                document_obj.title = title_stmt.find('title').text

                # language
                # Gets this from the filepath of the XML file (the last dir in root)
                # (Choices: Arabic, New Persian, Bactrian)
                language = root.split('/')[-1]
                document_obj.language = models.SlDocumentLanguage.objects.get(name=language)
                # correspondence
                correspondence = corresp_action.attrib['type']
                document_obj.correspondence = models.SlDocumentCorrespondence.objects.get_or_create(name=correspondence)[0]

                # Publication data, stored in separate <p> elements within publicationStmt
                pub_start_original = 'Originally published in: '
                pub_start_republished = 'The document was later republished in '
                for publication_p in file_desc.findall('publicationStmt/p'):
                    # publication_statement_original
                    if publication_p.text.startswith(pub_start_original):
                        document_obj.publication_statement_original = publication_p.text.replace(pub_start_original, '')
                    # publication_statement_republished
                    elif publication_p.text.startswith(pub_start_republished):
                        document_obj.publication_statement_republished = publication_p.text.replace(pub_start_republished, '')
                    # publication_statement
                    else:
                        document_obj.publication_statement = models.SlPublicationStatement.objects.get_or_create(name=publication_p.text)[0]

                # subject
                document_obj.subject = profile_desc.find('particDesc/p').text
                # country
                try:
                    country = ms_desc.find('msIdentifier/country').text
                    document_obj.country = models.SlCountry.objects.get_or_create(name=country)[0]
                except AttributeError:
                    pass
                # collection
                try:
                    collection = ms_desc.find('msIdentifier/institution').text
                    document_obj.collection = models.SlDocumentCollection.objects.get_or_create(name=collection)[0]
                except AttributeError:
                    pass
                # shelfmark
                try:
                    document_obj.shelfmark = ms_desc.find('msIdentifier/idno[@type="shelfmark"]').text
                except AttributeError:
                    pass
                # material_details
                document_obj.material_details = ''.join(ms_desc.find('physDesc/objectDesc/supportDesc/support/p').itertext())

                # Dimensions
                try:
                    # dimensions_unit
                    dimensions_unit = dimensions.find('height').attrib['unit']
                    document_obj.dimensions_unit = models.SlUnitOfMeasurement.objects.get_or_create(name=dimensions_unit)[0]
                    # dimensions_height
                    document_obj.dimensions_height = dimensions.find('height').text
                    # dimensions_width
                    document_obj.dimensions_width = dimensions.find('width').text
                except AttributeError:
                    pass

                # fold_lines
                # document_obj. = 
                # damage
                # document_obj. = 
                # physical_additional_details
                try:
                    # Many were empty strings with just lots of whitespace
                    physical_additional_details = ms_desc.find('physDesc/additions').text.strip()
                    # Set empty string values to be null
                    if not len(physical_additional_details):
                        physical_additional_details = None
                    document_obj.physical_additional_details = physical_additional_details
                except AttributeError:
                    pass
 
                # place
                try:
                    document_obj.place = corresp_action.find('placeName').text
                except AttributeError:
                    pass

                # Save Document object in db
                document_obj.save()

                # Once Document object is saved in db we can add related data,
                # e.g. reverse FK objects and M2M relationships

                # Reverse FK objects:
                # DocumentPersonAppearance
                for person in corresp_action.findall('persName'):
                    models.DocumentPersonAppearance.objects.create(
                        document=document_obj,
                        type=models.SlDocumentPersonType.objects.get_or_create(name=person.attrib['type'])[0],
                        person=models.DocumentPerson.objects.get_or_create(name=person.text)[0]
                    )
                # DocumentDate
                for date in corresp_action.findall('date'):
                    # Define values
                    calendar = date.attrib['calendar'].replace('#', '')
                    try:
                        date_when = date.attrib['when']
                    except KeyError:
                        date_when = None
                    try:
                        date_not_before = date.attrib['notBefore']
                    except KeyError:
                        date_not_before = None
                    try:
                        date_not_after = date.attrib['notAfter']
                    except KeyError:
                        date_not_after = None
                    try:
                        date_text = date.text
                    except AttributeError:
                        pass
                    # Create the object
                    models.DocumentDate.objects.create(
                        document=document_obj,
                        calendar=models.SlCalendar.objects.get_or_create(name=calendar)[0],
                        date=date_when,
                        date_not_before=date_not_before,
                        date_not_after=date_not_after,
                        date_text=date_text
                    )

                # M2M relationships
                # (some only have 1 instance in XML but field is M2M for future flexibility):
                # Keywords
                for keyword in profile_desc.findall('textClass/keywords/term'):
                    # Ignore location-based keywords for now until confirmed by team that this should actually be a keyword TODO
                    if 'type' not in keyword.attrib:
                        document_obj.keywords.add(
                            models.SlKeyword.objects.get_or_create(name=keyword.text)[0]
                        )

                # Funders
                funder = title_stmt.find('funder').text
                document_obj.funders.add(
                    models.SlFunder.objects.get_or_create(name=funder)[0]
                )

                # Materials
                material = ms_desc.find('physDesc/objectDesc/supportDesc').attrib['material']
                document_obj.materials.add(
                    models.SlMaterial.objects.get_or_create(name=material)[0]
                )


def insert_data_documents_fk(apps, schema_editor):
    """
    Inserts data for foreign key fields in the Document model
    """

    with open(os.path.join(PATH_OLD_DATA, "data_documents_fk.txt"), 'r') as file:
        set_related_values(file, models.Document, 'fk')


def insert_data_documents_m2m(apps, schema_editor):
    """
    Inserts data for many to many fields in the Document model
    """

    with open(os.path.join(PATH_OLD_DATA, "data_documents_m2m.txt"), 'r') as file:
        set_related_values(file, models.Document, 'm2m')


def insert_data_documentimages(apps, schema_editor):
    """
    Inserts data into the Document Image model
    """

    # Delete thumbnail directory and the existing images in them, to start fresh
    try:
        shutil.rmtree(os.path.join(settings.BASE_DIR, f"media/palaeography/documentimages-thumbnails"))
    except FileNotFoundError:
        pass  # it's ok if can't find dir, will just skip it

    with open(os.path.join(PATH_OLD_DATA, "data_documentimages.txt"), 'r') as file:
        for object in literal_eval(file.read()):

            # Tidy custom_instructions data
            object['custom_instructions'] = strip_html_tags(object['custom_instructions'])

            # Save object
            models.DocumentImage.objects.create(**object)


def insert_data_documentimageparts(apps, schema_editor):
    """
    Inserts data into the Document Image Part model
    """

    with open(os.path.join(PATH_OLD_DATA, "data_documentimageparts.txt"), 'r') as file:
        for object in literal_eval(file.read()):
            models.DocumentImagePart.objects.create(**object)


class Migration(migrations.Migration):

    dependencies = [
        ('researchdata', '0001_initial')
    ]

    operations = [
        migrations.RunPython(insert_data_select_list_models),
        migrations.RunPython(insert_data_documents),
        # migrations.RunPython(insert_data_documents_fk),
        # migrations.RunPython(insert_data_documents_m2m),
        # migrations.RunPython(insert_data_documentimages),
        # migrations.RunPython(insert_data_documentimageparts),
    ]
