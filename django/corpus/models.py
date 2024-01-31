from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from PIL import Image, ImageOps
from django.core.files import File
from io import BytesIO
from django.db.models.functions import Upper
from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from bs4 import BeautifulSoup
from unidecode import unidecode
import os
import textwrap


# Three main sections:
# 1. Reusable code
# 2. Select List Models
# 3. Main models


#
# 1. Reusable code
#


date_help_text = 'Format: "YYYY-MM-DD" - e.g. "0608-01-31". Please ensure years before 1000 are 4 digits long using 0s at start, e.g. 0608 not 608, 0056 not 56, etc.'


class SlAbstract(models.Model):
    """
    An abstract model for Select List models
    See: https://docs.djangoproject.com/en/4.0/topics/db/models/#abstract-base-classes
    """

    name = models.CharField(max_length=1000, db_index=True)
    name_unidecode = models.CharField(max_length=1000, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.name if self.name and self.name != "" else f"#{self.id}"

    def save(self, *args, **kwargs):
        self.name_unidecode = unidecode(self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = [Upper('name_unidecode'), 'id']


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


def queryset_to_html_list(queryset):
    """
    Returns a HTML list element (i.e. <ul></ul>), with each obj in queryset as a <li> item
    """
    if len(queryset):
        html = '<ul>'
        for obj in queryset:
            html += f'<li>{str(obj)}</li>'
        html += '</ul>'
        return html


#
# 2. Select List models (all inherit from above SlAbstract class, with some extending with additional fields, etc.)
#


class SlTextTypeCategory(SlAbstract):
    """
    A category of Text types
    E.g. 'document', 'literature'
    """
    pass

    class Meta:
        ordering = [Upper('name'), 'id']
        verbose_name_plural = 'sl text type categories'


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

    class Meta:
        ordering = [Upper('name'), 'id']
        verbose_name_plural = 'sl text document subtype categories'


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


class SlTextWritingSupport(SlAbstract):
    """
    A type of writing surface
    E.g. 'paper', 'ostraca', 'parchment'
    """
    pass


class SlTextWritingSupportDetail(SlAbstract):
    """
    Common details of writing supports
    """
    pass


class SlTextFoldLinesAlignment(SlAbstract):
    """
    How fold lines are aligned
    E.g. 'vertical', 'horizontal', 'vertical and horizontal'
    """
    pass


class SlTextCollection(SlAbstract):
    """
    A collection of Texts
    E.g. 'National Library of Israel', 'Khalili Collection', 'Sam Fogg Rate Books'
    """
    pass


class SlTextCorpus(SlAbstract):
    """
    Another corpus of Texts
    E.g. 'Bamiyan Papers', 'Firuzkuh Papers'
    """
    pass

    class Meta:
        ordering = [Upper('name'), 'id']
        verbose_name_plural = 'sl text corpus'


class SlTextClassification(SlAbstract):
    """
    The team classifies Texts based on their quality/stag of development
    E.g. 'Gold', 'Silver', 'Bronze'
    """
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    @property
    def name_full(self):
        return f'{self.name} ({self.description})'

    def __str__(self):
        return f'{self.order} - {self.name_full}'

    class Meta:
        ordering = ['order', Upper('name'), 'id']


class SlTextScript(SlAbstract):
    """
    A script that a Text was originally written in
    E.g. 'Arabic', 'Bactrian', 'New Persian'
    """
    is_written_right_to_left = models.BooleanField(default=False)


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


class SlTextToponym(SlAbstract):
    """
    A toponym (aka place name) that appears in a Text
    E.g. 'Ariz', 'Balkh'
    """
    alternative_readings = models.CharField(max_length=1000, blank=True, null=True)
    other_attested_forms = models.CharField(max_length=1000, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True, help_text='Optional. Use if you want this toponym to appear on maps in the public interface.')
    longitude = models.CharField(max_length=255, blank=True, null=True, help_text='Optional. Use if you want this toponym to appear on maps in the public interface.')
    urls = models.TextField(blank=True, null=True, help_text='Optional. Add URLs that relate to this toponym (add one URL per line). Must be a full URL e.g. "https://www.google.com"')
    notes = models.TextField(blank=True, null=True, help_text='Optional. Notes included here are only visible in admin dashboard, not on public interface.')

    @property
    def urls_as_html_links(self):
        """
        Converts the URLs in self.urls to html anchor/link tags
        E.g. https://www.google.com -> <a href="https://www.google.com">https://www.google.com</a>
        """
        if self.urls and len(self.urls):
            url_links = []
            for url in self.urls.split('\n'):
                url_clean = url.strip()
                validator = URLValidator()
                try:
                    validator(url_clean)
                    url_links.append(f'<a class="sltextfoliotag-url" href="{url_clean}">{url_clean}</a>')
                except ValidationError as e:
                    print(e)
            return mark_safe('<br>'.join(url_links))

    def __str__(self):
        str = self.name
        if self.alternative_readings:
            str += f' ({self.alternative_readings})'
        if self.other_attested_forms:
            str += f' ({self.other_attested_forms})'
        return str


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


class SlTextGregorianCentury(SlAbstract):
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
        ordering = ['century_number', 'id']
        verbose_name_plural = 'sl text centuries'


class SlPersonInTextRole(SlAbstract):
    """
    A type of person within a text.
    E.g. 'promisor', 'promisee', 'sender', 'receiver'
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


class SlTextFolioTagCategory(SlAbstract):
    """
    A category of tags of terms found in text folios
    E.g. 'Land measurement units', 'Documentations', 'Agricultural produce'
    """
    pass

    class Meta:
        ordering = [Upper('name'), 'id']
        verbose_name_plural = 'sl text folio tag categories'


class SlTextFolioTag(SlAbstract):
    """
    A tag of terms found in text folios
    """
    category = models.ForeignKey('SlTextFolioTagCategory', on_delete=models.RESTRICT, related_name='tags')

    class Meta:
        ordering = [Upper('category__name'), Upper('name'), 'id']


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


class SlSealDescription(SlAbstract):
    """
    A description/tag of a seal.
    E.g. 'bearded', 'stag'
    """
    pass


class SlSealColour(SlAbstract):
    """
    A colour of a seal.
    E.g. 'red', 'orange'
    """
    pass


class SlSealImprint(SlAbstract):
    """
    A category/imprint of a seal.
    E.g. 'animals', 'busts'
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
    texts = models.ManyToManyField('self', through='M2MTextToText', blank=True)
    toponyms = models.ManyToManyField('SlTextToponym', blank=True, related_name=related_name, db_index=True)

    # Physical Description
    writing_support = models.ForeignKey('SlTextWritingSupport', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)
    writing_support_details = models.ManyToManyField('SlTextWritingSupportDetail', blank=True, related_name=related_name, db_index=True)
    writing_support_details_additional = models.TextField(blank=True, null=True, verbose_name='additional writing support details')
    dimensions_height = models.FloatField(blank=True, null=True, verbose_name='height (cm)')
    dimensions_width = models.FloatField(blank=True, null=True, verbose_name='width (cm)')
    fold_lines_count = models.IntegerField(blank=True, null=True)
    fold_lines_alignment = models.ForeignKey('SlTextFoldLinesAlignment', blank=True, null=True, on_delete=models.RESTRICT, related_name=related_name)
    fold_lines_details = models.TextField(blank=True, null=True)

    # Content
    summary_of_content = RichTextField(blank=True, null=True)

    # Converted Gregorian Date (see child TextDate model for original dates)
    gregorian_date_text = models.CharField(max_length=1000, blank=True, null=True, help_text='Format date as free text - e.g. "11 February 1198" or "January-February 1162".<br>For help converting original dates to the Gregorian calendar please see <a href="https://www.muqawwim.com" target="_blank">www.muqawwim.com</a>')
    gregorian_date = models.CharField(max_length=1000, blank=True, null=True, help_text=date_help_text)
    gregorian_date_range_start = models.CharField(max_length=1000, blank=True, null=True, help_text=date_help_text)
    gregorian_date_range_end = models.CharField(max_length=1000, blank=True, null=True, help_text=date_help_text)
    gregorian_date_century = models.ForeignKey(SlTextGregorianCentury, on_delete=models.SET_NULL, blank=True, null=True, help_text='This century data is only used to filter and sort results in the list of Corpus Texts in the public interface. If the exact century is not known but an approximate date range is available then insert your best estimate (e.g. the middle of the date range) or leave blank if no estimate is available.')

    # Commentary
    commentary = RichTextField(blank=True, null=True, help_text='<br>Commentary will not be displayed on the public website. It is for internal project team purposes only.')

    # Review & Approve Text to Show on Public Website
    public_review_reviewer = models.ForeignKey(
        User,
        related_name="text_public_review_reviewer",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='You can only change the reviewer if you are the principal data entry person, principal editor, or the existing reviewer of this Corpus Text.',  # NOQA
        verbose_name='reviewer'
    )
    public_review_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Optional. Include any necessary comments, feedback, or notes during the review process.",
        verbose_name='review notes'
    )
    public_review_approved = models.BooleanField(
        default=False,
        help_text='Ticking this box will make this Corpus Text visible on the public website. You can only tick this box if you are the Reviewer of this Corpus Text.<br>Unticking this box will hide this Corpus Text from the public interface. You can only untick this box if you approved this Corpus Text.',
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
    admin_classification = models.ForeignKey('SlTextClassification', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name, verbose_name='classification')
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
    def has_transliteration(self):
        for folio in self.text_folios.all():
            if folio.transliteration is not None and len(folio.transliteration):
                return True

    @property
    def has_image(self):
        for folio in self.text_folios.all():
            if folio.image:
                return True

    @property
    def count_text_folios(self):
        return self.text_folios.count()

    @property
    def gregorian_date_range_str(self):
        if self.gregorian_date_range_start and self.gregorian_date_range_end:
            return f'Estimated date range: {self.gregorian_date_range_start}-{self.gregorian_date_range_end}'
        elif self.gregorian_date_range_start:
            return f'Estimated date: {self.gregorian_date_range_start}'
        elif self.gregorian_date_range_end:
            return f'Estimated date: {self.gregorian_date_range_end}'
        else:
            return ''

    @property
    def gregorian_date_full(self):
        str = f'The Gregorian calendar: {self.gregorian_date_text}'
        if self.gregorian_date:
            str += f' ({self.gregorian_date})'
        if len(self.gregorian_date_range_str):
            str += f' ({self.gregorian_date_range_str})'
        return str

    @property
    def image_permission_statement(self):
        if self.has_image and self.collection:
            return f"""Images of this Text displayed on this web page are provided by {self.collection}.
            <br>
            © {self.collection}, All rights reserved.
            <br>
            If you wish to reproduce these images please contact {self.collection}."""

    @property
    def summary_of_content_preview(self):
        return textwrap.shorten(self.summary_of_content, width=350, placeholder="...")

    @property
    def list_image(self):
        # Return the first image of a folio, if exists
        for folio in self.text_folios.all():
            if folio.image:
                return folio.image_small

    @property
    def details_html_dates(self):
        if len(self.text_dates.all()):
            html = '<ul>'
            for date in self.text_dates.all():
                html += f'<li>{date}</li>'
            html += '</ul>'
            return html

    @property
    def details_html_person_in_text(self):
        if len(self.persons_in_texts.all()):
            html = '<ul>'
            for person in self.persons_in_texts.all():
                html += f'<li>{person.person.name}'
                html += f' ({person.person_name_in_text})' if person.person_name_in_text else ''
                html += f' ({person.person_role_in_text})' if person.person_role_in_text else ''
                html += '</li>'
            html += '</ul>'
            return html

    @property
    def details_html_publications(self):
        if len(self.text_related_publications.all()):
            html = '<ul>'
            for publication in self.text_related_publications.all():
                html += f'<li>{publication.publication}'
                html += f' (Pages: {publication.pages})' if publication.pages else ''
                html += f' (Catalogue Number: {publication.catalogue_number})' if publication.catalogue_number else ''
                html += '</li>'
            html += '</ul>'
            return html

    @property
    def details_html_texts(self):
        if len(self.texts.all()):
            html = '<ul>'
            for text in self.texts.all():
                html += f'<li><a href="{reverse("corpus:text-detail", args=[str(text.id)])}">{text}</a></li>'
            html += '</ul>'
            return html

    @property
    def title(self):
        return f"{self.primary_language.name}: {self.collection}, {self.shelfmark}"

    def get_absolute_url(self):
        return reverse('corpus:text-detail', args=[str(self.id)])

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
    date_text = models.CharField(max_length=1000, blank=True, null=True, help_text="""Format date as free text - e.g. 10 Ramaḍān 605
    <br><br><br>
    <table>
        <tr><th>Number</th><th>Hebrew Month</th><th>Hijri Month</th></tr>
        <tr><td>1</td><td dir="rtl">תשרי (Tishrei)</td><td dir="rtl">محرم (al-Muḥarram)</td></tr>
        <tr><td>2</td><td dir="rtl">חשון (Cheshvan)</td><td dir="rtl">صفر (Ṣafar)</td></tr>
        <tr><td>3</td><td dir="rtl">כסלו (Kislev)</td><td dir="rtl">ربيع الأول (Rabīʿ al-Awwal)</td></tr>
        <tr><td>4</td><td dir="rtl">טבת (Tevet)</td><td dir="rtl">ربيع الثاني (Rabīʿ al-Thānī)</td></tr>
        <tr><td>5</td><td dir="rtl">שבט (Shevat)</td><td dir="rtl">جمادى الأولى (Jumādā al-Ūlā)</td></tr>
        <tr><td>6</td><td dir="rtl">אדר (Adar)</td><td dir="rtl">جمادى الثانية (Jumādā al-Thānī)</td></tr>
        <tr><td>7</td><td dir="rtl">ניסן (Nisan)</td><td dir="rtl">رجب (Rajab)</td></tr>
        <tr><td>8</td><td dir="rtl">אייר (Iyar)</td><td dir="rtl">شعبان (Shaʿbān)</td></tr>
        <tr><td>9</td><td dir="rtl">סיון (Sivan)</td><td dir="rtl">رمضان (Ramaḍān)</td></tr>
        <tr><td>10</td><td dir="rtl">תמוז (Tammuz)</td><td dir="rtl">شوال (Shawwāl)</td></tr>
        <tr><td>11</td><td dir="rtl">אב (Av)</td><td dir="rtl">ذو القعدة (Dhū al-Qaʿda)</td></tr>
        <tr><td>12</td><td dir="rtl">אלול (Elul)</td><td dir="rtl">ذو الحجة (Dhū al-Ḥijja)</td></tr>
    </table>""")
    date = models.CharField(max_length=1000, blank=True, null=True, help_text=date_help_text)
    date_range_start = models.CharField(max_length=1000, blank=True, null=True, help_text=date_help_text)
    date_range_end = models.CharField(max_length=1000, blank=True, null=True, help_text=date_help_text)

    @property
    def date_range_str(self):
        if self.date_range_start and self.date_range_end:
            return f'Estimated date range: {self.date_range_start}-{self.date_range_end}'
        elif self.date_range_start:
            return f'Estimated date: {self.date_range_start}'
        elif self.date_range_end:
            return f'Estimated date: {self.date_range_end}'
        else:
            return ''

    def __str__(self):
        str = f'{self.calendar.name_full}: {self.date_text}'
        if self.date:
            str += f' ({self.date})'
        if len(self.date_range_str):
            str += f' ({self.date_range_str})'
        return str

    class Meta:
        verbose_name = 'Date'
        verbose_name_plural = 'Original Dates'


class TextRelatedPublication(models.Model):
    """
    A related publication of a Text
    """

    related_name = 'text_related_publications'

    text = models.ForeignKey('Text', on_delete=models.CASCADE, related_name=related_name)
    publication = models.ForeignKey('SlTextPublication', on_delete=models.RESTRICT, related_name=related_name)
    pages = models.CharField(max_length=1000, blank=True, null=True, help_text='Specify the page number or range of page numbers - e.g. 4, 82-84, etc.')
    catalogue_number = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name = 'Related Publication'


class TextFolio(models.Model):
    """
    A folio (e.g. a side of paper) within a Text
    """

    related_name = 'text_folios'
    text_folio_trans_help_text = """<br><br>Lines of text:<br>
To start creating lines of text click the 'numbered list' button
<br>
To manually override an automatic line number simply:
<br>
&nbsp;&nbsp;&nbsp;&nbsp;1. Click the 'Source' button
<br>
&nbsp;&nbsp;&nbsp;&nbsp;2. Add a value to the <em>&lt;li&gt;</em>. E.g. change <em>&lt;li&gt;</em> to <em>&lt;li value="4"&gt;</em>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;3. If last line is a range (e.g. 8-9) add <em>'data-range-end'</em>. E.g. <em>&lt;li data-range-end="9"&gt;</em>
<br>
<br>
Tables:
<br>
To add a table, click on the table button in the toolbar
<br>
You can edit/delete an existing table (e.g. add/remove a row/column) by right clicking the table and choosing the appropriate option
<br>
If you add a new list of line numbers below a table, please note that you'll need to set the line number by adding the value attribute to the first <em>&lt;li&gt;</em> as described above (e.g. <em>&lt;li value="4"&gt;</em>)
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
    transliteration = RichTextField(blank=True, null=True, help_text='<br>Optional. Only relevant to some Middle Persian texts.')

    def trans_text_lines(self, text_field, field_name):
        """
        Takes the specified trans text field (e.g. one of transcription, translation, transliteration)
        and generates a list of dictionaries containing data about each line that's necessary
        to generate the HTML to display on the public interface

        Each of these fields should have a related property that calls this method like so:
        @property
        def transcription_text_lines(self):
            return self.trans_text_lines(self.transcription, 'transcription')
        """

        # Ensure the text field includes a HTML ordered list with items or a table
        if (('<ol' in text_field and '</li>' in text_field) or '<table' in text_field) and field_name in ['transcription', 'translation', 'transliteration']:
            lines_data = []
            soup = BeautifulSoup(text_field, features="html.parser")
            lines = soup.find_all(['li', 'table'])
            rtl = self.text.primary_language.script.is_written_right_to_left and field_name == 'transcription'
            line_number = 0
            line_index = -1

            for line in lines:

                # Lines that are <li> elements (aka list items in a <ol> element, aka standard lines of text)
                if str(line).startswith('<li'):

                    # Increase the line index for each line
                    line_index += 1

                    # Line number
                    try:
                        line_number = int(line.attrs['value'])
                    except KeyError:
                        line_number += 1
                    # Line number range end
                    try:
                        # If the next line has a value attribute that's greater than 1 more than current line count then
                        next_line_number = int(lines[line_index + 1].attrs['value'])
                        if line_number < (next_line_number - 1):
                            line_number_range_end = next_line_number - 1
                    except (IndexError, KeyError):
                        try:
                            # Try getting the current line's 'data-range-end' attribute (valid if this is the last line)
                            line_number_range_end = int(line.attrs['data-range-end'])
                        except KeyError:
                            line_number_range_end = None
                    # Line number label
                    line_number_label = f'{line_number}-{line_number_range_end}' if line_number_range_end else str(line_number)
                    # Line numbers (e.g. if line number label is 4-6 then line numbers is 4,5,6)
                    line_numbers = ','.join([str(ln) for ln in range(line_number, line_number_range_end + 1)]) if line_number_range_end else line_number

                    # Image part data
                    try:
                        # Get attr values from line li element
                        image_part_left = line.attrs['data-imagepartleft']
                        image_part_top = line.attrs['data-imageparttop']
                        image_part_width = line.attrs['data-imagepartwidth']
                        image_part_height = line.attrs['data-imagepartheight']

                        # Build new attributes to add to new line div element (if provided)
                        image_part_left_attr = f' data-imagepartleft={image_part_left}' if image_part_left else ''
                        image_part_top_attr = f' data-imageparttop={image_part_top}' if image_part_top else ''
                        image_part_width_attr = f' data-imagepartwidth={image_part_width}' if image_part_width else ''
                        image_part_height_attr = f' data-imagepartheight={image_part_height}' if image_part_height else ''
                    except KeyError:
                        # Set empty attributes
                        image_part_left_attr = ''
                        image_part_top_attr = ''
                        image_part_width_attr = ''
                        image_part_height_attr = ''

                    # Build dict for this line and add to list of lines data
                    lines_data.append({
                        'lineNumbers': line_numbers,
                        'lineIndex': line_index,
                        'trans': field_name,
                        'folio': self.id,
                        'image_part_left_attr': image_part_left_attr,
                        'image_part_top_attr': image_part_top_attr,
                        'image_part_width_attr': image_part_width_attr,
                        'image_part_height_attr': image_part_height_attr,
                        'lineNumberLabel': line_number_label,
                        'rtl': rtl,
                        'text': "".join([str(t) for t in line.contents])
                    })

                # Lines that are a <table> element (e.g. witness tables, etc.)
                elif str(line).startswith('<table'):
                    # Process all <td> elements in table
                    for td in line.find_all('td'):
                        # Increase the line index for each td, as each td is considered a 'line' (i.e. can draw each td on an image and highlight each td on hover)
                        line_index += 1
                        # Assign
                        td['class'] = 'folio-lines-line'
                        td['dir'] = 'auto'
                        td['data-linenumbers'] = ''
                        td['data-lineindex'] = line_index
                        td['data-trans'] = field_name
                        td['data-folio'] = self.id
                    # Add a new td containing the line number at the start of each row
                    for tr_index, tr in enumerate(line.find_all('tr')):
                        line_number_td = soup.new_tag('td', **{'class': 'line-number', 'dir': f'{"rtl" if rtl else "auto"}'})
                        # Line number: if this <table> is first element in whole trans text
                        if len(lines_data) == 0:
                            tr_number = 1 + tr_index
                        # Line number: if previous item in lines_data is a <li>
                        elif 'lineNumbers' in lines_data[-1]:
                            tr_number = int(str(lines_data[-1]['lineNumbers']).split(',')[-1]) + 1 + tr_index
                        # Line number: all other cases (e.g. if previous item in lines_data is another table)
                        else:
                            tr_number += 1
                        line_number_td.string = str(tr_number)
                        tr.insert(0, line_number_td)

                    # Build the html for the table and add it to lines_data
                    table_html = f'<table class="folio-table{(" rtl" if rtl else "")}">{"".join([str(tag) for tag in line])}</table>'

                    # Add related lines
                    if field_name != 'transcription':
                        table_html += '<div class="related-lines" data-trans="transcription"></div>'
                    if field_name != 'translation':
                        table_html += '<div class="related-lines" data-trans="translation"></div>'
                    if field_name != 'transliteration':
                        table_html += '<div class="related-lines" data-trans="transliteration"></div>'

                    lines_data.append({'table': table_html})

            return lines_data

    @property
    def transcription_text_lines(self):
        return self.trans_text_lines(self.transcription, 'transcription')

    @property
    def translation_text_lines(self):
        return self.trans_text_lines(self.translation, 'translation')

    @property
    def transliteration_text_lines(self):
        return self.trans_text_lines(self.transliteration, 'transliteration')

    @property
    def image_is_wider_than_tall(self):
        return image_is_wider_than_tall(self.image)

    @property
    def image_preview(self):
        return mark_safe(f'<img src="{self.image_small.url}" alt="image of this folio" />')

    @property
    def name_short(self):
        return ", ".join([str(field) for field in [self.open_state, self.side] if field is not None])

    def __str__(self):
        return f'{self.text}: Folio ({self.name_short})'

    def save(self, *args, **kwargs):
        # Must save now, so image is saved before working with it
        super().save(*args, **kwargs)

        # Create small, medium, and large versions of the original image
        # Update the object (must use update() not save() to avoid unique ID error)
        try:
            TextFolio.objects.filter(id=self.id).update(
                image_small=image_compress(self.image, self.image_small, 640),
                image_medium=image_compress(self.image, self.image_medium, 1920),
                image_large=image_compress(self.image, self.image_large, 5000)
            )
        except FileNotFoundError as f:
            print(f)

    class Meta:
        ordering = ['text', 'open_state', 'side', 'id']
        verbose_name = 'Folio'
        verbose_name_plural = 'Folios (including Transcription, Translation, Images, etc.)'


class TextFolioTag(models.Model):
    """
    A tag of a term within a TextFolio, using tags specified in SlTextFolioTag
    """

    related_name = 'text_folio_tags'

    text_folio = models.ForeignKey('TextFolio', on_delete=models.CASCADE, related_name=related_name)
    tag = models.ForeignKey('SlTextFolioTag', on_delete=models.CASCADE, related_name=related_name)
    details = models.TextField(blank=True, null=True)
    # Image part measurements
    # left and top are the x,y coordinates of the top-left starting point of the part in the image
    image_part_left = models.FloatField(blank=True, null=True)
    image_part_top = models.FloatField(blank=True, null=True)
    image_part_width = models.FloatField(blank=True, null=True)
    image_part_height = models.FloatField(blank=True, null=True)
    # Metadata
    meta_created_by = models.ForeignKey(
        User,
        related_name="textfoliotag_created_by",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="created by"
    )
    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name="created")
    meta_lastupdated_by = models.ForeignKey(
        User,
        related_name="textfoliotag_lastupdated_by",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="last updated by"
    )
    meta_lastupdated_datetime = models.DateTimeField(blank=True, null=True, verbose_name="last updated")

    @property
    def is_drawn_on_text_folio_image(self):
        return self.image_part_left is not None

    @property
    def is_in_text_folio_transcription(self):
        return self.text_folio.transcription and f'data-textfoliotag="{self.id}"' in self.text_folio.transcription

    @property
    def is_in_text_folio_translation(self):
        return self.text_folio.translation and f'data-textfoliotag="{self.id}"' in self.text_folio.translation

    @property
    def is_in_text_folio_transliteration(self):
        return self.text_folio.transliteration and f'data-textfoliotag="{self.id}"' in self.text_folio.transliteration

    class Meta:
        ordering = ['text_folio', Upper('tag__category__name'), Upper('tag__name'), 'id']


class Person(models.Model):
    """
    A Person that appears in a Text
    """

    name = models.CharField(max_length=1000)
    name_unidecode = models.CharField(max_length=1000, blank=True, null=True)
    gender = models.ForeignKey('SlPersonGender', on_delete=models.CASCADE, blank=True, null=True)
    profession = models.CharField(max_length=1000, blank=True, null=True, verbose_name='profession or professional title')
    persons = models.ManyToManyField('self', through='M2MPersonToPerson', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name_unidecode = unidecode(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = [Upper('name_unidecode'), 'id']


class PersonInText(models.Model):
    """
    An instance of a Person appearing within a Text
    """

    related_name = 'persons_in_texts'

    text = models.ForeignKey('Text', on_delete=models.CASCADE, related_name=related_name)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name=related_name, help_text="Be sure to search the list before adding a new person. We do not want duplicate records.")
    person_name_in_text = models.CharField(max_length=1000, blank=True, null=True, help_text='If Person is named differently in Text than in this database then record their name in the Text here', verbose_name='person name (as it appears in this text)')
    person_role_in_text = models.ForeignKey('SlPersonInTextRole', on_delete=models.SET_NULL, blank=True, null=True, related_name=related_name)

    def __str__(self):
        str = f'{self.text.title}: {self.person.name}'
        if self.person_role_in_text:
            str += f' ({self.person_role_in_text.name})'
        return str

    class Meta:
        verbose_name = 'Person in Text'
        verbose_name_plural = 'Persons in Text'


class Seal(models.Model):
    """
    Lerner Seals
    """

    related_name = 'seals'

    text = models.ForeignKey('Text', on_delete=models.CASCADE, related_name=related_name)
    type = models.CharField(max_length=1000, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    inscription = models.TextField(blank=True, null=True)
    measurements = models.CharField(max_length=1000, blank=True, null=True, verbose_name='measurements (mm)', help_text='e.g. 28 x 23 x 16; 13 x 12')
    descriptions = models.ManyToManyField('SlSealDescription', blank=True)
    colours = models.ManyToManyField('SlSealColour', blank=True)
    imprints = models.ManyToManyField('SlSealImprint', blank=True)
    image = models.ImageField(upload_to='corpus/seals__original', blank=True, null=True)
    image_small = models.ImageField(upload_to='corpus/seals__small', blank=True, null=True)

    @property
    def descriptions_html_list(self):
        return queryset_to_html_list(self.descriptions.all())

    @property
    def colours_html_list(self):
        return queryset_to_html_list(self.colours.all())

    @property
    def imprints_html_list(self):
        return queryset_to_html_list(self.imprints.all())

    @property
    def image_preview(self):
        return mark_safe(f'<img src="{self.image_small.url}" alt="image of this seal" />')

    def save(self, *args, **kwargs):
        # Must save now, so image is saved before working with it
        super().save(*args, **kwargs)

        # Create small versions of the original image
        # Update the object (must use update() not save() to avoid unique ID error)
        Seal.objects.filter(id=self.id).update(
            image_small=image_compress(self.image, self.image_small, 1000)
        )

    class Meta:
        ordering = ['text', 'type', 'id']
        verbose_name = 'Seal'
        verbose_name_plural = 'Seals (only applicable to Bactrian texts)'


# Many to Many Relationships


class M2MPersonToPerson(models.Model):
    """
    Many to many relationship between 2x Person objects
    """
    person_1 = models.ForeignKey(Person, related_name='person_1', on_delete=models.CASCADE, verbose_name='person')
    person_2 = models.ForeignKey(Person, related_name='person_2', on_delete=models.CASCADE, verbose_name='person')
    relationship_type = models.ForeignKey(SlM2MPersonToPersonRelationshipType, on_delete=models.SET_NULL, blank=True, null=True)
    relationship_details = models.CharField(max_length=1000, blank=True, null=True)


class M2MTextToText(models.Model):
    """
    Many to many relationship between 2x Text objects
    """
    text_1 = models.ForeignKey(Text, related_name='text_1', on_delete=models.CASCADE, verbose_name='text')
    text_2 = models.ForeignKey(Text, related_name='text_2', on_delete=models.CASCADE, verbose_name='text')
    relationship_type = models.ForeignKey(SlM2MTextToTextRelationshipType, on_delete=models.SET_NULL, blank=True, null=True)
    relationship_details = models.CharField(max_length=1000, blank=True, null=True)
