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


class SlTextTypeCategory(SlAbstract):
    """
    A type of Text
    E.g. 'document', 'literature'
    """
    pass


class SlTextType(SlAbstract):
    """
    A type of Text
    E.g. 'legal', 'letter'
    """
    category = models.ForeignKey('SlTextTypeCategory', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})' if self.category else self.name


class SlTextTypeLegalTransactions(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeAdministrativeInternalCorrespondence(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeAdministrativeTaxReceipts(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeAdministrativeListsAndAccounting(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeLandMeasurementUnits(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypePeopleAndProcessesAdmin(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypePeopleAndProcessesLegal(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeDocumentation(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeGeographicAdministrativeUnits(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeLegalAndAdministrativeStockPhrases(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeFinanceAndAccountancyPhrases(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeAgriculturalProduce(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeCurrenciesAndDenominations(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeMarkings(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeReligion(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTypeToponym(SlAbstract):
    """
    A Text type related field. Toponym = place
    """
    pass


class SlTextWritingSupport(SlAbstract):
    """
    A type of Text
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


class SlTextCollection(SlAbstract):
    """
    An collection of Texts
    E.g. 'NLI', 'Khalili Collection', 'Sam Fogg Rate Books'
    """
    pass


class SlTextClassification(SlAbstract):
    """
    The team classifies Texts based on their quality/stag of development
    E.g. 'Gold', 'Silver', 'Bronze'
    """
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.order} - {self.name} ({self.description})'
    
    class Meta:
        ordering = ['order', Upper('name'), 'id']


class SlTextCorrespondence(SlAbstract):
    """
    The correspondence of a Text
    E.g. 'contract', 'administration', 'legal', 'colophon'
    """
    pass


class SlTextScript(SlAbstract):
    """
    A script that a Text was originally written in
    E.g. 'Arabic', 'Bactrian', 'New Persian'
    """
    pass


class SlTextLanguage(SlAbstract):
    """
    A language that a Text was originally written in
    E.g. 'Arabic', 'Bactrian', 'New Persian'
    """
    script = models.ForeignKey('SlTextScript', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.script:
            return f'{self.name} ({self.script.name} script)'
        else:
            return self.name


class SlTranslationLanguage(SlAbstract):
    """
    A language that a Text has been translated into
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
    A statement about who has published a Text
    E.g. 'This text is published and distributed online by the Invisible East project, University of Oxford.'
    """
    pass


class SlCalendar(SlAbstract):
    """
    A calendar/date system.
    E.g. 'Gregorian', 'Hijri', 'Bactrian'
    """
    name_full = models.CharField(max_length=100, blank=True, null=True)


class SlPersonInTextRole(SlAbstract):
    """
    A type of person within a text.
    E.g. 'promisor', 'promisee', 'witness', 'sender', 'receiver'
    """
    pass


class SlTextFolioSide(SlAbstract):
    """
    The side of a TextFolio within a Text.
    E.g. 'recto', 'verso'
    """
    pass


class SlTextFolioOpen(SlAbstract):
    """
    Whether a TextFolio is open or closed.
    E.g. 'open', 'closed'
    """
    pass


class SlTextFolioPartType(SlAbstract):
    """
    A type of TextFolioPart.
    E.g. 'damage', 'mark'
    """
    pass


class SlM2MPersonToPersonRelationshipType(SlAbstract):
    """
    A type of relationship between two persons.
    E.g. 'mother', 'brother', 'colleague'
    """
    pass


class SlM2MTextToTextRelationshipType(SlAbstract):
    """
    A type of relationship between two texts.
    E.g. 'in same document'
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


class Text(models.Model):
    """
    A historical Text
    """

    related_name = 'texts'

    # General
    collection = models.ForeignKey('SlTextCollection', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    shelfmark = models.CharField(max_length=1000, blank=True, null=True)
    id_khan = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Khan ID")
    id_nicholas_simms_williams = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nicholas Simms-Williams ID")
    country = models.ForeignKey('SlCountry', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    subject = models.TextField(blank=True, null=True)
    languages = models.ManyToManyField('SlTextLanguage', blank=True, related_name=related_name, db_index=True)
    correspondence = models.ForeignKey('SlTextCorrespondence', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    funders = models.ManyToManyField('SlFunder', blank=True, related_name=related_name, db_index=True)
    texts = models.ManyToManyField('self', through='M2MTextToText', blank=True)

    # Type and type-related
    type = models.ForeignKey('SlTextType', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    # The below fields may be related to above 'type' value, e.g. Legal or Administrative so need to show/hide necessary fields in admin
    legal_transactions = models.ManyToManyField('SlTextTypeLegalTransactions', blank=True, related_name=related_name, db_index=True)
    administrative_internal_correspondences = models.ManyToManyField('SlTextTypeAdministrativeInternalCorrespondence', blank=True, related_name=related_name, db_index=True)
    administrative_tax_receipts = models.ManyToManyField('SlTextTypeAdministrativeTaxReceipts', blank=True, related_name=related_name, db_index=True)
    administrative_lists_and_accounting = models.ManyToManyField('SlTextTypeAdministrativeListsAndAccounting', blank=True, related_name=related_name, db_index=True)
    land_measurement_units = models.ManyToManyField('SlTextTypeLandMeasurementUnits', blank=True, related_name=related_name, db_index=True)
    people_and_processes_admins = models.ManyToManyField('SlTextTypePeopleAndProcessesAdmin', blank=True, related_name=related_name, db_index=True, verbose_name='People and processes involved in public administration, tax, trade, and commerce')
    people_and_processes_legal = models.ManyToManyField('SlTextTypePeopleAndProcessesLegal', blank=True, related_name=related_name, db_index=True, verbose_name='People and processes involved in legal and judiciary system')
    documentations = models.ManyToManyField('SlTextTypeDocumentation', blank=True, related_name=related_name, db_index=True)
    geographic_administrative_units = models.ManyToManyField('SlTextTypeGeographicAdministrativeUnits', blank=True, related_name=related_name, db_index=True)
    legal_and_administrative_stock_phrases = models.ManyToManyField('SlTextTypeLegalAndAdministrativeStockPhrases', blank=True, related_name=related_name, db_index=True)
    finance_and_accountancy_phrases = models.ManyToManyField('SlTextTypeFinanceAndAccountancyPhrases', blank=True, related_name=related_name, db_index=True)
    agricultural_produce = models.ManyToManyField('SlTextTypeAgriculturalProduce', blank=True, related_name=related_name, db_index=True, help_text='Agricultural produce, animals, and farming equipment')
    currencies_and_denominations = models.ManyToManyField('SlTextTypeCurrenciesAndDenominations', blank=True, related_name=related_name, db_index=True)
    markings = models.ManyToManyField('SlTextTypeMarkings', blank=True, related_name=related_name, db_index=True, help_text='Scribal markings, ciphers, abbreviations, para-text, column format')
    religions = models.ManyToManyField('SlTextTypeReligion', blank=True, related_name=related_name, db_index=True)
    toponyms = models.ManyToManyField('SlTextTypeToponym', blank=True, related_name=related_name, db_index=True, help_text='Place names')

    # Publication Statements
    publication_statement = models.ForeignKey('SlPublicationStatement', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    publication_statement_original = models.TextField(blank=True, null=True)  # "publicationStmt > p (Originally...)" in xml
    publication_statement_republished = models.TextField(blank=True, null=True)  # "publicationStmt > p (The text was later republished...)" in xml

    # Physical Description
    writing_support = models.ForeignKey('SlTextWritingSupport', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    writing_support_details = models.TextField(blank=True, null=True)
    dimensions_unit = models.ForeignKey('SlUnitOfMeasurement', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    dimensions_height = models.FloatField(blank=True, null=True)
    dimensions_width = models.FloatField(blank=True, null=True)
    fold_lines_count_details = models.TextField(blank=True, null=True, help_text='Include fold lines count details, e.g. for recto, verso, etc.')
    fold_lines_count_total = models.IntegerField(blank=True, null=True, help_text='Specify the total number of fold lines for this Text (you may need to add together the fold lines counts of recto, verso, etc. where applicable)')
    physical_additional_details = models.TextField(blank=True, null=True)

    # Approve Text to Show on Public Website
    public_review_requests = models.ManyToManyField(
        User,
        related_name="text_public_review_request",
        blank=True,
        help_text='Select admins to request that they review this Text and approve it to be shown on the public website. Reviewers will be notified via email.'
    )
    public_review_notes = models.TextField(blank=True, null=True, help_text="Used to make comments or notes during the review process.")
    public_approval_1_of_2 = models.ForeignKey(
        User,
        related_name="text_public_approval_1_of_2",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='Texts must be approved by 2 admins to be visible on the public website. This is the 1st approval.'
    )
    public_approval_1_of_2_datetime = models.DateTimeField(blank=True, null=True)
    public_approval_2_of_2 = models.ForeignKey(
        User,
        related_name="text_public_approval_2_of_2",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='Texts must be approved by 2 admins to be visible on the public website. This is the 2nd approval.'
    )
    public_approval_2_of_2_datetime = models.DateTimeField(blank=True, null=True)

    # Admin
    admin_commentary = models.TextField(blank=True, null=True)
    admin_classification = models.ForeignKey('SlTextClassification', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    admin_owners = models.ManyToManyField(
        User,
        related_name='text_admin_owners',
        blank=True,
        help_text='Admins who are responsible for this text'
    )
    admin_contributors = models.ManyToManyField(
        User,
        related_name='text_admin_contributors',
        blank=True,
        help_text='Admins who have contributed to this text but are not responsible for it'
    )
    admin_notes = models.TextField(blank=True, null=True)

    # Metadata
    meta_created_by = models.ForeignKey(
        User,
        related_name="text_created_by",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="created by"
    )
    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name="created")
    meta_lastupdated_by = models.ForeignKey(
        User,
        related_name="text_lastupdated_by",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="last updated by"
    )
    meta_lastupdated_datetime = models.DateTimeField(blank=True, null=True, verbose_name="last updated")

    @property
    def title(self):
        return f"{self.type.name}: {self.collection}, {self.shelfmark}"

    @property
    def public_approved(self):
        # True if 2 approvals to include this Text on public website
        return self.public_approval_1_of_2 and self.public_approval_2_of_2

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Corpus Text'


class TextDate(models.Model):
    """
    A date of a Text
    """

    related_name = 'text_dates'

    text = models.ForeignKey('Text', on_delete=models.CASCADE, related_name=related_name)
    calendar = models.ForeignKey('SlCalendar', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    date = models.CharField(max_length=1000, blank=True, null=True, help_text='E.g. 0605-09-10, 1198-02-11, etc.')
    date_not_before = models.CharField(max_length=1000, blank=True, null=True, help_text='E.g. 0605-09-10, 1198-02-11, etc.')
    date_not_after = models.CharField(max_length=1000, blank=True, null=True, help_text='E.g. 0605-09-10, 1198-02-11, etc.')
    date_text = models.CharField(max_length=1000, blank=True, null=True, help_text='E.g. 10 Ramaḍān 605, 11 Feb 1198, etc.')


class TextFolio(models.Model):
    """
    A folio (e.g. a side of paper) within a Text
    """

    related_name = 'text_folios'

    text = models.ForeignKey('Text', on_delete=models.CASCADE, related_name=related_name)
    side = models.ForeignKey('SlTextFolioSide', on_delete=models.RESTRICT, blank=True, null=True)
    open_state = models.ForeignKey('SlTextFolioOpen', on_delete=models.RESTRICT, blank=True, null=True)
    image = models.ImageField(upload_to='researchdata/text_folios', blank=True, null=True)

    def __str__(self):
        # Build the descriptors text
        descriptors = [str(field) for field in [self.side, self.open_state] if field is not None]
        descriptors_text = f' ({", ".join(descriptors)})' if len(descriptors) else ''
        # Return the string
        return f'{self.text}: Folio {descriptors_text}'

    class Meta:
        ordering = ['text', 'open_state', 'side', 'id']


class TextFolioLine(models.Model):
    """
    A line of text within a TextFolio
    """

    related_name = 'text_folio_lines'

    text_folio = models.ForeignKey('TextFolio', on_delete=models.CASCADE, related_name=related_name)

    # Transcription (original language)
    transcription_line_number = models.IntegerField()
    transcription_line_number_end = models.IntegerField(blank=True, null=True, help_text='If this line spans multiple lines, specify the last line number here. E.g. if line range is 19-21, put 21 here')
    transcription_text = models.TextField(max_length=1000, blank=True, null=True)

    # Translation (English)
    translation_line_number = models.IntegerField(blank=True, null=True)
    translation_line_number_end = models.IntegerField(blank=True, null=True, help_text='If this line spans multiple lines, specify the last line number here. E.g. if line range is 19-21, put 21 here')
    translation_text = models.TextField(max_length=1000, blank=True, null=True)

    position_in_image = models.TextField(blank=True, null=True)  # TODO


class TextFolioPart(models.Model):
    """
    A part of a TextFolio (other than lines of text) that is noteworthy
    e.g. damage, marks, drawings, etc.
    """

    related_name = 'text_folio_parts'

    text_folio = models.ForeignKey('TextFolio', on_delete=models.CASCADE, related_name=related_name)
    type = models.ForeignKey('SlTextFolioPartType', on_delete=models.CASCADE, related_name=related_name)
    description = models.TextField(max_length=1000, blank=True, null=True)
    position_in_image = models.TextField(blank=True, null=True)  # TODO


class Person(models.Model):
    """
    A Person that appears in a Text
    """

    name = models.CharField(max_length=1000)
    gender = models.ForeignKey('SlPersonGender', on_delete=models.CASCADE, blank=True, null=True)
    profession = models.CharField(max_length=1000, blank=True, null=True)
    persons = models.ManyToManyField('self', through='M2MPersonToPerson', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']


class PersonInText(models.Model):
    """
    An instance of a Person appearing within a Text
    """

    related_name = 'persons_in_texts'

    text = models.ForeignKey('Text', on_delete=models.CASCADE, related_name=related_name)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name=related_name)
    person_name_in_text = models.CharField(max_length=1000, blank=True, null=True, help_text='If Person is named differently in Text than in this database then record their name in the Text here')
    person_role_in_text = models.ForeignKey('SlPersonInTextRole', on_delete=models.RESTRICT, related_name=related_name)

    def __str__(self):
        return f'{self.text.title}: {self.person.name} ({self.person_role_in_text.name})'


# Many to Many Relationships


class M2MPersonToPerson(models.Model):
    """
    Many to many relationship between 2x Person objects
    """
    person_1 = models.ForeignKey(Person, related_name='person_1', on_delete=models.CASCADE, verbose_name='person')
    person_2 = models.ForeignKey(Person, related_name='person_2', on_delete=models.CASCADE, verbose_name='person')
    relationship_type = models.ForeignKey(SlM2MPersonToPersonRelationshipType, on_delete=models.CASCADE)
    relationship_details = models.CharField(max_length=1000, blank=True, null=True)


class M2MTextToText(models.Model):
    """
    Many to many relationship between 2x Text objects
    """
    text_1 = models.ForeignKey(Text, related_name='text_1', on_delete=models.CASCADE, verbose_name='text')
    text_2 = models.ForeignKey(Text, related_name='text_2', on_delete=models.CASCADE, verbose_name='text')
    relationship_type = models.ForeignKey(SlM2MTextToTextRelationshipType, on_delete=models.CASCADE)
    relationship_details = models.CharField(max_length=1000, blank=True, null=True)
