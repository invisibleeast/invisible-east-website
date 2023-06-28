import xml.etree.ElementTree as ET
from pathlib import Path
from django.conf import settings
from django.db import migrations
from researchdata import models
from ast import literal_eval
from html.parser import HTMLParser
from io import StringIO
from account import models as account_models
import os, shutil, re


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


def line_numbers(line_element):
    """
    Returns tuple of line number values when given ET XML <lb> element
    e.g. returns (line number, line number end)
    """
    if line_element is not None:
        if '-' in line_element.attrib['n']:
            line_transcription_n = line_element.attrib['n'].split('-')
            return (int(line_transcription_n[0]), int(line_transcription_n[1]))
        else:
            return (int(line_element.attrib['n']), None)
    else:
        return (None, None)


# Migration functions


def insert_data_select_list_models(apps, schema_editor):
    """
    Inserts data into the new select list tables/models in this new database.
    FK data is also inserted below using get_or_create, but sometimes it's
    required to manually set additional values.
    """

    # SlDocumentType
    for name in [
        'Legal',
        'Letter',
        'List or table',
        'Literary text',
        'Paraliterary',
        'Administrative'
    ]:
        models.SlDocumentType.objects.create(name=name)

    # SlDocumentTypeLegalTransactions
    for name in [
        'Worship acts (ibādat)',
        'Sale (bayʿ)',
        'Rent-hire (ʿijāra)',
        'Partnership (sharīk/shurāka)',
        'Marriage (ʿaqd, nikāh)',
        'Divorce (ṭalāq)',
        'Loan (wām)/ Debt (dayn)',
        'Amicable Settlement',
        'Preemption',
        'Power of attorney',
        'Slavery and Manumission',
        'Inheritance',
        'Donation',
        'Transfer of money (Ḥawāla)',
        'Guarantee of liability (dark-I ḍamān)',
        'Debt (Unknown origin)',
        'Penal rules',
        'Personal Status',
        'Testimony',
        'Litigation',

    ]:
        models.SlDocumentTypeLegalTransactions.objects.create(name=name)

    # SlDocumentTypeAdministrativeInternalCorrespondence
    for name in [
        'Missives to the field',
        'Informational note to the field',
        'Requests',
        'Missives for action'
    ]:
        models.SlDocumentTypeAdministrativeInternalCorrespondence.objects.create(name=name)

    # SlDocumentTypeAdministrativeTaxReceipts
    for name in [
        'TODO',
    ]:
        models.SlDocumentTypeAdministrativeTaxReceipts.objects.create(name=name)

    # SlDocumentTypeAdministrativeListsAndAccounting
    for name in [
        'TODO',
    ]:
        models.SlDocumentTypeAdministrativeListsAndAccounting.objects.create(name=name)

    # SlDocumentTypeLandMeasurementUnits
    for name in [
        'Mann',
        'Sitīr',
        'Qafīz/Qawīz',
        'Tasū',
        'Ṭās',
        'Pāra',
        'Kharwār',
        'Paymāna',
        'Juft',
        'Tīr'
        
    ]:
        models.SlDocumentTypeLandMeasurementUnits.objects.create(name=name)

    # SlDocumentTypePeopleAndProcessesAdmin
    for name in [
        'Muʿāmala',
        'Taḥakumāna (ghalla-yi)',
        'Anbār',
        'Amīn',
        'Amīr',
        'Barzigar',
        'Khaylbāsh',
        'Dihqān',
        'Raʿīs',
        'Sipahsālār',
        'Sarhang',
        'Shiḥna/shiḥnagī',
        'Mihtar',
        'Muwakkil',
        'Mīr',
        'Muhāṣṣil-i ghalla',
        'Naqīb',
        'Nāyib',
        'Muwakkil',
        'Dīwān',
        'ʿAwāriḍ (public expenses)',
    ]:
        models.SlDocumentTypePeopleAndProcessesAdmin.objects.create(name=name)

    # SlDocumentTypePeopleAndProcessesLegal
    for name in [
        'Qāḍī',
        'Faqīh',
        'Muḥtasib'
    ]:
        models.SlDocumentTypePeopleAndProcessesLegal.objects.create(name=name)

    # SlDocumentTypeDocumentation
    for name in [
        'Qabāla',
        'Barāt',
        'Chak',
        'Ḥujjat',
        'Ḥisāb/ḥisab',
        'Mithāl',
        'Nāma',
        'Nuskhat',
        'Nishān',
        'Ruqʿa',
        'Risāla'
    ]:
        models.SlDocumentTypeDocumentation.objects.create(name=name)

    # SlDocumentTypeGeographicAdministrativeUnits
    for name in [
        'Wilāyat',
        'Badiya',
        'Dīh',
        'Qariya',
        'Qaṣaba',
        'Zamīn',
        'Shahr',
        'Darra',
        'Ribāṭ',
        'Sarāy'
    ]:
        models.SlDocumentTypeGeographicAdministrativeUnits.objects.create(name=name)

    # SlDocumentTypeLegalAndAdministrativeStockPhrases
    for name in [
        'Pious invocations',
        'Bismillāh (including abbrev)',
        'In a state of sound body and mind',
        'Of their own volition and without coercion',
        'Iqrār opener',
        'Jawāz (person with legal agency)',
        'ʿUḍr/ghiflat (excuse or delay)',
        'Muhlat (extension granted)',
        'Guwāhī',
        'Dhimmat (obligation, charge)',
        'Iʿtimād nimūdan [bar-īn nishān] (trust the seal)',
        'Gharāmat (fine, debt)',
        'Ḥīmāyat (protection)',
        'Ḥaq/Ḥuqūq (obligation, policy, assessed payment)',
        'Abandoned property',
        'Tafārīqāt',
        'Tax collection (bīrun kardan)',
        'Taxes: Kharāj',
        'Taxes: ʿUshr',
        'Taxes: Jizya'
    ]:
        models.SlDocumentTypeLegalAndAdministrativeStockPhrases.objects.create(name=name)

    # SlDocumentTypeFinanceAndAccountancyPhrases
    for name in [
        'Tafṣīl (itemisation)',
        'Wajh/wujūh (in account/payment of)',
        'Bāqī (remainder)',
        'Wām (-I lāzim) (loan)'
    ]:
        models.SlDocumentTypeFinanceAndAccountancyPhrases.objects.create(name=name)

    # SlDocumentTypeAgriculturalProduce
    for name in [
        'Ghalla (grain)',
        'Gandum (wheat)',
        'Jaw (barley)',
        'Kāh (straw)',
        'Sheep',
        'Oxen',
        'Donkeys',
        'Oil',
        'Seeds',
        'Plough/plough-share/covers',
        'Hoe/sickle',
        'Shovel',
        'Harvest collecting (bardāshtan, rafʿ kardan)',
        'ʿĀsiya (mill)',
    ]:
        models.SlDocumentTypeAgriculturalProduce.objects.create(name=name)

    # SlDocumentTypeCurrenciesAndDenominations
    for name in [
        'ʿAdlī',
        'Shiyānī',
        'Sīm (-i nīk, -i rasmī)',
        'Zar',
        'Dīnār',
        'Dilīwār-I sultānī',
        'Dirham',
        'Diramsang',
        'Dāng/dāniq/danānīq (one-sixth)'
    ]:
        models.SlDocumentTypeCurrenciesAndDenominations.objects.create(name=name)

    # SlDocumentTypeMarkings
    for name in [
        'Oblique stroke (check mark)',
        'Jaʾiza (cipher)',
        'Taṣnīf (half-amount stroke above written out number)',
        'Column format',
        'Siyāq (accountants’ abbreviations of numbers)',
    ]:
        models.SlDocumentTypeMarkings.objects.create(name=name)

    # SlDocumentTypeReligion
    for name in [
        'Temple',
        'Mosque',
        'Church',
        'God(s)',
        'Fatwa/istiftāʿ',
        'Rituals'
    ]:
        models.SlDocumentTypeReligion.objects.create(name=name)

    # SlDocumentTypeToponym
    for name in [
        # Bamiyan
        'Āhangarān, آهنگران',
        'Āsiyāb, آسیاب',
        'Āsyāb-i Sar-i Rāh آسیاب سر راه',
        'ʿAjagak, عجگک',
        'Andarāba, اندرابه/ اندراب',
        'Angār. انگار',
        'Arsaf, ار سف/ سف',
        'Arsānī/Sānī, ار سانی/ سانی/ شانی/ شایی',
        'Azraw',
        'Balkh, بلخی',
        'Bāmiyān, بامیان',
        'Band-i Khāsh, بند خاش',
        'Batajlīz/Batajlīzh, بنجلیز/ بنجلیژ',
        'Butiyān, بوتیان',
        'Chākirī, چاکری/ حاکری',
        'Darra, دره',
        'Dāwar, داور',
        'Dupawi, دو پوی/ دو پول',
        'Durustī, درستی',
        'Funduqistān, فندقستان',
        'Ghandak, غندک',
        'Ghārminj (or Ghārmīkh), عار میح',
        'Ghūr Karūd [var. Garūd], غور کرود',
        'Ghūrwand, غوروند',
        'Īsh, اِیش',
        'Jawlāh /Jūlāh, جولاه',
        'Jawqāni, جوقانی',
        'Kadūr',
        'Karyān/Kadyān, کریان',
        'Kafshān/Kāfshān, کاف‌شان',
        'Karūd',
        'Kawrij',
        'Khīsh, حیس',
        'Khustgān, خستگان',
        'Miyān shahr, میان شهر',
        'Naqdī, نقدی',
        'Naw Bāgh/ Sar-i Bāgh, نو باغ/ سرباغ',
        'Nāy, نای',
        'Nayak',
        'Panjhīr, پنجهیری',
        'Rāgh, راغ',
        'Rubāṭ, رباط ',
        'Rubāṭiyān, رباطیان',
        'Rubāṭ-i Miyān shahr,رباط میانشهر',
        'Rasj, رسح مر',
        'Rīw, ریو',
        'Sabz bahār, سبزبهار',
        'Safī, سفی',
        'Safīd Sang, سفید سنگ',
        'Skānj, سکانح',
        'Sagnūl, سگ نول',
        'Sar-i Khish, سرخیش',
        'Sar Āsiyā, سر آسیا',
        'Sar-i Guzar, سری گذر',
        'Sū/ Shū, سو/ شو',
        'Surkh Dar, سرخ در',
        'Surkh Dar, סורך דר',
        'Sūya/Sūba, سویه/ سوبه',
        'Sabārghū/Shabārghū, سبارغو/ شبارغو',
        'Shawāniq, شوانق',
        'Shawār/Sawār, شوار/ سوار',
        'Shīngiryān/Sīngiryān, شنگریانی',
        'Tālīzh, تالیژ',
        'Ṭabbakhān-i Karūd, طباخان کرود',
        'Tūlak, تولکی',
        'Wak, وک',
        'Warmiyās/Wariyās, ورمیاس/ وری یاس',
        'Wāshān, درۀ واشان',
        'Wān.shān, ואנשאן',
        'Wazāmān/Farāmān/Barāmān, وزامن/ فرامن',
        'Zīr-i ʿAj, زیر عج',
        'Zīrdamān, زیر دمان',

        # Firuzkuh
        'Abdar [var. Andar]',
        'Anūr-kūh or Anūr-gird',
        'Arīz',
        'Asp-qūl',
        'Barāslīzh',
        'Bardīz',
        'Balkh',
        'Bandalīzh/Bandalīch/Bandānalīch',
        'Dāmam',
        'Fīrūzkūh',
        'Ghandamīn, Ghalmīn',
        'Ghaznīn [var. Ghaznī]',
        'Ghūr',
        'Hind',
        'Iraq',
        'Jūzjān',
        'Kāliyūn',
        'Khāy',
        'Khurāsān',
        'Maymana [var. Mayman]',
        'Murghāb',
        'Nala',
        'Naylanj',
        'Pūza-yi ʿAliyā',
        'Rabanjī',
        'Rāmtak',
        'Sakūn',
        'Sanga/Sangeh',
        'Shāristay',
        'Siparf',
        'Suf [var. Suq]',
        'Ṭāq [var. Tigāb Ṭāq/Tāgh]',
        'Tufanda',
        'Tufandī/Tukhandī',
        'Ṭūs',
        'Warsīkh',
        'Waylīzh',
        '(Wīlīzh?)',

        # PersianKhalili
        'Istīw, Istiwuy',

        # Bactrian
        'TODO',

        # Khurasan
        'TODO',

        # MiddlePersian
        'TODO',
    ]:
        models.SlDocumentTypeToponym.objects.create(name=name)

    # SlDocumentScript
    for name in [
        'Arabic',
        'Hebrew',
        'Greek-based',
        'Ancient Pahlavi'
    ]:
        models.SlDocumentScript.objects.create(name=name)

    # SlDocumentLanguage
    for obj in [
        {
            'name': 'Arabic',
            'script': models.SlDocumentScript.objects.get(name='Arabic')
        },
        {
            'name': 'Bactrian',
            'script': models.SlDocumentScript.objects.get(name='Greek-based')
        },
        {
            'name': 'Judeo-Persian',
            'script': models.SlDocumentScript.objects.get(name='Hebrew')
        },
        {
            'name': 'Middle Persian',
            'script': models.SlDocumentScript.objects.get(name='Ancient Pahlavi')
        },
        {
            'name': 'New Persian',
            'script': models.SlDocumentScript.objects.get(name='Arabic')
        },
    ]:
        models.SlDocumentLanguage.objects.create(**obj)

    # SlTranslationLanguage
    for name in [
        'English',
        'French'
    ]:
        models.SlTranslationLanguage.objects.create(name=name)

    # SlDocumentWritingSupport
    for name in [
        'paper',
        'ostraca',
        'parchment',
        'linen',
        'clay (bullae)',
        'seals',
        'stone (graves)',
    ]:
        models.SlDocumentWritingSupport.objects.create(name=name)

    # SlPublicationStatement
    models.SlPublicationStatement.objects.create(
        name='This document is published and distributed online by the Invisible East project, University of Oxford.'
    )

    # SlFunder
    models.SlFunder.objects.create(
        name='ERC',
        name_full='European Research Council'
    )

    # SlM2MPersonToPersonRelationshipType
    for name in [
        'brother',
        'sister',
        'mother',
        'father',
        'grandfather',
        'grandmother',
        'grandson',
        'granddaughter',
        'uncle',
        'aunt',
        'nephew',
        'neice',
        'colleague',
        'friend',
    ]:
        models.SlM2MPersonToPersonRelationshipType.objects.create(name=name)

    # SlDocumentClassification
    for obj in [
        {
            'name': 'Bronze',
            'description': "for internal purposes only",
            'order': 1
        },
        {
            'name': 'Silver',
            'description': "given following internal peer review",
            'order': 2
        },
        {
            'name': 'Gold',
            'description': "given following external peer review through journal/book publication",
            'order': 3
        }
    ]:
        models.SlDocumentClassification.objects.create(**obj)

    # SlDocumentPageSide
    for name in [
        'recto',
        'verso'
    ]:
        models.SlDocumentPageSide.objects.create(name=name)

    # SlDocumentPageOpen
    for name in [
        'open',
        'closed'
    ]:
        models.SlDocumentPageOpen.objects.create(name=name)

    # SlDocumentPagePartType
    for name in [
        'damage',
        'mark',
        'drawing',
        'word',
        'symbol',
        'seal',
        'sealing',
        'chord',
        'hole',
        'place',
        'date'
    ]:
        models.SlDocumentPagePartType.objects.create(name=name)

    # SlCalendar
    for obj in [
        {'name': 'Gregorian', 'name_full': 'The Gregorian calendar'},
        {'name': 'Hijri', 'name_full': 'The Hijri calendar'},
        {'name': 'Bactrian', 'name_full': 'The calendar of the Bactrian era'}
    ]:
        models.SlCalendar.objects.create(**obj)

    # SlPersonGender
    for name in [
        'male',
        'female'
    ]:
        models.SlPersonGender.objects.create(name=name)


def insert_data_documents(apps, schema_editor):
    """
    Inserts data into the Document model
    """

    # Loop through all XML files found in input dir
    prefix_map = {"xml": "http://relaxng.org/ns/structure/1.0"}
    for root, dirs, input_files in os.walk(PATH_OLD_DATA):
        for input_file in input_files:
            if input_file.endswith(".xml"):

                # Progress monitoring
                print(f'importing: {input_file}')

                # Get XML from file as string and pre-process (e.g. remove unwanted parts)
                file_content = Path(os.path.join(root, input_file)).read_text()
                # remove TEI namespace
                file_content = file_content.replace(' xmlns="http://www.tei-c.org/ns/1.0"', '')
                # remove xml: namespace
                file_content = file_content.replace('xml:', '')

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
                # id_nicholas_simms_williams
                try:
                    document_obj.id_nicholas_simms_williams = ms_desc.find('msIdentifier/idno[@type="NSW"]').text
                except AttributeError:
                    pass
                # country
                try:
                    country = ms_desc.find('msIdentifier/country').text
                    document_obj.country = models.SlCountry.objects.get_or_create(name=country)[0]
                except AttributeError:
                    pass
                # subject
                document_obj.subject = '\n\n'.join(
                    [subject.text for subject in profile_desc.findall('particDesc/p')]
                )
                # type
                document_type = profile_desc.findall('textClass/keywords/term')[0].text
                document_obj.type = models.SlDocumentType.objects.get_or_create(name=document_type)[0]

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

                # writing_support
                writing_support = ms_desc.find('physDesc/objectDesc/supportDesc').attrib['material']
                document_obj.writing_support = models.SlDocumentWritingSupport.objects.get_or_create(name=writing_support)[0]
                # writing_support_details
                # Includes tags within e.g. "blah blah <material>blah</material> blah blah" so itertext() will remove the tags
                document_obj.writing_support_details = ''.join(ms_desc.find('physDesc/objectDesc/supportDesc/support/p').itertext())

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
                try:
                    # Join multiple <p> tag text into single string, separated with new lines
                    fold_lines_count_details = '\n\n'.join(
                        [flcd.text for flcd in ms_desc.findall('physDesc/objectDesc/layoutDesc/p')]
                    )
                    document_obj.fold_lines_count_details = fold_lines_count_details
                    # Get all numbers from the details string and add them together to likely give the total count
                    fold_lines_count_numbers = re.findall(r'\d+', fold_lines_count_details)
                    document_obj.fold_lines_count_total = sum(map(int, fold_lines_count_numbers))
                except AttributeError:
                    pass

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

                # meta_created_by
                try:
                    meta_created_by = None
                    # Ed
                    if title_stmt.find('respStmt[@id="EST"]', prefix_map):
                        meta_created_by = account_models.User.objects.get(email="edward.shawe-taylor@wolfson.ox.ac.uk")
                    # Cat
                    elif title_stmt.find('respStmt[@id="CM"]'):
                        meta_created_by = account_models.User.objects.get(email="catherine.mcnally@stx.ox.ac.uk")
                    if meta_created_by:
                        document_obj.meta_created_by = meta_created_by
                except AttributeError:
                    pass
                # meta_created_by - Cat

                # Save Document object in db
                document_obj.save()

                # Once Document object is saved in db we can add related data,
                # e.g. reverse FK objects and M2M relationships

                # Reverse FK objects:

                # PersonInDocument
                for person in corresp_action.findall('persName'):
                    models.PersonInDocument.objects.create(
                        document=document_obj,
                        person_role_in_document=models.SlPersonInDocumentRole.objects.get_or_create(name=person.attrib['type'])[0],
                        person=models.Person.objects.get_or_create(name=person.text)[0]
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
                        date_text = None
                    # Create the object
                    models.DocumentDate.objects.create(
                        document=document_obj,
                        calendar=models.SlCalendar.objects.get_or_create(name=calendar)[0],
                        date=date_when,
                        date_not_before=date_not_before,
                        date_not_after=date_not_after,
                        date_text=date_text
                    )

                # Document Pages and Lines
                for page_div in body.findall('div[@type="original"]'):

                    # Check that same amount of pb as there are ab,
                    # as below code relies on there being a matching ab for each pb
                    pb_count = len(page_div.findall('pb'))
                    ab_count = len(page_div.findall('ab'))
                    if pb_count != ab_count:
                        print(f'WARNING: pb count ({pb_count}) != ab count ({ab_count}):', input_file)

                    # DocumentPage
                    for page_index, page in enumerate(page_div.findall('pb')):

                        # Side (e.g. recto or verso)
                        side_code = page.attrib['id'].rsplit('-', 1)[-1]
                        if 'v' in side_code:
                            side_name = 'verso'
                        elif 'r' in side_code:
                            side_name = 'recto'
                        else:
                            side_name = None
                        side = models.SlDocumentPageSide.objects.get(name=side_name) if side_name else None

                        # Open state (e.g. open or closed)
                        try:
                            open_state = models.SlDocumentPageOpen.objects.filter(name=page_div.attrib['subtype']).first()
                        except KeyError:
                            open_state = None

                        # Create the DocumentPage object
                        page_obj = models.DocumentPage.objects.create(
                            document=document_obj,
                            side=side,
                            open_state=open_state
                        )

                        # DocumentPageLines within this DocumentPage
                        page_content = page_div.findall('ab')[page_index]
                        for line_transcription in page_content.findall('lb'):

                            line_transcription_id = line_transcription.attrib["id"]

                            # Set transcription line number (and line number end, if a hyphen exists, e.g. 2-3)
                            line_transcription_number, line_transcription_number_end = line_numbers(line_transcription)

                            # Check that line numbers match numbers in ID
                            if line_transcription.attrib['n'] not in line_transcription_id:
                                print('WARNING: Mismatched line number and ID in:', input_file, line_transcription.attrib['n'], ' --- ', line_transcription_id)

                            # Find matching line in translation
                            # Note, not all will be found, as some lines become grouped in a range
                            # (e.g. lines 2, 3, 4 may be translated into a single line of range 2-4)
                            line_translation_id = f'tr-{line_transcription_id}'
                            line_translation = body.find(f'div[@type="translation"]/ab/lb[@id="{line_translation_id}"]')

                            # If not found, likely due to being in a range
                            if line_translation is None:
                                for potential_line_translation in body.findall(f'div[@type="translation"]/ab/lb[@id]'):
                                    # Get first line in range (e.g. line 4 in 4-6, ignoring 5 and 6)
                                    if potential_line_translation.attrib['id'].startswith(f'{line_translation_id}-'):
                                        line_translation = potential_line_translation
                                        break

                            # Set translation line number (and line number end, if a hyphen exists, e.g. 2-3)
                            line_translation_number, line_translation_number_end = line_numbers(line_translation)

                            # Create the DocumentPageLine object
                            try:
                                line_obj = models.DocumentPageLine.objects.create(
                                    document_page=page_obj,
                                    transcription_line_number=line_transcription_number,
                                    transcription_line_number_end=line_transcription_number_end,
                                    transcription_text=line_transcription.tail.strip(),
                                )
                            except AttributeError as e:
                                # pass
                                print(input_file, line_transcription_id, e)

                            # place TODO

                            # Add translation data to line obj (separately, as optional)
                            try:
                                line_obj.translation_line_number = line_translation_number
                                line_obj.translation_line_number_end = line_translation_number_end
                                line_obj.translation_text = line_translation.tail.strip()
                                line_obj.save()
                            except AttributeError:
                                pass
                                # print(input_file, line_transcription_id)

                # M2M relationships
                # (some only have 1 instance in XML but field is M2M for future flexibility):

                # Toponyms (place/location)
                try:
                    toponym = profile_desc.findall('textClass/keywords/term[@type="location"]')[0].text
                    document_obj.toponyms.add(
                        models.SlDocumentTypeToponym.objects.get_or_create(name=toponym)[0]
                    )
                except (AttributeError, IndexError):
                    pass

                # Funders
                funder = title_stmt.find('funder').text
                document_obj.funders.add(
                    models.SlFunder.objects.get_or_create(name=funder)[0]
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
        migrations.RunPython(insert_data_documents)
    ]
