from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe
from PIL import Image, ImageOps
from django.core.files import File
from io import BytesIO
from django.db.models.functions import Upper
from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import os
import textwrap


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
    A category of Text types
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


class SlTextDocumentSubtypeCategory(SlAbstract):
    """
    A category of subtypes of Texts that are documents
    E.g. 'administrative', 'legal'
    """
    pass


class SlTextDocumentSubtype(SlAbstract):
    """
    A subtype of Texts that are documents
    E.g. 'legal', 'letter'
    """
    category = models.ForeignKey('SlTextDocumentSubtypeCategory', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.category.name}: {self.name}' if self.category else self.name

    class Meta:
        ordering = [Upper('category__name'), Upper('name'), 'id']


class SlTextTagLandMeasurementUnits(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTagPeopleAndProcessesAdmin(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTagPeopleAndProcessesLegal(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTagDocumentation(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTagGeographicAdministrativeUnits(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTagLegalAndAdministrativeStockPhrases(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTagFinanceAndAccountancyPhrases(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTagAgriculturalProduce(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTagCurrenciesAndDenominations(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTagMarkings(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTagReligion(SlAbstract):
    """
    A Text type related field
    """
    pass


class SlTextTagToponym(SlAbstract):
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


class SlTextPublication(SlAbstract):
    """
    A statement about who has published a Text
    E.g. 'Khan, Geoffrey. 2007. Arabic documents from early Islamic Khurasan (Studies in the Khalili Collection Volume V). London: The Nour Foundation in association with Azimuth Editions.'
    """
    pass


class SlCalendar(SlAbstract):
    """
    A calendar/date system.
    E.g. 'Gregorian', 'Hijri', 'Bactrian'
    """
    name_full = models.CharField(max_length=100, blank=True, null=True)


class SlTextCentury(SlAbstract):
    """
    A century in Gregorian calendar CE.
    E.g. 1st Century CE ... 21st Century CE
    """

    century_number = models.IntegerField(validators=[MaxValueValidator(21), MinValueValidator(1)])

    @property
    def html_select_value_field(self):
        """
        The field to be used as the value in the <option value=""> for select html elements. 'id' used by default.
        """
        return self.century_number

    class Meta:
        ordering = ['century_number']


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
    shelfmark = models.CharField(max_length=1000, help_text="If this Corpus Text doesn't have a shelfmark then insert another value here to use as a title, such as a catalogue number or a brief description. If this Corpus Text is part of reused sheet that shares a shelfmark with another Corpus Text then append 'recto' or 'verso' to this shelfmark.", verbose_name="Shelfmark / Title")
    collection = models.ForeignKey('SlTextCollection', on_delete=models.RESTRICT, related_name=related_name)
    corpus = models.ForeignKey('SlTextCorpus', on_delete=models.RESTRICT, blank=True, null=True, related_name=related_name)
    primary_language = models.ForeignKey('SlTextLanguage', on_delete=models.RESTRICT, related_name=f'{related_name}_primary')
    additional_languages = models.ManyToManyField('SlTextLanguage', blank=True, related_name=related_name, db_index=True, help_text="Don't include the primary language. Only include additional languages/scripts that also appear in the text.")
    type = models.ForeignKey('SlTextType', blank=True, null=True, on_delete=models.RESTRICT, related_name=related_name)
    document_subtype = models.ForeignKey('SlTextDocumentSubtype', blank=True, null=True, on_delete=models.RESTRICT, related_name=related_name, help_text='If a type of Administrative or Legal is selected for this Corpus Text, please also provide the subtype')
    century = models.ForeignKey(SlTextCentury, on_delete=models.SET_NULL, blank=True, null=True, help_text='Uses the Gregorian calendar. This is used to filter and sort results in the public interface. If only a date range is available then select the century in the middle of the range. More specific data about dates can be found below in the "Text Dates" section of this form.')
    texts = models.ManyToManyField('self', through='M2MTextToText', blank=True)

    # Content
    summary_of_content = RichTextField(blank=True, null=True)

    # Tags of Terms in Text
    land_measurement_units = models.ManyToManyField('SlTextTagLandMeasurementUnits', blank=True, related_name=related_name, db_index=True)
    people_and_processes_admins = models.ManyToManyField('SlTextTagPeopleAndProcessesAdmin', blank=True, related_name=related_name, db_index=True, verbose_name='People and processes involved in public administration, tax, trade, and commerce')
    people_and_processes_legal = models.ManyToManyField('SlTextTagPeopleAndProcessesLegal', blank=True, related_name=related_name, db_index=True, verbose_name='People and processes involved in legal and judiciary system')
    documentations = models.ManyToManyField('SlTextTagDocumentation', blank=True, related_name=related_name, db_index=True)
    geographic_administrative_units = models.ManyToManyField('SlTextTagGeographicAdministrativeUnits', blank=True, related_name=related_name, db_index=True)
    legal_and_administrative_stock_phrases = models.ManyToManyField('SlTextTagLegalAndAdministrativeStockPhrases', blank=True, related_name=related_name, db_index=True)
    finance_and_accountancy_phrases = models.ManyToManyField('SlTextTagFinanceAndAccountancyPhrases', blank=True, related_name=related_name, db_index=True)
    agricultural_produce = models.ManyToManyField('SlTextTagAgriculturalProduce', blank=True, related_name=related_name, db_index=True, help_text='Agricultural produce, animals, and farming equipment')
    currencies_and_denominations = models.ManyToManyField('SlTextTagCurrenciesAndDenominations', blank=True, related_name=related_name, db_index=True)
    markings = models.ManyToManyField('SlTextTagMarkings', blank=True, related_name=related_name, db_index=True, help_text='Scribal markings, ciphers, abbreviations, para-text, column format')
    religions = models.ManyToManyField('SlTextTagReligion', blank=True, related_name=related_name, db_index=True)
    toponyms = models.ManyToManyField('SlTextTagToponym', blank=True, related_name=related_name, db_index=True, help_text='Place names')

    # Physical Description
    writing_support = models.ForeignKey('SlTextWritingSupport', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    writing_support_details = models.TextField(blank=True, null=True)
    dimensions_height = models.FloatField(blank=True, null=True, verbose_name='height (cm)')
    dimensions_width = models.FloatField(blank=True, null=True, verbose_name='width (cm)')
    fold_lines_details = models.TextField(blank=True, null=True)
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
    def has_transcription(self):
        for folio in self.text_folios.all():
            if folio.transcription is not None and len(folio.transcription):
                return True

    @property
    def has_translation(self):
        for folio in self.text_folios.all():
            if folio.translation is not None and len(folio.translation):
                return True

    @property
    def count_text_folios(self):
        return self.text_folios.count()

    @property
    def summary_of_content_preview(self):
        return textwrap.shorten(self.summary_of_content, width=350, placeholder="...")

    @property
    def list_image(self):
        # Return the first image of a folio, if exists
        return self.text_folios.first().image_small

    @property
    def title(self):
        return f"{self.primary_language.name}: {self.collection}, {self.shelfmark}"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Corpus Text'


class TextDate(models.Model):
    """
    A date of a Text
    """

    date_help_text = 'Format date as: YYYY-MM-DD - e.g. 0605-01-31'
    related_name = 'text_dates'

    text = models.ForeignKey('Text', on_delete=models.CASCADE, related_name=related_name)
    calendar = models.ForeignKey('SlCalendar', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    date_text = models.CharField(max_length=1000, blank=True, null=True, help_text='Format date as free text - e.g. 10 Ramaḍān 605, 11 Feb 1198')
    date = models.CharField(max_length=1000, blank=True, null=True, help_text=date_help_text)
    date_range_start = models.CharField(max_length=1000, blank=True, null=True, help_text=date_help_text)
    date_range_end = models.CharField(max_length=1000, blank=True, null=True, help_text=date_help_text)


class TextRelatedPublication(models.Model):
    """
    A related publication of a Text
    """

    related_name = 'text_related_publications'

    text = models.ForeignKey('Text', on_delete=models.CASCADE, related_name=related_name)
    publication = models.ForeignKey('SlTextPublication', on_delete=models.RESTRICT, related_name=related_name)
    pages = models.CharField(max_length=1000, blank=True, null=True, help_text='Specify the page number or range of page numbers - e.g. 4, 82-84, etc.')


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

    transcription = RichTextField(blank=True, null=True, help_text=text_folio_trans_help_text)
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
        verbose_name = 'Text Folio (including Transcription, Translation, Images, etc.)'
        verbose_name_plural = verbose_name


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
