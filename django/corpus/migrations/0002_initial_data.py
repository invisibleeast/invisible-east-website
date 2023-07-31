import xml.etree.ElementTree as ET
from pathlib import Path
from django.conf import settings
from django.db import migrations
from corpus import models
from ast import literal_eval
from html.parser import HTMLParser
from io import StringIO
from account import models as account_models
import os, shutil, re


# Reusable functions/variables

PATH_OLD_DATA = os.path.join(settings.BASE_DIR, 'corpus', 'migrations', 'old_data')


def set_related_values(data_file, main_model, relationship_type):
    """
    data_file = a .txt file containing a list of objects
    main_model = the model of the object for which the data is being set, e.g. models.Text
    relationship_type = 'fk' or 'm2m'
    """
    for object_dict in literal_eval(data_file.read()):
        # Get the main model object
        object = main_model.objects.get(id=object_dict['id'])
        # Loop through key/value pairs in object dictionary (other than the id field)
        for field, value in object_dict.items():
            if field != 'id':
                # Get the related object
                related_object = models.Text._meta.get_field(field).related_model.objects.get_or_create(name_en=value)[0]
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


def folio_lines_html(folio_lines):
    """
    Return the HTML of lines of text in a trans/translation for a folio
    This will be an ordered list <ol> with <li> for each line of text
    Some lines will need the automatic line numbering manually set using the value attribute
    """
    folio_trans_text = '<ol>'
    for i, line_trans in enumerate(folio_lines):
        # Determine line number as value attribute (if need to override automatic line numbering)
        line_number = line_trans.attrib['n']
        value = ''
        range_end = ''
        # Set first line number
        if i == 0:
            value = f' value="{line_number.split("-")[0]}"'
        # Determine if there's a range in previous line and set this line number to 1 above the end range
        # e.g. if previous line is 3-4 set this to 5
        else:
            line_number_previous = folio_lines[i - 1].attrib['n']
            if '-' in line_number_previous:
                value = f' value="{int(line_number_previous.split("-")[1]) + 1}"'
        # If last line number has a range, include the end number in the 'data-range-end' attribute
        if i + 1 == len(folio_lines) and '-' in line_number:
            range_end = f' data-range-end="{line_number.split("-")[1]}"'
        # Create <li> element for this line
        folio_trans_text += f'<li{value}{range_end}>{line_trans.tail.strip()}</li>'
    folio_trans_text += '</ol>'
    return folio_trans_text


# Migration functions


def insert_data_select_list_models(apps, schema_editor):
    """
    Inserts data into the new select list tables/models in this new database.
    FK data is also inserted below using get_or_create, but sometimes it's
    required to manually set additional values.
    """

    # SlTextTypeCategory
    for name in [
        'Document',
        'Literature'
    ]:
        models.SlTextTypeCategory.objects.create(name=name)

    # SlTextCorpus
    for name in [
        'Bamiyan Papers',
        'Firuzkuh Papers'
    ]:
        models.SlTextCorpus.objects.create(name=name)

    # SlTextType
    for obj in [
        {
            'name': 'Administrative',
            'category': models.SlTextTypeCategory.objects.get(name='Document')
        },
        {
            'name': 'Legal',
            'category': models.SlTextTypeCategory.objects.get(name='Document')
        },
        {
            'name': 'Letter',
            'category': models.SlTextTypeCategory.objects.get(name='Document')
        },
        {
            'name': 'List or table',
            'category': models.SlTextTypeCategory.objects.get(name='Document')
        },
        {
            'name': 'Literary text',
            'category': models.SlTextTypeCategory.objects.get(name='Literature')
        },
        {
            'name': 'Paraliterary',
            'category': models.SlTextTypeCategory.objects.get(name='Literature')
        }
    ]:
        models.SlTextType.objects.create(**obj)

    # SlTextSubjectLegalTransactions
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
        models.SlTextSubjectLegalTransactions.objects.create(name=name)

    # SlTextSubjectAdministrativeInternalCorrespondence
    for name in [
        'Missives to the field',
        'Informational note to the field',
        'Requests',
        'Missives for action'
    ]:
        models.SlTextSubjectAdministrativeInternalCorrespondence.objects.create(name=name)

    # SlTextSubjectAdministrativeTaxReceipts
    for name in [
        'TODO',
    ]:
        models.SlTextSubjectAdministrativeTaxReceipts.objects.create(name=name)

    # SlTextSubjectAdministrativeListsAndAccounting
    for name in [
        'TODO',
    ]:
        models.SlTextSubjectAdministrativeListsAndAccounting.objects.create(name=name)

    # SlTextSubjectLandMeasurementUnits
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
        models.SlTextSubjectLandMeasurementUnits.objects.create(name=name)

    # SlTextSubjectPeopleAndProcessesAdmin
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
        models.SlTextSubjectPeopleAndProcessesAdmin.objects.create(name=name)

    # SlTextSubjectPeopleAndProcessesLegal
    for name in [
        'Qāḍī',
        'Faqīh',
        'Muḥtasib'
    ]:
        models.SlTextSubjectPeopleAndProcessesLegal.objects.create(name=name)

    # SlTextSubjectDocumentation
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
        models.SlTextSubjectDocumentation.objects.create(name=name)

    # SlTextSubjectGeographicAdministrativeUnits
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
        models.SlTextSubjectGeographicAdministrativeUnits.objects.create(name=name)

    # SlTextSubjectLegalAndAdministrativeStockPhrases
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
        models.SlTextSubjectLegalAndAdministrativeStockPhrases.objects.create(name=name)

    # SlTextSubjectFinanceAndAccountancyPhrases
    for name in [
        'Tafṣīl (itemisation)',
        'Wajh/wujūh (in account/payment of)',
        'Bāqī (remainder)',
        'Wām (-I lāzim) (loan)'
    ]:
        models.SlTextSubjectFinanceAndAccountancyPhrases.objects.create(name=name)

    # SlTextSubjectAgriculturalProduce
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
        models.SlTextSubjectAgriculturalProduce.objects.create(name=name)

    # SlTextSubjectCurrenciesAndDenominations
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
        models.SlTextSubjectCurrenciesAndDenominations.objects.create(name=name)

    # SlTextSubjectMarkings
    for name in [
        'Oblique stroke (check mark)',
        'Jaʾiza (cipher)',
        'Taṣnīf (half-amount stroke above written out number)',
        'Column format',
        'Siyāq (accountants’ abbreviations of numbers)',
    ]:
        models.SlTextSubjectMarkings.objects.create(name=name)

    # SlTextSubjectReligion
    for name in [
        'Temple',
        'Mosque',
        'Church',
        'God(s)',
        'Fatwa/istiftāʿ',
        'Rituals'
    ]:
        models.SlTextSubjectReligion.objects.create(name=name)

    # SlTextSubjectToponym
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
        models.SlTextSubjectToponym.objects.create(name=name)

    # SlTextScript
    for name in [
        'Arabic',
        'Hebrew',
        'Greek-based',
        'Ancient Pahlavi'
    ]:
        models.SlTextScript.objects.create(name=name)

    # SlTextLanguage
    for obj in [
        {
            'name': 'Arabic',
            'script': models.SlTextScript.objects.get(name='Arabic')
        },
        {
            'name': 'Bactrian',
            'script': models.SlTextScript.objects.get(name='Greek-based')
        },
        {
            'name': 'Judeo-Persian',
            'script': models.SlTextScript.objects.get(name='Hebrew')
        },
        {
            'name': 'Middle Persian',
            'script': models.SlTextScript.objects.get(name='Ancient Pahlavi')
        },
        {
            'name': 'New Persian',
            'script': models.SlTextScript.objects.get(name='Arabic')
        },
    ]:
        models.SlTextLanguage.objects.create(**obj)

    # SlTranslationLanguage
    for name in [
        'English',
        'French'
    ]:
        models.SlTranslationLanguage.objects.create(name=name)

    # SlTextWritingSupport
    for name in [
        'paper',
        'ostraca',
        'parchment',
        'linen',
        'clay (bullae)',
        'seals',
        'stone (graves)',
    ]:
        models.SlTextWritingSupport.objects.create(name=name)

    # SlPublicationStatement
    models.SlPublicationStatement.objects.create(
        name='This text is published and distributed online by the Invisible East project, University of Oxford.'
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

    # SlM2MTextToTextRelationshipType
    for name in [
        'part of same document',
    ]:
        models.SlM2MTextToTextRelationshipType.objects.create(name=name)

    # SlTextClassification
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
        models.SlTextClassification.objects.create(**obj)

    # SlTextFolioSide
    for name in [
        'recto',
        'verso'
    ]:
        models.SlTextFolioSide.objects.create(name=name)

    # SlTextFolioOpen
    for name in [
        'open',
        'closed'
    ]:
        models.SlTextFolioOpen.objects.create(name=name)

    # SlTextFolioAnnotationType
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
        models.SlTextFolioAnnotationType.objects.create(name=name)

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


def insert_data_texts(apps, schema_editor):
    """
    Inserts data into the Text model
    """

    # User accounts used below
    account_ed = account_models.User.objects.get(email="edward.shawe-taylor@wolfson.ox.ac.uk")
    account_cat = account_models.User.objects.get(email="catherinemcnally@comcast.net")

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
                # E.g. Text (parent) comes before TextPerson (child)
                # Optional fields must be exception handled in case value is None or element doesn't exist in XML

                # Create Text object
                text_obj = models.Text()

                # shelfmark
                try:
                    text_obj.shelfmark = ms_desc.find('msIdentifier/idno[@type="shelfmark"]').text
                except AttributeError:
                    pass
                # collection
                try:
                    collection = ms_desc.find('msIdentifier/institution').text
                    text_obj.collection = models.SlTextCollection.objects.get_or_create(name=collection)[0]
                except AttributeError:
                    pass
                # primary language
                # Gets this from the filepath of the XML file (the last dir in root)
                # (Choices: Arabic, New Persian, Bactrian)
                primary_language = root.split('/')[-1]
                text_obj.primary_language = models.SlTextLanguage.objects.get(name=primary_language)
                # id_khan
                try:
                    text_obj.id_khan = ms_desc.find('msIdentifier/idno[@type="Khan"]').text
                except AttributeError:
                    pass
                # id_nicholas_simms_williams
                try:
                    text_obj.id_nicholas_simms_williams = ms_desc.find('msIdentifier/idno[@type="NSW"]').text
                except AttributeError:
                    pass
                # country
                try:
                    country = ms_desc.find('msIdentifier/country').text
                    text_obj.country = models.SlCountry.objects.get_or_create(name=country)[0]
                except AttributeError:
                    pass
                # description
                text_obj.description = '\n\n'.join(
                    [description.text for description in profile_desc.findall('particDesc/p')]
                )
                # type
                text_type = profile_desc.findall('textClass/keywords/term')[0].text
                text_obj.type = models.SlTextType.objects.get_or_create(name=text_type)[0]
                # correspondence
                correspondence = corresp_action.attrib['type']
                text_obj.correspondence = models.SlTextCorrespondence.objects.get_or_create(name=correspondence)[0]

                # Publication data, stored in separate <p> elements within publicationStmt
                pub_start_original = 'Originally published in: '
                pub_start_republished = 'The text was later republished in '
                for publication_p in file_desc.findall('publicationStmt/p'):
                    # publication_statement_original
                    if publication_p.text.startswith(pub_start_original):
                        text_obj.publication_statement_original = publication_p.text.replace(pub_start_original, '')
                    # publication_statement_republished
                    elif publication_p.text.startswith(pub_start_republished):
                        text_obj.publication_statement_republished = publication_p.text.replace(pub_start_republished, '')
                    # publication_statement
                    else:
                        text_obj.publication_statement = models.SlPublicationStatement.objects.get_or_create(name=publication_p.text)[0]

                # writing_support
                writing_support = ms_desc.find('physDesc/objectDesc/supportDesc').attrib['material']
                text_obj.writing_support = models.SlTextWritingSupport.objects.get_or_create(name=writing_support)[0]
                # writing_support_details
                # Includes tags within e.g. "blah blah <material>blah</material> blah blah" so itertext() will remove the tags
                text_obj.writing_support_details = ''.join(ms_desc.find('physDesc/objectDesc/supportDesc/support/p').itertext())

                # Dimensions
                try:
                    # dimensions_unit
                    dimensions_unit = dimensions.find('height').attrib['unit']
                    text_obj.dimensions_unit = models.SlUnitOfMeasurement.objects.get_or_create(name=dimensions_unit)[0]
                    # dimensions_height
                    text_obj.dimensions_height = dimensions.find('height').text
                    # dimensions_width
                    text_obj.dimensions_width = dimensions.find('width').text
                except AttributeError:
                    pass

                # fold_lines
                try:
                    # Join multiple <p> tag text into single string, separated with new lines
                    fold_lines_count_details = '\n\n'.join(
                        [flcd.text for flcd in ms_desc.findall('physDesc/objectDesc/layoutDesc/p')]
                    )
                    text_obj.fold_lines_count_details = fold_lines_count_details
                    # Get all numbers from the details string and add them together to likely give the total count
                    fold_lines_count_numbers = re.findall(r'\d+', fold_lines_count_details)
                    text_obj.fold_lines_count_total = sum(map(int, fold_lines_count_numbers))
                except AttributeError:
                    pass

                # physical_additional_details
                try:
                    # Many were empty strings with just lots of whitespace
                    physical_additional_details = ms_desc.find('physDesc/additions').text.strip()
                    # Set empty string values to be null
                    if not len(physical_additional_details):
                        physical_additional_details = None
                    text_obj.physical_additional_details = physical_additional_details
                except AttributeError:
                    pass
 
                # place
                try:
                    text_obj.place = corresp_action.find('placeName').text
                except AttributeError:
                    pass

                # meta_created_by and admin_principal_data_entry_person
                try:
                    meta_created_by = None
                    admin_principal_data_entry_person = None
                    # Ed
                    if title_stmt.find('respStmt[@id="EST"]', prefix_map):
                        meta_created_by = account_ed
                        admin_principal_data_entry_person = account_ed
                    # Cat
                    elif title_stmt.find('respStmt[@id="CM"]'):
                        meta_created_by = account_cat
                        admin_principal_data_entry_person = account_cat
                    if meta_created_by:
                        text_obj.meta_created_by = meta_created_by
                    if admin_principal_data_entry_person:
                        text_obj.admin_principal_data_entry_person = admin_principal_data_entry_person
                except AttributeError:
                    pass
                # meta_created_by - Cat

                # Save Text object in db
                text_obj.save()

                # Once Text object is saved in db we can add related data,
                # e.g. reverse FK objects and M2M relationships

                # Reverse FK objects:

                # PersonInText
                for person in corresp_action.findall('persName'):
                    models.PersonInText.objects.create(
                        text=text_obj,
                        person_role_in_text=models.SlPersonInTextRole.objects.get_or_create(name=person.attrib['type'])[0],
                        person=models.Person.objects.get_or_create(name=person.text)[0]
                    )

                # TextDate
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
                    models.TextDate.objects.create(
                        text=text_obj,
                        calendar=models.SlCalendar.objects.get_or_create(name=calendar)[0],
                        date=date_when,
                        date_not_before=date_not_before,
                        date_not_after=date_not_after,
                        date_text=date_text
                    )

                # Text Folios and Lines
                # Loop through original (i.e. transcription) texts
                for folio_div in body.findall('div[@type="original"]'):

                    # Check that same amount of pb as there are ab,
                    # as below code relies on there being a matching ab for each pb
                    pb_count = len(folio_div.findall('pb'))
                    ab_count = len(folio_div.findall('ab'))
                    if pb_count != ab_count:
                        print(f'WARNING: pb count ({pb_count}) != ab count ({ab_count}):', input_file)

                    # TextFolio
                    for folio_index, folio in enumerate(folio_div.findall('pb')):

                        # Side (e.g. recto or verso)
                        side_code = folio.attrib['id'].rsplit('-', 1)[-1]
                        if 'v' in side_code:
                            side_name = 'verso'
                        else:
                            side_name = 'recto'
                        side = models.SlTextFolioSide.objects.get(name=side_name) if side_name else None

                        # Open state (e.g. open or closed)
                        try:
                            open_state = models.SlTextFolioOpen.objects.filter(name=folio_div.attrib['subtype']).first()
                        except KeyError:
                            open_state = None

                        # Create the TextFolio object
                        folio_obj = models.TextFolio.objects.create(
                            text=text_obj,
                            side=side,
                            open_state=open_state
                        )

                        # Transcription
                        folio_content = folio_div.findall('ab')[folio_index]
                        folio_transcription_id = folio_content.attrib['id']
                        folio_transcription_lines = folio_content.findall('lb')
                        # Build HTML for transcription text
                        folio_obj.transcription = folio_lines_html(folio_transcription_lines)

                        # Translation
                        # Get the matching translation block
                        folio_translation_id = '_tr-'.join(folio_transcription_id.rsplit('_', 1))
                        folio_translation = body.find(f'div[@type="translation"]/ab[@id="{folio_translation_id}"]')
                        # Many translations don't have an ID provided (human error in XML input)
                        # but only have 1 <ab> so just use the first (and only) translation <ab>
                        if folio_translation is None:
                            folio_translation = body.findall(f'div[@type="translation"]/ab')[0]
                        # If a valid matching translation has been found, add it
                        if folio_translation is not None:
                            folio_translation_lines = folio_translation.findall('lb')
                            if len(folio_translation_lines):
                                folio_obj.translation = folio_lines_html(folio_translation_lines)
                        else:
                            print(f'No matching translation found for this transcription: {folio_transcription_id}')

                        # Save the folio object once the transcription + translation data has been added
                        folio_obj.save()

                # M2M relationships
                # (some only have 1 instance in XML but field is M2M for future flexibility):

                # toponyms (place/location)
                try:
                    toponym = profile_desc.findall('textClass/keywords/term[@type="location"]')[0].text
                    text_obj.toponyms.add(
                        models.SlTextSubjectToponym.objects.get_or_create(name=toponym)[0]
                    )
                except (AttributeError, IndexError):
                    pass

                # funders
                funder = title_stmt.find('funder').text
                text_obj.funders.add(
                    models.SlFunder.objects.get_or_create(name=funder)[0]
                )


def insert_data_texts_fk(apps, schema_editor):
    """
    Inserts data for foreign key fields in the Text model
    """

    with open(os.path.join(PATH_OLD_DATA, "data_texts_fk.txt"), 'r') as file:
        set_related_values(file, models.Text, 'fk')


def insert_data_texts_m2m(apps, schema_editor):
    """
    Inserts data for many to many fields in the Text model
    """

    with open(os.path.join(PATH_OLD_DATA, "data_texts_m2m.txt"), 'r') as file:
        set_related_values(file, models.Text, 'm2m')


def insert_data_textimages(apps, schema_editor):
    """
    Inserts data into the Text Image model
    """

    # Delete thumbnail directory and the existing images in them, to start fresh
    try:
        shutil.rmtree(os.path.join(settings.BASE_DIR, f"media/palaeography/textimages-thumbnails"))
    except FileNotFoundError:
        pass  # it's ok if can't find dir, will just skip it

    with open(os.path.join(PATH_OLD_DATA, "data_textimages.txt"), 'r') as file:
        for object in literal_eval(file.read()):

            # Tidy custom_instructions data
            object['custom_instructions'] = strip_html_tags(object['custom_instructions'])

            # Save object
            models.TextImage.objects.create(**object)


def insert_data_textimageparts(apps, schema_editor):
    """
    Inserts data into the Text Image Part model
    """

    with open(os.path.join(PATH_OLD_DATA, "data_textimageparts.txt"), 'r') as file:
        for object in literal_eval(file.read()):
            models.TextImagePart.objects.create(**object)


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0001_initial')
    ]

    operations = [
        migrations.RunPython(insert_data_select_list_models),
        migrations.RunPython(insert_data_texts)
    ]
