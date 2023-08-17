# Generated by Django 4.2.3 on 2023-08-17 16:49

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
                ('profession', models.CharField(blank=True, max_length=1000, null=True)),
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
            name='SlTextCentury',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
                ('century_number', models.IntegerField(validators=[django.core.validators.MaxValueValidator(21), django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'ordering': ['century_number'],
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
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
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
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTextFolioAnnotationType',
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
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SlTextTagAgriculturalProduce',
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
            name='SlTextTagCurrenciesAndDenominations',
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
            name='SlTextTagDocumentation',
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
            name='SlTextTagFinanceAndAccountancyPhrases',
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
            name='SlTextTagGeographicAdministrativeUnits',
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
            name='SlTextTagLandMeasurementUnits',
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
            name='SlTextTagLegalAndAdministrativeStockPhrases',
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
            name='SlTextTagMarkings',
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
            name='SlTextTagPeopleAndProcessesAdmin',
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
            name='SlTextTagPeopleAndProcessesLegal',
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
            name='SlTextTagReligion',
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
            name='SlTextTagToponym',
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
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
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
                ('summary_of_content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('writing_support_details', models.TextField(blank=True, null=True)),
                ('dimensions_height', models.FloatField(blank=True, null=True, verbose_name='height (cm)')),
                ('dimensions_width', models.FloatField(blank=True, null=True, verbose_name='width (cm)')),
                ('fold_lines_details', models.TextField(blank=True, null=True)),
                ('physical_additional_details', models.TextField(blank=True, null=True)),
                ('public_review_ready', models.BooleanField(default=False, help_text='Tick this box to mark this Corpus Text as ready to be reviewed by the Principal Editor.<br>If the editor approves it, this Corpus Text will then be visible on the public website.<br>The editor will be notified via email when you tick this box.<br>You can only tick this box if a Principal Editor has been set for this Corpus Text (see the above Admin section).', verbose_name='ready to review')),
                ('public_review_notes', models.TextField(blank=True, help_text='Optional. Include any necessary comments, feedback, or notes during the review process.', null=True, verbose_name='review notes')),
                ('public_review_approved', models.BooleanField(default=False, help_text='Tick to approve this Corpus Text. This will make it visible on the public website. You can only tick this box if you are the Principal Editor and this Corpus Text has been marked as ready to review', verbose_name='approved')),
                ('public_review_approved_datetime', models.DateTimeField(blank=True, null=True, verbose_name='approved date/time')),
                ('admin_commentary', models.TextField(blank=True, null=True, verbose_name='Commentary')),
                ('meta_created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('meta_lastupdated_datetime', models.DateTimeField(blank=True, null=True, verbose_name='last updated')),
                ('additional_languages', models.ManyToManyField(blank=True, db_index=True, help_text="Don't include the primary language. Only include additional languages/scripts that also appear in the text.", related_name='texts', to='corpus.sltextlanguage')),
                ('admin_classification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='texts', to='corpus.sltextclassification', verbose_name='Classification')),
                ('admin_contributors', models.ManyToManyField(blank=True, help_text='Users who have contributed to this Corpus Text (e.g. co-editors, data entry persons, etc.) but are not the principal editor or principal data entry person (these are specified above).<br>', related_name='text_admin_contributors', to=settings.AUTH_USER_MODEL, verbose_name='contributors')),
                ('admin_principal_data_entry_person', models.ForeignKey(blank=True, help_text='The main person who has entered the data for this Corpus Text into the database', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_admin_principal_data_entry_person', to=settings.AUTH_USER_MODEL, verbose_name='principal data entry person')),
                ('admin_principal_editor', models.ForeignKey(blank=True, help_text='The main person responsible for this Corpus Text', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_admin_principal_editor', to=settings.AUTH_USER_MODEL, verbose_name='principal editor')),
                ('agricultural_produce', models.ManyToManyField(blank=True, db_index=True, help_text='Agricultural produce, animals, and farming equipment', related_name='texts', to='corpus.sltexttagagriculturalproduce')),
                ('century', models.ForeignKey(blank=True, help_text='Uses the Gregorian calendar. This is used to filter and sort results in the public interface. If only a date range is available then select the century in the middle of the range. More specific data about dates can be found below in the "Text Dates" section of this form.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='corpus.sltextcentury')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='texts', to='corpus.sltextcollection')),
                ('corpus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='texts', to='corpus.sltextcorpus')),
                ('currencies_and_denominations', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltexttagcurrenciesanddenominations')),
                ('document_subtype', models.ForeignKey(blank=True, help_text='If a type of Administrative or Legal is selected for this Corpus Text, please also provide the subtype', null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='texts', to='corpus.sltextdocumentsubtype')),
                ('documentations', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltexttagdocumentation')),
                ('finance_and_accountancy_phrases', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltexttagfinanceandaccountancyphrases')),
                ('geographic_administrative_units', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltexttaggeographicadministrativeunits')),
                ('land_measurement_units', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltexttaglandmeasurementunits')),
                ('legal_and_administrative_stock_phrases', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltexttaglegalandadministrativestockphrases')),
                ('markings', models.ManyToManyField(blank=True, db_index=True, help_text='Scribal markings, ciphers, abbreviations, para-text, column format', related_name='texts', to='corpus.sltexttagmarkings')),
                ('meta_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('meta_lastupdated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_lastupdated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
                ('people_and_processes_admins', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltexttagpeopleandprocessesadmin', verbose_name='People and processes involved in public administration, tax, trade, and commerce')),
                ('people_and_processes_legal', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltexttagpeopleandprocesseslegal', verbose_name='People and processes involved in legal and judiciary system')),
                ('primary_language', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='texts_primary', to='corpus.sltextlanguage')),
                ('public_review_approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_public_review_approved_by', to=settings.AUTH_USER_MODEL, verbose_name='approved by')),
                ('religions', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltexttagreligion')),
                ('texts', models.ManyToManyField(blank=True, through='corpus.M2MTextToText', to='corpus.text')),
                ('toponyms', models.ManyToManyField(blank=True, db_index=True, help_text='Place names', related_name='texts', to='corpus.sltexttagtoponym')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='texts', to='corpus.sltexttype')),
                ('writing_support', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='texts', to='corpus.sltextwritingsupport')),
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
                ('transcription', ckeditor.fields.RichTextField(blank=True, help_text='\nTo start creating lines of text click the \'numbered list\' button\n<br>\nTo manually override an automatic line number simply:\n<br>\n&nbsp;&nbsp;&nbsp;&nbsp;1. Click the \'Source\' button\n<br>\n&nbsp;&nbsp;&nbsp;&nbsp;2. Add a value to the <em>&lt;li&gt;</em>. E.g. change <em>&lt;li&gt;</em> to <em>&lt;li value="4"&gt;</em>\n<br>\n&nbsp;&nbsp;&nbsp;&nbsp;3. If last line is a range (e.g. 8-9) add <em>\'data-range-end\'</em>. E.g. <em>&lt;li data-range-end="9"&gt;</em>\n', null=True)),
                ('translation', ckeditor.fields.RichTextField(blank=True, help_text='\nTo start creating lines of text click the \'numbered list\' button\n<br>\nTo manually override an automatic line number simply:\n<br>\n&nbsp;&nbsp;&nbsp;&nbsp;1. Click the \'Source\' button\n<br>\n&nbsp;&nbsp;&nbsp;&nbsp;2. Add a value to the <em>&lt;li&gt;</em>. E.g. change <em>&lt;li&gt;</em> to <em>&lt;li value="4"&gt;</em>\n<br>\n&nbsp;&nbsp;&nbsp;&nbsp;3. If last line is a range (e.g. 8-9) add <em>\'data-range-end\'</em>. E.g. <em>&lt;li data-range-end="9"&gt;</em>\n', null=True)),
                ('transliteration', ckeditor.fields.RichTextField(blank=True, help_text='Optional. Only relevant to some Middle Persian texts.', null=True)),
                ('open_state', models.ForeignKey(blank=True, help_text='Optional. Only relevant to some Bactrian texts.', null=True, on_delete=django.db.models.deletion.RESTRICT, to='corpus.sltextfolioopen')),
                ('side', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='corpus.sltextfolioside')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_folios', to='corpus.text')),
            ],
            options={
                'verbose_name': 'Text Folio (including Transcription, Translation, Images, etc.)',
                'verbose_name_plural': 'Text Folio (including Transcription, Translation, Images, etc.)',
                'ordering': ['text', 'open_state', 'side', 'id'],
            },
        ),
        migrations.CreateModel(
            name='TextRelatedPublication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pages', models.CharField(blank=True, help_text='Specify the page number or range of page numbers - e.g. 4, 82-84, etc.', max_length=1000, null=True)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='text_related_publications', to='corpus.sltextpublication')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_related_publications', to='corpus.text')),
            ],
        ),
        migrations.CreateModel(
            name='TextFolioAnnotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('position_in_image', models.TextField(blank=True, null=True)),
                ('text_folio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_folio_parts', to='corpus.textfolio')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_folio_parts', to='corpus.sltextfolioannotationtype')),
            ],
        ),
        migrations.CreateModel(
            name='TextDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_text', models.CharField(blank=True, help_text='Format date as free text - e.g. 10 Ramaḍān 605, 11 Feb 1198', max_length=1000, null=True)),
                ('date', models.CharField(blank=True, help_text='Format date as: YYYY-MM-DD - e.g. 0605-01-31', max_length=1000, null=True)),
                ('date_range_start', models.CharField(blank=True, help_text='Format date as: YYYY-MM-DD - e.g. 0605-01-31', max_length=1000, null=True)),
                ('date_range_end', models.CharField(blank=True, help_text='Format date as: YYYY-MM-DD - e.g. 0605-01-31', max_length=1000, null=True)),
                ('calendar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='text_dates', to='corpus.slcalendar')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_dates', to='corpus.text')),
            ],
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
            model_name='sltextdocumentsubtype',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='corpus.sltextdocumentsubtypecategory'),
        ),
        migrations.CreateModel(
            name='PersonInText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name_in_text', models.CharField(blank=True, help_text='If Person is named differently in Text than in this database then record their name in the Text here', max_length=1000, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons_in_texts', to='corpus.person')),
                ('person_role_in_text', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='persons_in_texts', to='corpus.slpersonintextrole')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons_in_texts', to='corpus.text')),
            ],
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus.slm2mtexttotextrelationshiptype'),
        ),
        migrations.AddField(
            model_name='m2mtexttotext',
            name='text_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_1', to='corpus.text', verbose_name='text'),
        ),
        migrations.AddField(
            model_name='m2mtexttotext',
            name='text_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_2', to='corpus.text', verbose_name='text'),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus.slm2mpersontopersonrelationshiptype'),
        ),
    ]
