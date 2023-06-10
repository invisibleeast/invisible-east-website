from django.db import models
from django.utils import timezone
from django.db.models.functions import Upper
from account.models import User


# Three main sections:
# 1. Reusable code
# 2. Select List Models
# 3. Main models


#
# 1. Reusable code
#


class SlAbstract(models.Model):
    """
    An abstract model for Select List models
    See: https://docs.djangoproject.com/en/4.0/topics/db/models/#abstract-base-classes
    """

    name = models.CharField(max_length=1000, blank=True, null=True, db_index=True)

    def __str__(self):
        return self.name if self.name and self.name != "" else f"#{self.id}"

    class Meta:
        abstract = True
        ordering = [Upper('name'), 'id']


#
# 2. Select List models (all inherit from above SlAbstract class, with some extending with additional fields, etc.)
#


class SlKeyword(SlAbstract):
    """
    A common word/phrase associated with a Document
    E.g. 'administration', 'receipt'
    """
    pass


class SlDocumentType(SlAbstract):
    """
    A type of Document
    E.g. 'legal', 'letter'
    """
    pass


class SlDocumentTypeLegalTransactions(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeAdministrativeInternalCorrespondence(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeAdministrativeTaxReceipts(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeAdministrativeListsAndAccounting(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeLandMeasurementUnits(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypePeopleAndProcessesAdmin(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypePeopleAndProcessesLegal(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeDocumentation(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeGeographicAdministrativeUnits(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeLegalAndAdministrativeStockPhrases(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeFinanceAndAccountancyPhrases(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeAgriculturalProduce(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeCurrenciesAndDenominations(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeMarkings(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeReligion(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeToponymBamiyan(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeToponymFiruzkuh(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeToponymPersianKhalili(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeToponymBactrian(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeToponymKhurasan(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentTypeToponymMiddlePersian(SlAbstract):
    """
    A Document type related field
    """
    pass


class SlDocumentWritingSupport(SlAbstract):
    """
    A type of Document
    E.g. 'paper', 'ostraca', 'parchment'
    """
    pass


class SlFunder(SlAbstract):
    """
    A research funder
    E.g. 'ERC'
    """
    name_full = models.CharField(max_length=100, blank=True, null=True)


class SlUnitOfMeasurement(SlAbstract):
    """
    A unit of measurement
    E.g. 'mm', 'cm'
    """
    pass


class SlDocumentCollection(SlAbstract):
    """
    An collection of Documents
    E.g. 'NLI', 'Khalili Collection', 'Sam Fogg Rate Books'
    """
    pass


class SlDocumentClassification(SlAbstract):
    """
    The team classifies Documents based on their quality/stag of development
    E.g. 'Gold', 'Silver', 'Bronze'
    """
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.order} - {self.name} ({self.description})'
    
    class Meta:
        ordering = ['order', Upper('name'), 'id']


class SlDocumentCorrespondence(SlAbstract):
    """
    The correspondence of a Document
    E.g. 'contract', 'administration', 'legal', 'colophon'
    """
    pass


class SlDocumentScript(SlAbstract):
    """
    A script that a Document was originally written in
    E.g. 'Arabic', 'Bactrian', 'New Persian'
    """
    pass


class SlDocumentLanguage(SlAbstract):
    """
    A language that a Document was originally written in
    E.g. 'Arabic', 'Bactrian', 'New Persian'
    """
    script = models.ForeignKey('SlDocumentScript', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.script:
            return f'{self.name} ({self.script.name} script)'
        else:
            return self.name


class SlTranslationLanguage(SlAbstract):
    """
    A language that a Document has been translated into
    E.g. 'English'
    """
    pass


class SlCountry(SlAbstract):
    """
    A type of location
    E.g. 'United Kingdom', 'United Arab Emirates'
    """
    pass


class SlMaterial(SlAbstract):
    """
    A material that a Document is made of
    E.g. 'paper', 'parchment', 'leather'
    """
    pass


class SlMaterialInk(SlAbstract):
    """
    An ink that's used to write content within a Document
    E.g. 'black'
    """
    pass


class SlPublicationStatement(SlAbstract):
    """
    A statement about who has published a Document
    E.g. 'This document is published and distributed online by the Invisible East project, University of Oxford.'
    """
    pass


class SlCalendar(SlAbstract):
    """
    A calendar/date system.
    E.g. 'Gregorian', 'Hijri', 'Bactrian'
    """
    name_full = models.CharField(max_length=100, blank=True, null=True)


class SlPersonInDocumentType(SlAbstract):
    """
    A type of person within a document.
    E.g. 'promisor', 'promisee', 'witness', 'sender', 'receiver'
    """
    pass


class SlDocumentTransType(SlAbstract):
    """
    A type of DocumentTrans.
    E.g. 'translation', 'transcription'
    """
    pass


class SlM2MPersonToPersonRelationshipType(SlAbstract):
    """
    A type of relationship between two persons.
    E.g. 'mother', 'brother', 'colleague'
    """
    pass


#
# 3. Main Models
#


class Document(models.Model):
    """
    A historical Document
    """

    related_name = 'documents'

    # General
    title = models.CharField(max_length=1000, blank=True, null=True)  # TODO XML titles need to be more consistent in structure across the range of languages
    subject = models.TextField(blank=True, null=True)  # "particDesc > p" in xml
    language = models.ForeignKey('SlDocumentLanguage', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    correspondence = models.ForeignKey('SlDocumentCorrespondence', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    keywords = models.ManyToManyField('SlKeyword', blank=True, related_name=related_name, db_index=True)
    funders = models.ManyToManyField('SlFunder', blank=True, related_name=related_name, db_index=True)
    writing_support = models.ForeignKey('SlDocumentWritingSupport', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)

    # Type and type-related
    type = models.ForeignKey('SlDocumentType', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    # The below fields may be related to above 'type' value, e.g. Legal or Administrative so need to show/hide necessary fields in admin
    legal_transactions = models.ManyToManyField('SlDocumentTypeLegalTransactions', blank=True, related_name=related_name, db_index=True)
    administrative_internal_correspondence = models.ManyToManyField('SlDocumentTypeAdministrativeInternalCorrespondence', blank=True, related_name=related_name, db_index=True)
    administrative_tax_receipts = models.ManyToManyField('SlDocumentTypeAdministrativeTaxReceipts', blank=True, related_name=related_name, db_index=True)
    administrative_lists_and_accounting = models.ManyToManyField('SlDocumentTypeAdministrativeListsAndAccounting', blank=True, related_name=related_name, db_index=True)
    land_measurement_units = models.ManyToManyField('SlDocumentTypeLandMeasurementUnits', blank=True, related_name=related_name, db_index=True)
    people_and_processes_admin = models.ManyToManyField('SlDocumentTypePeopleAndProcessesAdmin', blank=True, related_name=related_name, db_index=True, help_text='People and processes involved in public administration, tax, trade, and commerce')
    people_and_processes_legal = models.ManyToManyField('SlDocumentTypePeopleAndProcessesLegal', blank=True, related_name=related_name, db_index=True, help_text='People and processes involved in legal and judiciary system')
    documentation = models.ManyToManyField('SlDocumentTypeDocumentation', blank=True, related_name=related_name, db_index=True)
    geographic_administrative_units = models.ManyToManyField('SlDocumentTypeGeographicAdministrativeUnits', blank=True, related_name=related_name, db_index=True)
    legal_and_administrative_stock_phrases = models.ManyToManyField('SlDocumentTypeLegalAndAdministrativeStockPhrases', blank=True, related_name=related_name, db_index=True)
    finance_and_accountancy_phrases = models.ManyToManyField('SlDocumentTypeFinanceAndAccountancyPhrases', blank=True, related_name=related_name, db_index=True)
    agricultural_produce = models.ManyToManyField('SlDocumentTypeAgriculturalProduce', blank=True, related_name=related_name, db_index=True, help_text='Agricultural produce, animals, and farming equipment')
    currencies_and_denominations = models.ManyToManyField('SlDocumentTypeCurrenciesAndDenominations', blank=True, related_name=related_name, db_index=True)
    markings = models.ManyToManyField('SlDocumentTypeMarkings', blank=True, related_name=related_name, db_index=True, help_text='Scribal markings, ciphers, abbreviations, para-text, column format')
    religion = models.ManyToManyField('SlDocumentTypeReligion', blank=True, related_name=related_name, db_index=True)
    # Toponym (place names)
    toponym_bamiyan = models.ManyToManyField('SlDocumentTypeToponymBamiyan', blank=True, related_name=related_name, db_index=True, help_text='Place names featuring in Bamiyan papers')
    toponym_firuzkuh = models.ManyToManyField('SlDocumentTypeToponymFiruzkuh', blank=True, related_name=related_name, db_index=True, help_text='Place names featuring in Firuzkuh papers')
    toponym_persian_khalili = models.ManyToManyField('SlDocumentTypeToponymPersianKhalili', blank=True, related_name=related_name, db_index=True, help_text='Place names featuring in Persian Khalili papers')
    toponym_bactrian = models.ManyToManyField('SlDocumentTypeToponymBactrian', blank=True, related_name=related_name, db_index=True, help_text='Place names featuring in Bactrian documents')
    toponym_khurasan = models.ManyToManyField('SlDocumentTypeToponymKhurasan', blank=True, related_name=related_name, db_index=True, help_text='Place names featuring in Arabic Bactrian (Khurasan) documents')
    toponym_middle_persian = models.ManyToManyField('SlDocumentTypeToponymMiddlePersian', blank=True, related_name=related_name, db_index=True, help_text='Place names featuring in Middle Persian documents')

    # Publication Statements
    publication_statement = models.ForeignKey('SlPublicationStatement', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    publication_statement_original = models.TextField(blank=True, null=True)  # "publicationStmt > p (Originally...)" in xml
    publication_statement_republished = models.TextField(blank=True, null=True)  # "publicationStmt > p (The document was later republished...)" in xml

    # Responsibility Statement (respStmt) - is this needed?
    # Initial reading and translation
    # Preparation of the document for the Invisible East
    # TEI encoding
    # Encoding review

    # Manuscript Identifier (msIdentifier)
    country = models.ForeignKey('SlCountry', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    collection = models.ForeignKey('SlDocumentCollection', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)  # <institution> in xml
    shelfmark = models.CharField(max_length=1000, blank=True, null=True)
    # <idno type="NSW">?
    # <idno type="URI">?

    # Physical Description
    materials = models.ManyToManyField('SlMaterial', blank=True, related_name=related_name, db_index=True)
    material_details = models.TextField(blank=True, null=True)
    dimensions_unit = models.ForeignKey('SlUnitOfMeasurement', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    dimensions_height = models.FloatField(blank=True, null=True)
    dimensions_width = models.FloatField(blank=True, null=True)

    # What to do with this data?... inconsistent in XML (see todo.md). Split into recto/verso for line count? Store as char (so can add details) or int (so can sort)? etc.
    fold_lines = models.IntegerField(blank=True, null=True)
    layout_description = models.TextField(blank=True, null=True)

    physical_additional_details = models.TextField(blank=True, null=True)

    # Correspondance
    place = models.CharField(max_length=1000, blank=True, null=True)
    # Persons data (see DocumentPerson model)
    # Dates data (see DocumentDate model)

    # Admin
    admin_classification = models.ForeignKey('SlDocumentClassification', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    admin_public = models.BooleanField(default=False, help_text='Tick to make this document publicly available')
    admin_commentary = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)

    # Metadata
    meta_created_by = models.ForeignKey(User,
                                        related_name="document_created_by",
                                        on_delete=models.PROTECT,
                                        blank=True,
                                        null=True,
                                        verbose_name="created by")
    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name="created")
    meta_lastupdated_by = models.ForeignKey(User,
                                            related_name="document_lastupdated_by",
                                            on_delete=models.PROTECT,
                                            blank=True,
                                            null=True,
                                            verbose_name="last updated by")
    meta_lastupdated_datetime = models.DateTimeField(blank=True, null=True, verbose_name="last updated")

    @property
    def title_full(self):
        return f"{self.id}: {self.title}"

    def __str__(self):
        return self.title_full


class Person(models.Model):
    """
    A Person that appears in a Document
    """

    name = models.CharField(max_length=1000)
    person = models.ManyToManyField('self', through='M2MPersonToPerson', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']


class PersonInDocument(models.Model):
    """
    An instance of a DocumentPerson appearing within a Document
    """

    related_name = 'persons_in_documents'

    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name=related_name)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name=related_name)
    person_name_in_document = models.CharField(max_length=1000, blank=True, null=True, help_text='If Person is named differently in Document than in this database then record their name in the Document here')
    type = models.ForeignKey('SlPersonInDocumentType', on_delete=models.RESTRICT, related_name=related_name)

    def __str__(self):
        return f'{self.document.title}: {self.person.name} ({self.type.name})'


class DocumentDate(models.Model):
    """
    A date of a Document
    """

    related_name = 'document_dates'

    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name=related_name)
    calendar = models.ForeignKey('SlCalendar', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    date = models.CharField(max_length=1000, blank=True, null=True, help_text='E.g. 0605-09-10, 1198-02-11, etc.')
    date_not_before = models.CharField(max_length=1000, blank=True, null=True, help_text='E.g. 0605-09-10, 1198-02-11, etc.')
    date_not_after = models.CharField(max_length=1000, blank=True, null=True, help_text='E.g. 0605-09-10, 1198-02-11, etc.')
    date_text = models.CharField(max_length=1000, blank=True, null=True, help_text='E.g. 10 Ramaḍān 605, 11 Feb 1198, etc.')


class DocumentImage(models.Model):
    """
    An image of a Document
    """

    related_name = 'document_images'

    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name=related_name)
    # TODO


class DocumentTrans(models.Model):
    """
    A transcription or translation of a Document
    """

    related_name = 'document_trans'

    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name=related_name)
    type = models.ForeignKey('SlDocumentTransType', on_delete=models.RESTRICT)  # e.g. transcription or translation
    # TODO


# ... determine structure to record data about parts within documents and link to position in images


# Many to Many Relationships

class M2MPersonToPerson(models.Model):
    """
    Many to many relationship between 2x DocumentPerson objects
    """
    person_1 = models.ForeignKey(Person, related_name='person_1', on_delete=models.CASCADE)
    person_2 = models.ForeignKey(Person, related_name='person_2', on_delete=models.CASCADE)
    relationship_type = models.ForeignKey(SlM2MPersonToPersonRelationshipType, on_delete=models.CASCADE)
