from django.db import models
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
    order = models.IntegerField(blank=True, null=True)


class SlDocumentCorrespondence(SlAbstract):
    """
    The correspondence of a Document
    E.g. 'contract', 'administration', 'legal', 'colophon'
    """
    pass


class SlDocumentLanguage(SlAbstract):
    """
    A language that a Document was originally written in
    E.g. 'Arabic', 'Bactrian', 'New Persian'
    """
    pass


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


class SlDocumentPersonType(SlAbstract):
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


#
# 3. Main Models
#


class Document(models.Model):
    """
    A historical Document
    """

    related_name = 'documents'

    # General
    title = models.CharField(max_length=1000, blank=True, null=True)  # XML titles need to be more consistent in structure across the range of languages
    subject = models.TextField(blank=True, null=True)  # "particDesc > p" in xml
    language = models.ForeignKey('SlDocumentLanguage', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    correspondence = models.ForeignKey('SlDocumentCorrespondence', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    keywords = models.ManyToManyField('SlKeyword', blank=True, related_name=related_name, db_index=True)
    funders = models.ManyToManyField('SlFunder', blank=True, related_name=related_name, db_index=True)

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
                                        verbose_name="Created By")
    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    meta_lastupdated_by = models.ForeignKey(User,
                                            related_name="document_lastupdated_by",
                                            on_delete=models.PROTECT,
                                            blank=True,
                                            null=True,
                                            verbose_name="Last Updated By")
    meta_lastupdated_datetime = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    meta_firstpublished_datetime = models.DateTimeField(blank=True, null=True, verbose_name="First Published")


    @property
    def title_full(self):
        return f"{self.id}: {self.title}"

    def __str__(self):
        return self.title_full


class DocumentPerson(models.Model):
    """
    A Person that appears in a Document
    """

    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']


class DocumentPersonAppearance(models.Model):
    """
    An instance of a DocumentPerson appearing within a Document
    """

    related_name = 'document_persons'

    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name=related_name)
    person = models.ForeignKey('DocumentPerson', on_delete=models.CASCADE, related_name=related_name)
    type = models.ForeignKey('SlDocumentPersonType', on_delete=models.RESTRICT, related_name=related_name)

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
    type = models.ForeignKey('SlDocumentTransType', on_delete=models.RESTRICT) # e.g. transcription or translation
    # TODO


# ... determine structure to record data about parts within documents and link to position in images
