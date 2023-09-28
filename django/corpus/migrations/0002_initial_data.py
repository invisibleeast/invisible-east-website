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


def ordinal_number(n):
    """
    Return correct ordinal number (e.g. 1 -> 1st, 22 -> 22nd, 34 -> 34th, etc.)
    """
    return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


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

    # SlTextCorpus
    for name in [
        'Bamiyan Papers',
        'Firuzkuh Papers'
    ]:
        models.SlTextCorpus.objects.create(name=name)

    # SlTextTypeCategory
    for name in [
        'Document',
        'Literature'
    ]:
        models.SlTextTypeCategory.objects.create(name=name)

    # SlTextType
    category_document = models.SlTextTypeCategory.objects.get(name='Document')
    category_literature = models.SlTextTypeCategory.objects.get(name='Literature')
    for obj in [
        {
            'name': 'Administrative',
            'category': category_document
        },
        {
            'name': 'Legal',
            'category': category_document
        },
        {
            'name': 'Letter',
            'category': category_document
        },
        {
            'name': 'List or table',
            'category': category_document
        },
        {
            'name': 'Literary text',
            'category': category_literature
        },
        {
            'name': 'Paraliterary',
            'category': category_literature
        }
    ]:
        models.SlTextType.objects.create(**obj)

    # SlTextDocumentSubtypeCategory
    for name in [
        'Administrative',
        'Legal'
    ]:
        models.SlTextDocumentSubtypeCategory.objects.create(name=name)

    # SlTextDocumentSubtype
    category_administrative = models.SlTextDocumentSubtypeCategory.objects.get(name='Administrative')
    category_legal = models.SlTextDocumentSubtypeCategory.objects.get(name='Legal')
    for obj in [
        # Administrative
        { 'name': 'Missives to the field', 'category': category_administrative },
        { 'name': 'Informational note to the field', 'category': category_administrative },
        { 'name': 'Requests', 'category': category_administrative },
        { 'name': 'Missives for action', 'category': category_administrative },
        { 'name': 'Tax receipts', 'category': category_administrative },
        { 'name': 'Lists and accounting', 'category': category_administrative },
        # Legal
        { 'name': 'Worship acts (ibādat)', 'category': category_legal },
        { 'name': 'Sale (bayʿ)', 'category': category_legal },
        { 'name': 'Rent-hire (ʿijāra)', 'category': category_legal },
        { 'name': 'Partnership (sharīk/shurāka)', 'category': category_legal },
        { 'name': 'Marriage (ʿaqd, nikāh)', 'category': category_legal },
        { 'name': 'Divorce (ṭalāq)', 'category': category_legal },
        { 'name': 'Loan (wām)/ Debt (dayn)', 'category': category_legal },
        { 'name': 'Amicable Settlement', 'category': category_legal },
        { 'name': 'Preemption', 'category': category_legal },
        { 'name': 'Power of attorney', 'category': category_legal },
        { 'name': 'Slavery and Manumission', 'category': category_legal },
        { 'name': 'Inheritance', 'category': category_legal },
        { 'name': 'Donation', 'category': category_legal },
        { 'name': 'Transfer of money (Ḥawāla)', 'category': category_legal },
        { 'name': 'Guarantee of liability (dark-I ḍamān)', 'category': category_legal },
        { 'name': 'Debt (Unknown origin)', 'category': category_legal },
        { 'name': 'Penal rules', 'category': category_legal },
        { 'name': 'Personal Status', 'category': category_legal },
        { 'name': 'Testimony', 'category': category_legal },
        { 'name': 'Litigation', 'category': category_legal },
    ]:
        models.SlTextDocumentSubtype.objects.create(**obj)

    # SlTextCentury
    # e.g. "4th Century CE, 5th Century CE, ... 21st Century CE"
    for object in range(4, 22):
        models.SlTextCentury(
            name=f'{ordinal_number(object)} Century CE',
            century_number=object
        ).save()

    # SlTextScript
    for obj in [
        {
            'name': 'Arabic',
            'is_written_right_to_left': True
        },
        {
            'name': 'Hebrew',
            'is_written_right_to_left': False
        },
        {
            'name': 'Greek-based',
            'is_written_right_to_left': False
        },
        {
            'name': 'Ancient Pahlavi',
            'is_written_right_to_left': False
        },
    ]:
        models.SlTextScript.objects.create(**obj)

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

    # SlTextFoldLinesAlignment
    for name in [
        'horizontal',
        'vertical',
        'vertical and horizontal',
    ]:
        models.SlTextFoldLinesAlignment.objects.create(name=name)

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
        'part of same text',
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

    # SlTextFolioTag and SlTextFolioTagCategory (multiple loops, one for each category)
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
        models.SlTextFolioTag.objects.create(
            name=name,
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Land measurement units')[0]
        )
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
        models.SlTextFolioTag.objects.create(
            name=name,
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='People and processes involved in public administration, tax, trade, and commerce')[0]
        )
    for name in [
        'Qāḍī',
        'Faqīh',
        'Muḥtasib'
    ]:
        models.SlTextFolioTag.objects.create(
            name=name,
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='People and processes involved in legal and judiciary system')[0]
        )
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
        models.SlTextFolioTag.objects.create(
            name=name,
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Documentations')[0]
        )
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
        models.SlTextFolioTag.objects.create(
            name=name,
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Geographic administrative units')[0]
        )
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
        models.SlTextFolioTag.objects.create(
            name=name,
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Legal and administrative stock phrases')[0]
        )
    for name in [
        'Tafṣīl (itemisation)',
        'Wajh/wujūh (in account/payment of)',
        'Bāqī (remainder)',
        'Wām (-I lāzim) (loan)'
    ]:
        models.SlTextFolioTag.objects.create(
            name=name,
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Finance and accountancy phrases')[0]
        )
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
        models.SlTextFolioTag.objects.create(
            name=name,
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Agricultural produce')[0]
        )
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
        models.SlTextFolioTag.objects.create(
            name=name,
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Currencies and denominations')[0]
        )
    for name in [
        'Oblique stroke (check mark)',
        'Jaʾiza (cipher)',
        'Taṣnīf (half-amount stroke above written out number)',
        'Column format',
        'Siyāq (accountants’ abbreviations of numbers)',
    ]:
        models.SlTextFolioTag.objects.create(
            name=name,
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Markings')[0]
        )
    for name in [
        'Temple',
        'Mosque',
        'Church',
        'God(s)',
        'Fatwa/istiftāʿ',
        'Rituals'
    ]:
        models.SlTextFolioTag.objects.create(
            name=name,
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Religions')[0]
        )
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
    ]:
        models.SlTextFolioTag.objects.create(
            name=name,
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Toponyms')[0]
        )

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
    account_ed = account_models.User.objects.get(email="edward.shawe-taylor@ames.ox.ac.uk")
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
                # century
                try:
                    gregorian = corresp_action.findall('date[@calendar="#Gregorian"]')[0]
                    century = None
                    if 'when' in gregorian.attrib:
                        century = int(gregorian.attrib['when'][:2]) + 1
                    elif 'notAfter' in gregorian.attrib:
                        century = int(gregorian.attrib['notAfter'][:2]) + 1
                    elif 'notBefore' in gregorian.attrib:
                        century = int(gregorian.attrib['notBefore'][:2]) + 1
                    if century:
                        text_obj.century = models.SlTextCentury.objects.get(century_number=century)
                except IndexError:
                    pass
                # summary_of_content
                text_obj.summary_of_content = '\n\n'.join(
                    [summary_of_content.text for summary_of_content in profile_desc.findall('particDesc/p')]
                )
                # type
                text_type = profile_desc.findall('textClass/keywords/term')[0].text
                text_obj.type = models.SlTextType.objects.get_or_create(name=text_type)[0]

                # writing_support
                writing_support = ms_desc.find('physDesc/objectDesc/supportDesc').attrib['material']
                text_obj.writing_support = models.SlTextWritingSupport.objects.get_or_create(name=writing_support)[0]
                # writing_support_details_additional
                # Includes tags within e.g. "blah blah <material>blah</material> blah blah" so itertext() will remove the tags
                text_obj.writing_support_details_additional = ''.join(ms_desc.find('physDesc/objectDesc/supportDesc/support/p').itertext())

                # Dimensions
                try:
                    dimensions_unit = dimensions.find('height').attrib['unit']
                    # dimensions_height
                    dimensions_height = dimensions.find('height').text
                    if dimensions_height and len(dimensions_height):
                        # Convert mm to cm
                        dimensions_height = int(dimensions_height) / 10 if dimensions_unit == 'mm' else dimensions_height
                        text_obj.dimensions_height = dimensions_height
                    # dimensions_width
                    dimensions_width = dimensions.find('width').text
                    if dimensions_width and len(dimensions_width):
                        # Convert mm to cm
                        dimensions_width = int(dimensions_width) / 10 if dimensions_unit == 'mm' else dimensions_width
                        text_obj.dimensions_width = dimensions_width
                except AttributeError:
                    pass

                # fold_lines_details
                try:
                    # Join multiple <p> tag text into single string, separated with new lines
                    fold_lines_details = '\n\n'.join(
                        [flcd.text for flcd in ms_desc.findall('physDesc/objectDesc/layoutDesc/p')]
                    )
                    text_obj.fold_lines_details = fold_lines_details
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
                    # Cat
                    elif title_stmt.find('respStmt[@id="CM"]'):
                        meta_created_by = account_cat
                    # Data entry person set to Ed, as Cat leaving project
                    admin_principal_data_entry_person = account_ed
                    if meta_created_by:
                        text_obj.meta_created_by = meta_created_by
                    if admin_principal_data_entry_person:
                        text_obj.admin_principal_data_entry_person = admin_principal_data_entry_person
                except AttributeError:
                    pass

                # admin_classification
                if primary_language == 'Bactrian':
                    text_obj.admin_classification = models.SlTextClassification.objects.get(name='Gold')

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

                # Text Related Publications, stored in separate <p> elements within publicationStmt
                for publication_p in file_desc.findall('publicationStmt/p'):
                    # Ignore 'Invisible East' publication statements
                    if 'Invisible East' not in publication_p.text:

                        # Remove unwanted text from statement
                        publication_text = publication_p.text
                        publication_text = publication_text.replace('Originally published in: ', '')
                        publication_text = publication_text.replace('The document was later republished in ', '')

                        # Split pages from publication text
                        if ' Pages ' in publication_text:
                            publication_text, pages = publication_text.split(' Pages ')
                            pages = pages.strip().replace('.', '')

                        # Create the object
                        models.TextRelatedPublication.objects.create(
                            text=text_obj,
                            publication=models.SlTextPublication.objects.get_or_create(name=publication_text)[0],
                            pages=pages
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
                        date_range_start = date.attrib['notBefore']
                    except KeyError:
                        date_range_start = None
                    try:
                        date_range_end = date.attrib['notAfter']
                    except KeyError:
                        date_range_end = None
                    try:
                        date_text = date.text
                    except AttributeError:
                        date_text = None
                    # Create the object
                    models.TextDate.objects.create(
                        text=text_obj,
                        calendar=models.SlCalendar.objects.get_or_create(name=calendar)[0],
                        date=date_when,
                        date_range_start=date_range_start,
                        date_range_end=date_range_end,
                        date_text=date_text
                    )

                # Text Folios
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
                        folio_transcription_text_lines = folio_content.findall('lb')
                        # Build HTML for transcription text
                        folio_obj.transcription = folio_lines_html(folio_transcription_text_lines)

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
                            folio_translation_text_lines = folio_translation.findall('lb')
                            if len(folio_translation_text_lines):
                                folio_obj.translation = folio_lines_html(folio_translation_text_lines)
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
                        models.SlTextTagToponym.objects.get_or_create(name=toponym)[0]
                    )
                except (AttributeError, IndexError):
                    pass


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
