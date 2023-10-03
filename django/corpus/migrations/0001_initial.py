# Generated by Django 4.2.4 on 2023-10-03 06:16

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='M2MPersonToPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_details', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='M2MTextToText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_details', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('profession', models.CharField(blank=True, max_length=1000, null=True, verbose_name='profession or professional title')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
            },
        ),
        migrations.CreateModel(
            name='SlCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
                ('name_full', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlM2MPersonToPersonRelationshipType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlM2MTextToTextRelationshipType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlPersonGender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlPersonInTextRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlSealColour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlSealDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlSealImprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTextClassification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
                ('description', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['order', django.db.models.functions.text.Upper('name'), 'id'],
            },
        ),
        migrations.CreateModel(
            name='SlTextCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTextCorpus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'sl text corpus',
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
            },
        ),
        migrations.CreateModel(
            name='SlTextDocumentSubtype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('category__name'), django.db.models.functions.text.Upper('name'), 'id'],
            },
        ),
        migrations.CreateModel(
            name='SlTextDocumentSubtypeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'sl text document subtype categories',
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
            },
        ),
        migrations.CreateModel(
            name='SlTextFoldLinesAlignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTextFolioOpen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTextFolioSide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTextFolioTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
                ('latitude', models.CharField(blank=True, help_text='Optional. Use if this tag can be located on a map (e.g. is a toponym)', max_length=255, null=True)),
                ('longitude', models.CharField(blank=True, help_text='Optional. Use if this tag can be located on a map (e.g. is a toponym)', max_length=255, null=True)),
                ('urls', models.TextField(blank=True, help_text='Optional. Add URLs that relate to this tag (add one URL per line). Must be a full URL e.g. "https://www.google.com"', null=True)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('category__name'), django.db.models.functions.text.Upper('name'), 'id'],
            },
        ),
        migrations.CreateModel(
            name='SlTextFolioTagCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'sl text folio tag categories',
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
            },
        ),
        migrations.CreateModel(
            name='SlTextGregorianCentury',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
                ('century_number', models.IntegerField(validators=[django.core.validators.MaxValueValidator(21), django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name_plural': 'sl text centuries',
                'ordering': ['century_number', 'id'],
            },
        ),
        migrations.CreateModel(
            name='SlTextLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTextPublication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTextScript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
                ('is_written_right_to_left', models.BooleanField(default=False)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTextType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTextTypeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'sl text type categories',
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
            },
        ),
        migrations.CreateModel(
            name='SlTextWritingSupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTextWritingSupportDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTranslationLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shelfmark', models.CharField(help_text="If this Corpus Text doesn't have a shelfmark then insert another value here to use as a title, such as a catalogue number or a brief description. If this Corpus Text is part of reused sheet that shares a shelfmark with another Corpus Text then append 'recto' or 'verso' to this shelfmark.", max_length=1000, verbose_name='Shelfmark / Title')),
                ('writing_support_details_additional', models.TextField(blank=True, null=True, verbose_name='additional writing support details')),
                ('dimensions_height', models.FloatField(blank=True, null=True, verbose_name='height (cm)')),
                ('dimensions_width', models.FloatField(blank=True, null=True, verbose_name='width (cm)')),
                ('fold_lines_count', models.IntegerField(blank=True, null=True)),
                ('fold_lines_details', models.TextField(blank=True, null=True)),
                ('summary_of_content', ckeditor.fields.RichTextField(blank=True, help_text='Always paste content without formatting (Windows: Ctrl + Shift + V, Mac: Cmd + Shift + V)', null=True)),
                ('gregorian_date_text', models.CharField(blank=True, help_text='Format date as free text - e.g. 11 Feb 1198.<br>For help converting original dates to the Gregorian calendar please see <a href="https://www.muqawwim.com" target="_blank">www.muqawwim.com</a>', max_length=1000, null=True)),
                ('gregorian_date', models.CharField(blank=True, help_text='Format: "YYYY-MM-DD" - e.g. "0608-01-31". Please ensure years before 1000 are 4 digits long using 0s at start, e.g. 0608 not 608, 0056 not 56, etc.', max_length=1000, null=True)),
                ('gregorian_date_range_start', models.CharField(blank=True, help_text='Format: "YYYY-MM-DD" - e.g. "0608-01-31". Please ensure years before 1000 are 4 digits long using 0s at start, e.g. 0608 not 608, 0056 not 56, etc.', max_length=1000, null=True)),
                ('gregorian_date_range_end', models.CharField(blank=True, help_text='Format: "YYYY-MM-DD" - e.g. "0608-01-31". Please ensure years before 1000 are 4 digits long using 0s at start, e.g. 0608 not 608, 0056 not 56, etc.', max_length=1000, null=True)),
                ('commentary', ckeditor.fields.RichTextField(blank=True, help_text='Always paste content without formatting (Windows: Ctrl + Shift + V, Mac: Cmd + Shift + V)<br>Commentary will not be displayed on the public website. It is for internal project team purposes only.', null=True)),
                ('public_review_notes', models.TextField(blank=True, help_text='Optional. Include any necessary comments, feedback, or notes during the review process.', null=True, verbose_name='review notes')),
                ('public_review_approved', models.BooleanField(default=False, help_text='Ticking this box will make this Corpus Text visible on the public website. You can only tick this box if you are the Reviewer of this Corpus Text.<br>Unticking this box will hide this Corpus Text from the public interface. You can only untick this box if you approved this Corpus Text.', verbose_name='approved')),
                ('public_review_approved_datetime', models.DateTimeField(blank=True, null=True, verbose_name='approved date/time')),
                ('meta_created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('meta_lastupdated_datetime', models.DateTimeField(blank=True, null=True, verbose_name='last updated')),
                ('additional_languages', models.ManyToManyField(blank=True, db_index=True, help_text="Don't include the primary language. Only include additional languages/scripts that also appear in the text.", related_name='texts', to='corpus.sltextlanguage')),
                ('admin_classification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='texts', to='corpus.sltextclassification', verbose_name='classification')),
                ('admin_contributors', models.ManyToManyField(blank=True, help_text='Users who have contributed to this Corpus Text (e.g. co-editors, data entry persons, etc.) but are not the principal editor or principal data entry person (these are specified above).<br>', related_name='text_admin_contributors', to=settings.AUTH_USER_MODEL, verbose_name='contributors')),
                ('admin_principal_data_entry_person', models.ForeignKey(blank=True, help_text='The main person who has entered the data for this Corpus Text into the database', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_admin_principal_data_entry_person', to=settings.AUTH_USER_MODEL, verbose_name='principal data entry person')),
                ('admin_principal_editor', models.ForeignKey(blank=True, help_text='The main person responsible for this Corpus Text', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_admin_principal_editor', to=settings.AUTH_USER_MODEL, verbose_name='principal editor')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='texts', to='corpus.sltextcollection')),
                ('corpus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='texts', to='corpus.sltextcorpus')),
                ('document_subtype', models.ForeignKey(blank=True, help_text='If a type of Administrative or Legal is selected for this Corpus Text, please also provide the subtype', null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='texts', to='corpus.sltextdocumentsubtype')),
                ('fold_lines_alignment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='texts', to='corpus.sltextfoldlinesalignment')),
                ('gregorian_date_century', models.ForeignKey(blank=True, help_text='This century data is only used to filter and sort results in the list of Corpus Texts in the public interface. If the exact century is not known but an approximate date range is available then insert your best estimate (e.g. the middle of the date range) or leave blank if no estimate is available.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='corpus.sltextgregoriancentury')),
                ('meta_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('meta_lastupdated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_lastupdated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
                ('primary_language', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='texts_primary', to='corpus.sltextlanguage')),
                ('public_review_approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_public_review_approved_by', to=settings.AUTH_USER_MODEL, verbose_name='approved by')),
                ('public_review_reviewer', models.ForeignKey(blank=True, help_text='You can only change the reviewer if you are the principal data entry person, principal editor, or the existing reviewer of this Corpus Text.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_public_review_reviewer', to=settings.AUTH_USER_MODEL, verbose_name='reviewer')),
                ('texts', models.ManyToManyField(blank=True, through='corpus.M2MTextToText', to='corpus.text')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='texts', to='corpus.sltexttype')),
                ('writing_support', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='texts', to='corpus.sltextwritingsupport')),
                ('writing_support_details', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextwritingsupportdetail')),
            ],
            options={
                'verbose_name': 'Corpus Text',
            },
        ),
        migrations.CreateModel(
            name='TextFolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='corpus/text_folios__original')),
                ('image_small', models.ImageField(blank=True, null=True, upload_to='corpus/text_folios__small')),
                ('image_medium', models.ImageField(blank=True, null=True, upload_to='corpus/text_folios__medium')),
                ('image_large', models.ImageField(blank=True, null=True, upload_to='corpus/text_folios__large')),
                ('transcription', ckeditor.fields.RichTextField(blank=True, help_text='Always paste content without formatting (Windows: Ctrl + Shift + V, Mac: Cmd + Shift + V)<br>\nTo start creating lines of text click the \'numbered list\' button\n<br>\nTo manually override an automatic line number simply:\n<br>\n&nbsp;&nbsp;&nbsp;&nbsp;1. Click the \'Source\' button\n<br>\n&nbsp;&nbsp;&nbsp;&nbsp;2. Add a value to the <em>&lt;li&gt;</em>. E.g. change <em>&lt;li&gt;</em> to <em>&lt;li value="4"&gt;</em>\n<br>\n&nbsp;&nbsp;&nbsp;&nbsp;3. If last line is a range (e.g. 8-9) add <em>\'data-range-end\'</em>. E.g. <em>&lt;li data-range-end="9"&gt;</em>\n', null=True)),
                ('translation', ckeditor.fields.RichTextField(blank=True, help_text='Always paste content without formatting (Windows: Ctrl + Shift + V, Mac: Cmd + Shift + V)<br>\nTo start creating lines of text click the \'numbered list\' button\n<br>\nTo manually override an automatic line number simply:\n<br>\n&nbsp;&nbsp;&nbsp;&nbsp;1. Click the \'Source\' button\n<br>\n&nbsp;&nbsp;&nbsp;&nbsp;2. Add a value to the <em>&lt;li&gt;</em>. E.g. change <em>&lt;li&gt;</em> to <em>&lt;li value="4"&gt;</em>\n<br>\n&nbsp;&nbsp;&nbsp;&nbsp;3. If last line is a range (e.g. 8-9) add <em>\'data-range-end\'</em>. E.g. <em>&lt;li data-range-end="9"&gt;</em>\n', null=True)),
                ('transliteration', ckeditor.fields.RichTextField(blank=True, help_text='Always paste content without formatting (Windows: Ctrl + Shift + V, Mac: Cmd + Shift + V)<br>Optional. Only relevant to some Middle Persian texts.', null=True)),
                ('open_state', models.ForeignKey(blank=True, help_text='Optional. Only relevant to some Bactrian texts.', null=True, on_delete=django.db.models.deletion.RESTRICT, to='corpus.sltextfolioopen')),
                ('side', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='corpus.sltextfolioside')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_folios', to='corpus.text')),
            ],
            options={
                'verbose_name': 'Folio',
                'verbose_name_plural': 'Folios (including Transcription, Translation, Images, etc.)',
                'ordering': ['text', 'open_state', 'side', 'id'],
            },
        ),
        migrations.CreateModel(
            name='TextRelatedPublication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pages', models.CharField(blank=True, help_text='Specify the page number or range of page numbers - e.g. 4, 82-84, etc.', max_length=1000, null=True)),
                ('catalogue_number', models.CharField(blank=True, max_length=1000, null=True)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='text_related_publications', to='corpus.sltextpublication')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_related_publications', to='corpus.text')),
            ],
            options={
                'verbose_name': 'Related Publication',
            },
        ),
        migrations.CreateModel(
            name='TextFolioTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField(blank=True, null=True)),
                ('image_part_left', models.FloatField(blank=True, null=True)),
                ('image_part_top', models.FloatField(blank=True, null=True)),
                ('image_part_width', models.FloatField(blank=True, null=True)),
                ('image_part_height', models.FloatField(blank=True, null=True)),
                ('meta_created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('meta_lastupdated_datetime', models.DateTimeField(blank=True, null=True, verbose_name='last updated')),
                ('meta_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='textfoliotag_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('meta_lastupdated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='textfoliotag_lastupdated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_folio_tags', to='corpus.sltextfoliotag')),
                ('text_folio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_folio_tags', to='corpus.textfolio')),
            ],
            options={
                'ordering': ['text_folio', django.db.models.functions.text.Upper('tag__category__name'), django.db.models.functions.text.Upper('tag__name'), 'id'],
            },
        ),
        migrations.CreateModel(
            name='TextDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_text', models.CharField(blank=True, help_text='Format date as free text - e.g. 10 Ramaḍān 605', max_length=1000, null=True)),
                ('date', models.CharField(blank=True, help_text='Format: "YYYY-MM-DD" - e.g. "0608-01-31". Please ensure years before 1000 are 4 digits long using 0s at start, e.g. 0608 not 608, 0056 not 56, etc.', max_length=1000, null=True)),
                ('date_range_start', models.CharField(blank=True, help_text='Format: "YYYY-MM-DD" - e.g. "0608-01-31". Please ensure years before 1000 are 4 digits long using 0s at start, e.g. 0608 not 608, 0056 not 56, etc.', max_length=1000, null=True)),
                ('date_range_end', models.CharField(blank=True, help_text='Format: "YYYY-MM-DD" - e.g. "0608-01-31". Please ensure years before 1000 are 4 digits long using 0s at start, e.g. 0608 not 608, 0056 not 56, etc.', max_length=1000, null=True)),
                ('calendar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='text_dates', to='corpus.slcalendar')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_dates', to='corpus.text')),
            ],
            options={
                'verbose_name': 'Date',
                'verbose_name_plural': 'Original Dates',
            },
        ),
        migrations.AddField(
            model_name='sltexttype',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='corpus.sltexttypecategory'),
        ),
        migrations.AddField(
            model_name='sltextlanguage',
            name='script',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='corpus.sltextscript'),
        ),
        migrations.AddField(
            model_name='sltextfoliotag',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='tags', to='corpus.sltextfoliotagcategory'),
        ),
        migrations.AddField(
            model_name='sltextdocumentsubtype',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='corpus.sltextdocumentsubtypecategory'),
        ),
        migrations.CreateModel(
            name='Seal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=1000, null=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('inscription', models.TextField(blank=True, null=True)),
                ('measurements', models.CharField(blank=True, help_text='e.g. 28 x 23 x 16; 13 x 12', max_length=1000, null=True, verbose_name='measurements (mm)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='corpus/seals__original')),
                ('image_small', models.ImageField(blank=True, null=True, upload_to='corpus/seals__small')),
                ('colours', models.ManyToManyField(blank=True, to='corpus.slsealcolour')),
                ('descriptions', models.ManyToManyField(blank=True, to='corpus.slsealdescription')),
                ('imprints', models.ManyToManyField(blank=True, to='corpus.slsealimprint')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seals', to='corpus.text')),
            ],
            options={
                'verbose_name': 'Seal',
                'verbose_name_plural': 'Seals (only applicable to Bactrian texts)',
                'ordering': ['text', 'type', 'id'],
            },
        ),
        migrations.CreateModel(
            name='PersonInText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name_in_text', models.CharField(blank=True, help_text='If Person is named differently in Text than in this database then record their name in the Text here', max_length=1000, null=True, verbose_name='person name (as it appears in this text)')),
                ('person', models.ForeignKey(help_text='Be sure to search the list before adding a new person. We do not want duplicate records.', on_delete=django.db.models.deletion.CASCADE, related_name='persons_in_texts', to='corpus.person')),
                ('person_role_in_text', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='persons_in_texts', to='corpus.slpersonintextrole')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons_in_texts', to='corpus.text')),
            ],
            options={
                'verbose_name': 'Person in Text',
                'verbose_name_plural': 'Persons in Text',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corpus.slpersongender'),
        ),
        migrations.AddField(
            model_name='person',
            name='persons',
            field=models.ManyToManyField(blank=True, through='corpus.M2MPersonToPerson', to='corpus.person'),
        ),
        migrations.AddField(
            model_name='m2mtexttotext',
            name='relationship_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='corpus.slm2mtexttotextrelationshiptype'),
        ),
        migrations.AddField(
            model_name='m2mtexttotext',
            name='text_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_1', to='corpus.text', verbose_name='text'),
        ),
        migrations.AddField(
            model_name='m2mtexttotext',
            name='text_2',
            field=models.ForeignKey(help_text='Only complete this where multiple separate IE texts originally come from a text.', on_delete=django.db.models.deletion.CASCADE, related_name='text_2', to='corpus.text', verbose_name='text'),
        ),
        migrations.AddField(
            model_name='m2mpersontoperson',
            name='person_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_1', to='corpus.person', verbose_name='person'),
        ),
        migrations.AddField(
            model_name='m2mpersontoperson',
            name='person_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_2', to='corpus.person', verbose_name='person'),
        ),
        migrations.AddField(
            model_name='m2mpersontoperson',
            name='relationship_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='corpus.slm2mpersontopersonrelationshiptype'),
        ),
    ]
