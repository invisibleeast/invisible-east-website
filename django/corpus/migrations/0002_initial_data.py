import xml.etree.ElementTree as ET
from pathlib import Path
from django.conf import settings
from django.db import migrations
from corpus import models
from ast import literal_eval
from html.parser import HTMLParser
from io import StringIO
from account import models as account_models
import os


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

    # SlTextGregorianCentury
    # e.g. "4th Century CE, 5th Century CE, ... 21st Century CE"
    for object in range(4, 22):
        models.SlTextGregorianCentury(
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
        'Tafṣīl (itemisation)',
        'Wajh/wujūh (in account/payment of)',
        'Bāqī (remainder)',
        'Wām (-I lāzim) (loan)',

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
        'Taxes: Jizya',

        'Qāḍī',
        'Faqīh',
        'Muḥtasib',

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
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Administrative, Military and Legal Titles, Offices and Processes')[0]
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
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Agricultural Terms')[0]
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
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Currencies and Denominations')[0]
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
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Documentation Terms')[0]
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
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Geographic Administrative Units')[0]
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
            category=models.SlTextFolioTagCategory.objects.get_or_create(name='Measurement Units')[0]
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

    # SlCalendar
    for obj in [
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

    # SlSealDescription
    for name in [
        'bearded',
        'cross',
        'griffin',
        'bird',
        'inscription',
        'fingernail',
        'camel',
        'stag',
        'boarbeardless',
        'standing',
        'sitting',
        'hunt',
        'diadem',
        'winged',
        'serpent',
        'hydra',
        'swastika',
        'tamga',
        'trident',
        'peacock',
        'headdress',
        'inscription',
        'pearl',
        'necklace',
        'earring(s)',
        'lion',
        'bull',
        'hare',
        'wolf'
    ]:
        models.SlSealDescription.objects.create(name=name)

    # SlSealColour
    for name in [
        'black',
        'brown',
        'dun',
        'grey',
        'orange',
        'pink',
        'red',
        'tan',
        'white',
        'yellow',
    ]:
        models.SlSealColour.objects.create(name=name)

    # SlSealImprint
    for name in [
        'complete male figure',
        'complete female figure',
        'animals',
        'busts',
        'fingernails',
        'inscriptions',
        'symbols',
        'indeterminate'
    ]:
        models.SlSealImprint.objects.create(name=name)


def insert_data_toponyms(apps, schema_editor):
    """
    Inserts data into the SlTextToponym model
    """

    toponyms = [
        ["Toponym", "Other Attested Forms (one place, different writings)", "Alternative Readings (one place, different readings)", "Latitude", "Longitude", "Geonames link", "Comments"],
        ["Āhangarān", "", "", "34.80907", "67.91612", "http://www.geonames.org/1149302/dahan-e-ahangaran.html ", ""],
        ["ʿAjagak", "Hajigak (modern)", "", "34.0614", "67.31196", "http://www.geonames.org/1140359/hajigak.html", "Present-day Ḥājjigak? (34.0614, 67.31196; http://www.geonames.org/1140359/hajigak.html)"],
        ["Amber", "", "", "", "", "", ""],
        ["Andar", "", "Anwar", "", "", "", "Same place as Anwar-gird?"],
        ["Andarāba", "", "Andarāb", "35.62405", "69.17861", "http://www.geonames.org/7052857/andarab.html ", ""],
        ["Angār", "", "", "35.39726", "68.33866", "http://www.geonames.org/1148653/angar.html ", ""],
        ["Anwar-gird", "", "Andar-gird", "", "", "", "Same place as Anwar?"],
        ["Arsaf", "", "", "", "", "", "Doubtful reading"],
        ["Asp-qūl", "", "", "", "", "", ""],
        ["Azraw", "", "", "34.17355", "69.64573", "http://www.geonames.org/1147851/hukumati-azrah.html ", ""],
        ["Balkh", "", "", "36.75635", "66.8972", "http://www.geonames.org/1147290/balkh.html ", ""],
        ["Bāmiyān", "", "", "34.82156", "67.82734", "http://www.geonames.org/1147242/bamyan.html ", ""],
        ["Bandālīzh", "Bandānlīzh, Bandālīch, Bandān Līch, Band-i ʿAlī (?, modern)", "Band-i Alīzh, Band-i Ilīzh", "34.52397", "65.4381", "http://www.geonames.org/1147204/band-e-ali.html", "Present-day Band-i ʿAlī? (34.52397, 65.4381; http://www.geonames.org/1147204/band-e-ali.html)"],
        ["Band-i Khāsh", "Darra-yi Khāsh (?, modern)", "", "36.90561", "70.75941", "http://www.geonames.org/1136859/darah-ye-khash.html ", "A settlement by the name of Darra-yi Khāsh is situated in Badakhshān province (36.90561, 70.75941; http://www.geonames.org/1136859/darah-ye-khash.html ). However, it is unlikely that it is the same place mentioned in this document."],
        ["Barāslīzh", "", "", "", "", "", "Written ىراسلیژ. The lack of diacritics provided further reading possibilities."],
        ["Bardīz", "", "", "35.02256", "65.37386", "https://www.geonames.org/1147001/bardayz.html", ""],
        ["Būtiyān", "Botiyan (modern), Botyan (modern)", "", "34.92251", "68.36194", "http://www.geonames.org/1455442/dahan-e-botyan.html ", ""],
        ["Chākarī", "Chākarī (modern)", "Chāgarī, Jākar, Jāgarī", "35.99866", "69.64595", "https://www.geonames.org/1145604/chakari.html", "A settlement called Chākarī is situated in Baghlān province (35.99866, 69.64595; https://www.geonames.org/1145604/chakari.html). The connection to Jāghurī in Ghazni province seems less likely (33.14341, 67.46384; http://www.geonames.org/7052958/jaghuri.html)."],
        ["Chawqānī", "", "Jawqānī", "35.60195", "68.90153", "http://www.geonames.org/1469969/chowgani.html ", ""],
        ["Dāmam", "", "", "", "", "", ""],
        ["Dar Ṭakh", "Takht (?, modern)", "", "34.99825", "65.77522", "http://www.geonames.org/1123188/takht.html", "Present-day Takht? (34.99825, 65.77522; http://www.geonames.org/1123188/takht.html )"],
        ["Dāwar", "", "", "", "", "", ""],
        ["Dupawi", "", "", "", "", "", ""],
        ["Durustī", "", "", "35.01667", "69.31667", "http://www.geonames.org/1142828/dorosti.html ", ""],
        ["Farāmān", "", "Warāman, Wazāmān", "", "", "", ""],
        ["Firūzān", "", "", "", "", "", ""],
        ["Fīrūzkūh", "Jām (modern)", "", "34.39642", "64.51687", "http://www.geonames.org/1460029/pay-monar.html ", ""],
        ["Funduqistān", "Fondukistan (modern)", "", "34.98978", "68.90007", "https://www.geonames.org/9199798/fondukistan.html", ""],
        ["Garokan", "", "", "", "", "", ""],
        ["Gaz", "", "", "", "", "", ""],
        ["Ghandamīn", "Ghalmin (?, modern)", "", "34.8701", "65.31396", "http://www.geonames.org/1144000/darah-ye-ghalmin.html", "Present-day Ghalmīn? (34.8701, 65.31396;http://www.geonames.org/1144000/darah-ye-ghalmin.html)"],
        ["Ghandaq", "Ghandak (modern)", "", "34.99267", "68.01635", "http://www.geonames.org/1141452/ghandak.html", "Present-day Ghandak? (34.99267, 68.01635; http://www.geonames.org/1141452/ghandak.html)"],
        ["Ghandar", "", "", "", "", "", ""],
        ["Ghārmīkh", "", "Ghārminj, Ghārmikh", "", "", "", ""],
        ["Ghūr Karūd", "", "Ghūr Garūd", "", "", "", ""],
        ["Ghūrwand", "", "", "35.01039", "68.78769", "http://www.geonames.org/7054044/siyahgird-ghorband.html ", ""],
        ["Golg", "", "", "", "", "", ""],
        ["Gozgan", "", "", "", "", "", ""],
        ["Īsh", "", "Līzh", "", "", "", "Appears as a nisba (Īshī, ایشی or Līzhī, لیژی). The form Līzh (or Līch) is common in toponyms in Afghanistan, while the form Ēsh/Īsh is attested only in two places in Badakhshān, which is remote from Bamiyan: 1. Dasht-i Ēsh (37.92158, 70.53517; http://www.geonames.org/7096560/dasht-e-esh.html) 2. Kham-i Īsh Darra (37.98354, 70.47729; http://www.geonames.org/1467272/kham-e-ish-darah.html)"],
        ["Istīw", "Istīb", "", "", "", "", ""],
        ["Izīr", "", "", "34.78693", "65.35062", "https://www.geonames.org/1471119/izir.html", ""],
        ["Jawlāh", "", "Jūlāh, Chawlāh, Chūlāh", "34.800661", "68.145964", "", ""],
        ["Kadagstan", "", "", "", "", "", ""],
        ["Kadūr", "", "", "", "", "", ""],
        ["Kāfshān", "Kafshān", "Kāwshān, Kāf Shān", "35.0636", "69.06669", "http://www.geonames.org/1423313/dahan-e-kafshan.html ", "See also Haim 2019: 74-75"],
        ["Kāliyūn", "", "Kālyūn", "", "", "", ""],
        ["Karūd", "", "", "", "", "", ""],
        ["Kasūf", "", "", "", "", "", ""],
        ["Kawrīj", "", "Kūrīj", "", "", "", "Written کورىج. The lack of diacritics provided further reading possibilities."],
        ["Khāy", "", "", "35.02931", "65.20355", "http://www.geonames.org/1425662/kotal-e-khay.html ", ""],
        ["Khīsh", "", "", "34.71135", "68.37493", "http://www.geonames.org/1455529/qol-e-khesh.html ", ""],
        ["Khustgān", "", "", "35.39408", "68.32742", "http://www.geonames.org/1428820/khostgan.html ", ""],
        ["Kiriyān", "", "Kadyān, Karyān", "35.94433", "69.53873", "http://www.geonames.org/1143466/deh-e-kirian.html ", ""],
        ["Lāmtak", "", "", "", "", "", ""],
        ["Lizag", "", "", "", "", "", ""],
        ["Lizg", "", "", "", "", "", ""],
        ["Madr", "", "", "", "", "", ""],
        ["Miyān Shahr", "", "", "36.02024", "69.52179", "https://www.geonames.org/1132575/mian-shahr.html", "Present-day Miyān Shahr in Khust-o Firing district of Baghlān province? (36.02024, 69.52179; https://www.geonames.org/1132575/mian-shahr.html). Two settlements are also called Miyān Shahr (in Takhār and Badakhshān). However, it is less likely that they should identified with the toponym appearing in the Bamiyan Papers. Another possibility is that Miyān Shar is in fact the town of Maydān Shahr in present-day Wardak province (34.39561, 68.86618; https://www.geonames.org/1456960/maydanshakhr.html). "],
        ["Murghāb", "", "", "34.96944", "65.62178", "http://www.geonames.org/1132772/murghab.html ", "Appears as part of the toponym Ṭāq-i Murghāb"],
        ["Nala", "", "", "", "", "", ""],
        ["Nāy", "Nay Qalʿa (?, modern)", "", "34.81138", "68.18428", "http://www.geonames.org/1455934/nay-qal-ah.html", "Present-day Nay Qalʿa? (34.81138, 68.18428; http://www.geonames.org/1455934/nay-qal-ah.html). In Bāmiyān and its surroundings, there are many names with suffixes or prefixes of Nay and Nāy."],
        ["Nayak", "", "Himak, Nimak", "34.7295", "66.95501", "http://www.geonames.org/1457791/nayak.html ", ""],
        ["Nīlinj", "Nilinj (modern)", "", "35.07262", "65.14814", "http://www.geonames.org/1132408/nalinj.html ", ""],
        ["Pūza-yi ʿUlyā", "Pūza-yi Līch-i ʿUlyā (?, modern)", "", "34.53323", "65.32883", "http://www.geonames.org/1130299/pozah-ye-lich-e-ulya.html", "Present-day Pūza-yi Līch-i ʿUlyā? (34.53323, 65.32883; http://www.geonames.org/1130299/pozah-ye-lich-e-ulya.html)"],
        ["Rabanjī", "", "", "", "", "", "The lack of diacritics provided further reading possibilities."],
        ["Rāq", "Kūh-i Rāq", "", "35.73831", "66.21102", "https://www.geonames.org/1427015/koh-e-raq.html", "Near present-day Kūh-i Rāq? (35.73831, 66.21102; https://www.geonames.org/1427015/koh-e-raq.html)"],
        ["Rīw", "Riwah (?, modern)", "Zīr", "35.06529", "68.94578", "https://www.geonames.org/1128357/riwah.html", "Present-day Riwah (روه)? (35.06529, 68.94578; https://www.geonames.org/1128357/riwah.html)"],
        ["Rizm", "", "", "", "", "", ""],
        ["Rob", "", "", "", "", "", ""],
        ["Rubāṭ", "Āq Rabāṭ (?, modern)", "", "34.93505", "67.65657", "http://www.geonames.org/1148522/aq-rabat.html", "Present-day Aq Rubāṭ? (34.93505, 67.65657; http://www.geonames.org/1148522/aq-rabat.html). In Afghanistan, there are tens of places containing the form Rubāt."],
        ["Rubāṭ-i Miyān Shahr", "", "", "36.02024", "69.52179", "http://www.geonames.org/1132575/mian-shahr.html ", ""],
        ["Rubāṭiyān", "", "Ribāṭ Shār", "", "", "", "Rubātiyān may mean 'the people of Rubāṭ'. Therefore, the name of the village may be Rubāt."],
        ["Sabz Bahār", "", "", "", "", "", ""],
        ["Safī", "", "Saqī", "", "", "", ""],
        ["Sagnūl", "", "", "", "", "", "Probably the same place as sgnwl (סגנול) mentioned in archive of Yehuda ben Daniel (first half of the 11th century, Bamiyan)."],
        ["Sakūn", "", "", "", "", "", ""],
        ["Samangān", "", "", "", "", "", ""],
        ["Samingan", "", "Samangān", "", "", "", ""],
        ["Sandaran", "", "", "", "", "", ""],
        ["Sanga", "", "", "", "", "", ""],
        ["Sānī", "", "Shānī", "", "", "", "The lack of diacritics provided further reading possibilities."],
        ["Sar-i Āsiyā", "", "", "34.81279", "67.82151", "http://www.geonames.org/1457317/sar-asyab.html ", ""],
        ["Sarī Gudhar", "", "", "35.00749", "68.68418", "http://www.geonames.org/1126981/sar-guzar.html ", ""],
        ["Sar-i Khīsh", "Qūl-i Khīsh (?, modern)", "", "34.71135", "68.37493", "http://www.geonames.org/1455529/qol-e-khesh.html", "Present-day Qūl-i Khīsh? (34.71135, 68.37493; http://www.geonames.org/1455529/qol-e-khesh.html). See also Sims-Williams and Vaissière 2011: 40-41."],
        ["Shangaryān", "", "Shingiryān", "34.950112", "68.508819", "", ""],
        ["Shāristay", "Sharestay (modern)", "", "34.82953", "65.28906", "http://www.geonames.org/7537162/sharistay.html ", ""],
        ["Shawāniq", "", "", "", "", "", ""],
        ["Shawār", "", "", "", "", "", "Possibly related to šʾwrbhʾr (שאורבהאר) mentioned in archive of Yehuda ben Daniel (first half of the 11th century, Bamiyan)"],
        ["Shibārghū", "", "Sibārghū", "", "", "", ""],
        ["Skānj", "", "", "", "", "", ""],
        ["Sozargan", "", "", "", "", "", ""],
        ["Sparf", "Isparf (modern)", "", "35.0062", "65.80053", "http://www.geonames.org/1142382/darah-ye-isparf.html ", ""],
        ["Sū", "", "Shū, Safī, Saqī", "", "", "", ""],
        ["Suf", "Tagaw-e Suf (modern)", "Suq", "35.0266", "65.30474", "http://www.geonames.org/1123391/tagaw-e-suf.html", "Present-day Tagāb-i Suf? (35.0266, 65.30474; http://www.geonames.org/1123391/tagaw-e-suf.html)"],
        ["Surkh Dar", "", "", "34.848033", "67.758083", "", ""],
        ["Sūya", "Kūtal-i Ṣūba", "Shūya, Sūba", "34.67311", "67.95436", "http://www.geonames.org/1457381/kotal-e-sobah.html", "Present-day Kūtal-i Ṣūba (کوتل صوبه)? (34.67311, 67.95436; http://www.geonames.org/1457381/kotal-e-sobah.html)"],
        ["Tag Āb-i Kurgī", "Kurgin (?, modern)", "Tag Āb-i Kurgīn", "35.08905", "65.30647", "https://www.geonames.org/1135218/kurgin.html", "Present-day Kurgīn? (35.08905, 65.30647; https://www.geonames.org/1135218/kurgin.html)"],
        ["Tālīzh", "", "", "", "", "", ""],
        ["Ṭāq", "Tāgh, Ṭāq-i Murghāb, Tagaw-e Taq (modern)", "", "35.05164", "65.25941", "https://www.geonames.org/1123407/tagaw-e-taq.html ", ""],
        ["Tufandih", "Tukhundī (?, modern)", "", "35.16412", "64.74925", "https://www.geonames.org/1123130/takhundi-kuhnah.html", "Present-day Tukhundī? (35.16412, 64.74925; https://www.geonames.org/1123130/takhundi-kuhnah.html)"],
        ["Wak", "", "", "", "", "", ""],
        ["Warmiyās", "", "", "", "", "", ""],
        ["Warzīkh", "", "", "", "", "", ""],
        ["Wāshān", "", "Wānshān", "", "", "", "Probably the valley of Wānshān (drh wʾnšʾn, דרה ואנשאן), mentioned in archive of Yehuda ben Daniel (first half of the 11th century, Bamiyan)"],
        ["Wīlīzh", "", "Waylīzh", "", "", "", ""],
        ["Yaskarāgh", "", "", "", "", "", ""],
        ["Yaskin", "", "", "", "", "", ""],
        ["Yunavo (?)", "", "", "", "", "", ""],
        ["Zīr Damān", "", "Zīr-i Damān", "", "", "", ""],
        ["Zuwer", "", "", "", "", "", ""],
        ["رسحر مں (؟)", "", "", "", "", "", "The lack of diacritics prevents us from suggesting a plausible reading."]
    ]

    for toponym in toponyms:
        models.SlTextToponym.objects.create(
            name=toponym[0],
            other_attested_forms=toponym[1],
            alternative_readings=toponym[2],
            latitude=toponym[3],
            longitude=toponym[4],
            urls=toponym[5],
            notes=toponym[6],
        )


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

                # gregorian_date_... fields
                try:
                    gregorian_date = corresp_action.findall('date[@calendar="#Gregorian"]')[0]
                    gregorian_date_century = None
                    try:
                        text_obj.gregorian_date_text = gregorian_date.text
                    except AttributeError:
                        text_obj.gregorian_date_text = None
                    if 'when' in gregorian_date.attrib:
                        text_obj.gregorian_date_when = gregorian_date.attrib['when']
                        gregorian_date_century = int(gregorian_date.attrib['when'][:2]) + 1
                    if 'notBefore' in gregorian_date.attrib:
                        text_obj.gregorian_date_range_start = gregorian_date.attrib['notBefore']
                        gregorian_date_century = int(gregorian_date.attrib['notBefore'][:2]) + 1
                    if 'notAfter' in gregorian_date.attrib:
                        text_obj.gregorian_date_range_end = gregorian_date.attrib['notAfter']
                        gregorian_date_century = int(gregorian_date.attrib['notAfter'][:2]) + 1
                    if gregorian_date_century:
                        text_obj.gregorian_date_century = models.SlTextGregorianCentury.objects.get(century_number=gregorian_date_century)
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
                if primary_language in ['Bactrian', 'Arabic']:
                    text_obj.admin_classification = models.SlTextClassification.objects.get(name='Gold')
                elif primary_language == 'New Persian':
                    text_obj.admin_classification = models.SlTextClassification.objects.get(name='Bronze')

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
                    # Ignore 'Gregorian' calendar, as this is inserted directly within Text above
                    if calendar != 'Gregorian':
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
                            date_text=date_text,
                            date=date_when,
                            date_range_start=date_range_start,
                            date_range_end=date_range_end,
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


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0001_initial')
    ]

    operations = [
        migrations.RunPython(insert_data_select_list_models),
        migrations.RunPython(insert_data_toponyms),
        migrations.RunPython(insert_data_texts)
    ]
