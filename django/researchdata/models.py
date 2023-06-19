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

    name = models.CharField(max_length=1000, db_index=True)

    def __str__(self):
        return self.name if self.name and self.name != "" else f"#{self.id}"

    class Meta:
        abstract = True
        ordering = [Upper('name'), 'id']


#
# 2. Select List models (all inherit from above SlAbstract class, with some extending with additional fields, etc.)
#


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


class SlDocumentTypeToponym(SlAbstract):
    """
    A Document type related field. Toponym = place
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


class SlDocumentPageSide(SlAbstract):
    """
    The side of a DocumentPage within a Document.
    E.g. 'recto', 'verso'
    """
    pass


class SlDocumentPageOpen(SlAbstract):
    """
    Whether a DocumentPage is open or closed.
    E.g. 'open', 'closed'
    """
    pass


class SlDocumentPageContentType(SlAbstract):
    """
    A type of DocumentPageContent.
    E.g. 'translation', 'original transcription', 'transliteration'
    """
    pass


class SlDocumentPageContentPartType(SlAbstract):
    """
    A type of DocumentPageContentPart.
    E.g. 'line of text', 'drawing'
    """
    pass


class SlM2MPersonToPersonRelationshipType(SlAbstract):
    """
    A type of relationship between two persons.
    E.g. 'mother', 'brother', 'colleague'
    """
    pass


class SlPersonGender(SlAbstract):
    """
    A gender of a person.
    E.g. 'male', 'female'
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
    languages = models.ManyToManyField('SlDocumentLanguage', blank=True, related_name=related_name, db_index=True)
    correspondence = models.ForeignKey('SlDocumentCorrespondence', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    funders = models.ManyToManyField('SlFunder', blank=True, related_name=related_name, db_index=True)

    # Type and type-related
    type = models.ForeignKey('SlDocumentType', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    # The below fields may be related to above 'type' value, e.g. Legal or Administrative so need to show/hide necessary fields in admin
    legal_transactions = models.ManyToManyField('SlDocumentTypeLegalTransactions', blank=True, related_name=related_name, db_index=True)
    administrative_internal_correspondences = models.ManyToManyField('SlDocumentTypeAdministrativeInternalCorrespondence', blank=True, related_name=related_name, db_index=True)
    administrative_tax_receipts = models.ManyToManyField('SlDocumentTypeAdministrativeTaxReceipts', blank=True, related_name=related_name, db_index=True)
    administrative_lists_and_accounting = models.ManyToManyField('SlDocumentTypeAdministrativeListsAndAccounting', blank=True, related_name=related_name, db_index=True)
    land_measurement_units = models.ManyToManyField('SlDocumentTypeLandMeasurementUnits', blank=True, related_name=related_name, db_index=True)
    people_and_processes_admins = models.ManyToManyField('SlDocumentTypePeopleAndProcessesAdmin', blank=True, related_name=related_name, db_index=True, help_text='People and processes involved in public administration, tax, trade, and commerce')
    people_and_processes_legal = models.ManyToManyField('SlDocumentTypePeopleAndProcessesLegal', blank=True, related_name=related_name, db_index=True, help_text='People and processes involved in legal and judiciary system')
    documentations = models.ManyToManyField('SlDocumentTypeDocumentation', blank=True, related_name=related_name, db_index=True)
    geographic_administrative_units = models.ManyToManyField('SlDocumentTypeGeographicAdministrativeUnits', blank=True, related_name=related_name, db_index=True)
    legal_and_administrative_stock_phrases = models.ManyToManyField('SlDocumentTypeLegalAndAdministrativeStockPhrases', blank=True, related_name=related_name, db_index=True)
    finance_and_accountancy_phrases = models.ManyToManyField('SlDocumentTypeFinanceAndAccountancyPhrases', blank=True, related_name=related_name, db_index=True)
    agricultural_produce = models.ManyToManyField('SlDocumentTypeAgriculturalProduce', blank=True, related_name=related_name, db_index=True, help_text='Agricultural produce, animals, and farming equipment')
    currencies_and_denominations = models.ManyToManyField('SlDocumentTypeCurrenciesAndDenominations', blank=True, related_name=related_name, db_index=True)
    markings = models.ManyToManyField('SlDocumentTypeMarkings', blank=True, related_name=related_name, db_index=True, help_text='Scribal markings, ciphers, abbreviations, para-text, column format')
    religions = models.ManyToManyField('SlDocumentTypeReligion', blank=True, related_name=related_name, db_index=True)
    toponyms = models.ManyToManyField('SlDocumentTypeToponym', blank=True, related_name=related_name, db_index=True, help_text='Place names')

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
    writing_support = models.ForeignKey('SlDocumentWritingSupport', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    writing_support_details = models.TextField(blank=True, null=True)
    dimensions_unit = models.ForeignKey('SlUnitOfMeasurement', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    dimensions_height = models.FloatField(blank=True, null=True)
    dimensions_width = models.FloatField(blank=True, null=True)
    fold_lines_count_details = models.TextField(blank=True, null=True, help_text='Include fold lines count details, e.g. for recto, verso, etc.')
    fold_lines_count_total = models.IntegerField(blank=True, null=True, help_text='Specify the total number of fold lines for this Document (you may need to add together the fold lines counts of recto, verso, etc. where applicable)')
    physical_additional_details = models.TextField(blank=True, null=True)

    # Approve Document to Show on Public Website
    public_review_requests = models.ManyToManyField(
        User,
        related_name="document_public_review_request",
        blank=True,
        help_text='Select admins to request that they review this Document and approve it to be shown on the public website. Reviewers will be notified via email.'
    )
    public_review_notes = models.TextField(blank=True, null=True, help_text="Used to make comments or notes during the review process.")
    public_approval_1_of_2 = models.ForeignKey(
        User,
        related_name="document_public_approval_1_of_2",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='Documents must be approved by 2 admins to be visible on the public website. This is the 1st approval.'
    )
    public_approval_1_of_2_datetime = models.DateTimeField(blank=True, null=True)
    public_approval_2_of_2 = models.ForeignKey(
        User,
        related_name="document_public_approval_2_of_2",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='Documents must be approved by 2 admins to be visible on the public website. This is the 2nd approval.'
    )
    public_approval_2_of_2_datetime = models.DateTimeField(blank=True, null=True)

    # Admin
    admin_commentary = models.TextField(blank=True, null=True)
    admin_classification = models.ForeignKey('SlDocumentClassification', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    admin_owners = models.ManyToManyField(
        User,
        related_name='document_admin_owners',
        blank=True,
        help_text='Admins who are responsible for this document'
    )
    admin_contributors = models.ManyToManyField(
        User,
        related_name='document_admin_contributors',
        blank=True,
        help_text='Admins who have contributed to this document but are not responsible for it'
    )
    admin_notes = models.TextField(blank=True, null=True)

    # Metadata
    meta_created_by = models.ForeignKey(
        User,
        related_name="document_created_by",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="created by"
    )
    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name="created")
    meta_lastupdated_by = models.ForeignKey(
        User,
        related_name="document_lastupdated_by",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="last updated by"
    )
    meta_lastupdated_datetime = models.DateTimeField(blank=True, null=True, verbose_name="last updated")

    @property
    def title_full(self):
        return f"{self.id}: {self.title}"

    @property
    def public_approved(self):
        # True if 2 approvals to include this Document on public website
        return self.public_approval_1_of_2 and self.public_approval_2_of_2

    def __str__(self):
        return self.title_full


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


class DocumentPage(models.Model):
    """
    A page within a Document
    """

    related_name = 'document_pages'

    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name=related_name)
    page_number = models.IntegerField()
    side = models.ForeignKey('SlDocumentPageSide', on_delete=models.RESTRICT, blank=True, null=True)
    open_state = models.ForeignKey('SlDocumentPageOpen', on_delete=models.RESTRICT, blank=True, null=True)
    image = models.ImageField(upload_to='researchdata/document_pages', blank=True, null=True)

    def __str__(self):
        return f'{self.document}: Page {self.page_number} ({self.side})'

    class Meta:
        ordering = ['page_number', 'id']


class DocumentPageLine(models.Model):
    """
    A line of text within a DocumentPage
    """

    related_name = 'document_page_lines'

    document_page = models.ForeignKey('DocumentPage', on_delete=models.CASCADE, related_name=related_name)

    # Transcription (original language)
    transcription_line_number = models.IntegerField()
    transcription_line_number_end = models.IntegerField(blank=True, null=True, help_text='If this line spans multiple lines, specify the last line number here. E.g. if line range is 19-21, put 21 here')
    transcription_text = models.TextField(max_length=1000, blank=True, null=True)

    # Translation (English)
    translation_line_number = models.IntegerField(blank=True, null=True)
    translation_line_number_end = models.IntegerField(blank=True, null=True, help_text='If this line spans multiple lines, specify the last line number here. E.g. if line range is 19-21, put 21 here')
    translation_text = models.TextField(max_length=1000, blank=True, null=True)

    position_in_image = models.TextField(blank=True, null=True)  # TODO


class Person(models.Model):
    """
    A Person that appears in a Document
    """

    name = models.CharField(max_length=1000)
    gender = models.ForeignKey('SlPersonGender', on_delete=models.CASCADE, blank=True, null=True)
    profession = models.CharField(max_length=1000, blank=True, null=True)
    person = models.ManyToManyField('self', through='M2MPersonToPerson', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']


class PersonInDocument(models.Model):
    """
    An instance of a Person appearing within a Document
    """

    related_name = 'persons_in_documents'

    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name=related_name)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name=related_name)
    person_name_in_document = models.CharField(max_length=1000, blank=True, null=True, help_text='If Person is named differently in Document than in this database then record their name in the Document here')
    type = models.ForeignKey('SlPersonInDocumentType', on_delete=models.RESTRICT, related_name=related_name)

    def __str__(self):
        return f'{self.document.title}: {self.person.name} ({self.type.name})'


# Many to Many Relationships


class M2MPersonToPerson(models.Model):
    """
    Many to many relationship between 2x Person objects
    """
    person_1 = models.ForeignKey(Person, related_name='person_1', on_delete=models.CASCADE)
    person_2 = models.ForeignKey(Person, related_name='person_2', on_delete=models.CASCADE)
    relationship_type = models.ForeignKey(SlM2MPersonToPersonRelationshipType, on_delete=models.CASCADE)
