from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe
from PIL import Image, ImageOps
from django.core.files import File
from io import BytesIO
from django.db.models.functions import Upper
from account.models import User
import os


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


def image_compress(image_field_original, image_field_compressed, image_size):
    """
    Compresses an image to be suitable for web (i.e. in JPEG or PNG format with faster load times)
    Returns the value of an image field:
        - if an image exists will return the file path within the media directory as a string
        - if no image exists will delete it and return None
    """
    if image_field_original:
        # Must be PNG (.png) or JPEG (.jpg)
        file_extension = image_field_original.name.split('.')[-1].lower()
        if file_extension == 'png':
            file_format = 'PNG'
        else:
            file_format = 'JPEG'
            file_extension = 'jpg'
        if image_field_compressed:
            image_field_compressed.delete(save=False)
        img_compressed = Image.open(image_field_original.path)
        img_compressed.thumbnail((image_size, image_size))
        img_compressed = ImageOps.exif_transpose(img_compressed)  # Rotate to correct orientation
        blob_thumbnail = BytesIO()
        if file_format == 'JPEG' and img_compressed.mode in ("RGBA", "P"):
            img_compressed = img_compressed.convert("RGB")
        img_compressed.save(blob_thumbnail, file_format, optimize=True, quality=80)
        name = os.path.basename(image_field_original.name).rsplit('.', 1)[0]  # removes extension from main image name

        image_field_compressed_full_name = f'{name}__lte{image_size}px.{file_extension}'
        # Save the image file
        image_field_compressed.save(image_field_compressed_full_name, File(blob_thumbnail), save=False)
        # Return the compressed image field value (the path to the image)
        return f'{image_field_compressed.field.upload_to}/{image_field_compressed_full_name}'

    # Delete compressed image if no original image field but compressed image field still exists
    elif image_field_compressed:
        image_field_compressed.delete(save=False)
        return None


def image_is_wider_than_tall(image_field):
    """
    Takes in a Django image_field
    Returns:
        - True, if the image is wider than it is tall (height > width)
        - False, if the image is taller than it is wide (width > height)
        - None, if imagefield has no image
    Called by certain models below that have images, e.g. DocumentImage
    """

    if image_field:
        try:
            width, height = Image.open(image_field.path).size
            return True if width > height else False
        except Exception:
            pass


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


class SlTextSubjectLegalTransactions(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectAdministrativeInternalCorrespondence(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectAdministrativeTaxReceipts(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectAdministrativeListsAndAccounting(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectLandMeasurementUnits(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectPeopleAndProcessesAdmin(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectPeopleAndProcessesLegal(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectDocumentation(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectGeographicAdministrativeUnits(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectLegalAndAdministrativeStockPhrases(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectFinanceAndAccountancyPhrases(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectAgriculturalProduce(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectCurrenciesAndDenominations(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectMarkings(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectReligion(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextSubjectToponym(SlAbstract):
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


class SlTextCorpus(SlAbstract):
    """
    Another corpus of Texts
    E.g. 'Bamiyan Papers', 'Firuzkuh Papers'
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


class SlTextFolioAnnotationType(SlAbstract):
    """
    A type of TextFolioAnnotation.
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
    shelfmark = models.CharField(max_length=1000)
    collection = models.ForeignKey('SlTextCollection', on_delete=models.RESTRICT, related_name=related_name)
    corpus = models.ForeignKey('SlTextCorpus', on_delete=models.RESTRICT, blank=True, null=True, related_name=related_name)
    primary_language = models.ForeignKey('SlTextLanguage', on_delete=models.RESTRICT, related_name=f'{related_name}_primary')
    type = models.ForeignKey('SlTextType', on_delete=models.RESTRICT, related_name=related_name)
    correspondence = models.ForeignKey('SlTextCorrespondence', on_delete=models.RESTRICT, related_name=related_name)
    description = models.TextField()
    id_khan = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Khan ID")
    id_nicholas_simms_williams = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Nicholas Simms-Williams ID")
    country = models.ForeignKey('SlCountry', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    additional_languages = models.ManyToManyField('SlTextLanguage', blank=True, related_name=related_name, db_index=True, help_text="Don't include the primary language. Only include additional languages/scripts that also appear in the text.")
    funders = models.ManyToManyField('SlFunder', blank=True, related_name=related_name, db_index=True)
    texts = models.ManyToManyField('self', through='M2MTextToText', blank=True)

    # Subject
    # The below fields may be related to above 'type' value, e.g. Legal or Administrative so need to show/hide necessary fields in admin
    legal_transactions = models.ManyToManyField('SlTextSubjectLegalTransactions', blank=True, related_name=related_name, db_index=True)
    administrative_internal_correspondences = models.ManyToManyField('SlTextSubjectAdministrativeInternalCorrespondence', blank=True, related_name=related_name, db_index=True)
    administrative_tax_receipts = models.ManyToManyField('SlTextSubjectAdministrativeTaxReceipts', blank=True, related_name=related_name, db_index=True)
    administrative_lists_and_accounting = models.ManyToManyField('SlTextSubjectAdministrativeListsAndAccounting', blank=True, related_name=related_name, db_index=True)
    land_measurement_units = models.ManyToManyField('SlTextSubjectLandMeasurementUnits', blank=True, related_name=related_name, db_index=True)
    people_and_processes_admins = models.ManyToManyField('SlTextSubjectPeopleAndProcessesAdmin', blank=True, related_name=related_name, db_index=True, verbose_name='People and processes involved in public administration, tax, trade, and commerce')
    people_and_processes_legal = models.ManyToManyField('SlTextSubjectPeopleAndProcessesLegal', blank=True, related_name=related_name, db_index=True, verbose_name='People and processes involved in legal and judiciary system')
    documentations = models.ManyToManyField('SlTextSubjectDocumentation', blank=True, related_name=related_name, db_index=True)
    geographic_administrative_units = models.ManyToManyField('SlTextSubjectGeographicAdministrativeUnits', blank=True, related_name=related_name, db_index=True)
    legal_and_administrative_stock_phrases = models.ManyToManyField('SlTextSubjectLegalAndAdministrativeStockPhrases', blank=True, related_name=related_name, db_index=True)
    finance_and_accountancy_phrases = models.ManyToManyField('SlTextSubjectFinanceAndAccountancyPhrases', blank=True, related_name=related_name, db_index=True)
    agricultural_produce = models.ManyToManyField('SlTextSubjectAgriculturalProduce', blank=True, related_name=related_name, db_index=True, help_text='Agricultural produce, animals, and farming equipment')
    currencies_and_denominations = models.ManyToManyField('SlTextSubjectCurrenciesAndDenominations', blank=True, related_name=related_name, db_index=True)
    markings = models.ManyToManyField('SlTextSubjectMarkings', blank=True, related_name=related_name, db_index=True, help_text='Scribal markings, ciphers, abbreviations, para-text, column format')
    religions = models.ManyToManyField('SlTextSubjectReligion', blank=True, related_name=related_name, db_index=True)
    toponyms = models.ManyToManyField('SlTextSubjectToponym', blank=True, related_name=related_name, db_index=True, help_text='Place names')

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

    # Review & Approve Text to Show on Public Website
    public_review_ready = models.BooleanField(
        default=False,
        help_text='Tick this box to mark this Corpus Text as ready to be reviewed by the Principal Editor.<br>If the editor approves it, this Corpus Text will then be visible on the public website.<br>The editor will be notified via email when you tick this box.<br>You can only tick this box if a Principal Editor has been set for this Corpus Text (see the above Admin section).',  # NOQA
        verbose_name='ready to review'
    )
    public_review_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Optional. Include any necessary comments, feedback, or notes during the review process.",
        verbose_name='review notes'
    )
    public_review_approved = models.BooleanField(
        default=False,
        help_text='Tick to approve this Corpus Text. This will make it visible on the public website. You can only tick this box if you are the Principal Editor and this Corpus Text has been marked as ready to review',
        verbose_name='approved'
    )
    public_review_approved_by = models.ForeignKey(
        User,
        related_name="text_public_review_approved_by",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name='approved by'
    )
    public_review_approved_datetime = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='approved date/time'
    )

    # Admin
    admin_classification = models.ForeignKey('SlTextClassification', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name, verbose_name='Classification')
    admin_principal_editor = models.ForeignKey(
        User,
        related_name='text_admin_principal_editor',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='The main person responsible for this Corpus Text',
        verbose_name='principal editor'
    )
    admin_principal_data_entry_person = models.ForeignKey(
        User,
        related_name='text_admin_principal_data_entry_person',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='The main person who has entered the data for this Corpus Text into the database',
        verbose_name='principal data entry person'
    )
    admin_contributors = models.ManyToManyField(
        User,
        related_name='text_admin_contributors',
        blank=True,
        help_text='Users who have contributed to this Corpus Text (e.g. co-editors, data entry persons, etc.) but are not the principal editor or principal data entry person (these are specified above).<br>',
        verbose_name='contributors'
    )
    admin_commentary = models.TextField(blank=True, null=True, verbose_name='Commentary')

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
        return f"{self.primary_language.name}: {self.collection}, {self.shelfmark}. ({self.type.name})"

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
    text_folio_trans_help_text = """
To start creating lines of text click the 'numbered list' button
<br>
To manually override an automatic line number simply:
<br>
&nbsp;&nbsp;&nbsp;&nbsp;1. Click the 'Source' button
<br>
&nbsp;&nbsp;&nbsp;&nbsp;2. Add a value to the <em>&lt;li&gt;</em>. E.g. change <em>&lt;li&gt;</em> to <em>&lt;li value="4"&gt;</em>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;3. If last line is a range (e.g. 8-9) add <em>'data-range-end'</em>. E.g. <em>&lt;li data-range-end="9"&gt;</em>
"""

    text = models.ForeignKey('Text', on_delete=models.CASCADE, related_name=related_name)
    side = models.ForeignKey('SlTextFolioSide', on_delete=models.RESTRICT)
    open_state = models.ForeignKey('SlTextFolioOpen', on_delete=models.RESTRICT, blank=True, null=True, help_text='Optional. Only relevant to some Bactrian texts.')

    image = models.ImageField(upload_to='corpus/text_folios__original', blank=True, null=True)
    image_small = models.ImageField(upload_to='corpus/text_folios__small', blank=True, null=True)
    image_medium = models.ImageField(upload_to='corpus/text_folios__medium', blank=True, null=True)
    image_large = models.ImageField(upload_to='corpus/text_folios__large', blank=True, null=True)

    transcription = RichTextField(help_text=text_folio_trans_help_text)
    translation = RichTextField(blank=True, null=True, help_text=text_folio_trans_help_text)
    transliteration = RichTextField(blank=True, null=True, help_text='Optional. Only relevant to some Middle Persian texts.')

    @property
    def image_is_wider_than_tall(self):
        return image_is_wider_than_tall(self.image)

    @property
    def image_preview(self):
        return mark_safe(f'<img src="{self.image_small.url}" alt="image of this folio" />')

    def __str__(self):
        # Build the descriptors text
        descriptors = [str(field) for field in [self.side, self.open_state] if field is not None]
        descriptors_text = f' ({", ".join(descriptors)})' if len(descriptors) else ''
        # Return the string
        return f'{self.text}: Folio {descriptors_text}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Must save now, so image is saved before working with it

        # Create small, medium, and large versions of the original image
        # Update the object (must use update() not save() to avoid unique ID error)
        TextFolio.objects.filter(id=self.id).update(
            image_small=image_compress(self.image, self.image_small, 640),
            image_medium=image_compress(self.image, self.image_medium, 1920),
            image_large=image_compress(self.image, self.image_large, 5000)
        )

    class Meta:
        ordering = ['text', 'open_state', 'side', 'id']


class TextFolioAnnotation(models.Model):
    """
    A note/description of a part of a TextFolio (other than lines of text)
    e.g. damage, marks, drawings, characters, etc.
    """

    related_name = 'text_folio_parts'

    text_folio = models.ForeignKey('TextFolio', on_delete=models.CASCADE, related_name=related_name)
    type = models.ForeignKey('SlTextFolioAnnotationType', on_delete=models.CASCADE, related_name=related_name)
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
