# Generated by Django 4.2.1 on 2023-07-04 09:48

from django.conf import settings
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
            name='SlCountry',
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
            name='SlFunder',
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
            name='SlPublicationStatement',
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
            name='SlTextCategory',
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
            name='SlTextCorrespondence',
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
            name='SlTextFolioPartType',
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
            name='SlTextSubjectAdministrativeInternalCorrespondence',
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
            name='SlTextSubjectAdministrativeListsAndAccounting',
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
            name='SlTextSubjectAdministrativeTaxReceipts',
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
            name='SlTextSubjectAgriculturalProduce',
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
            name='SlTextSubjectCurrenciesAndDenominations',
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
            name='SlTextSubjectDocumentation',
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
            name='SlTextSubjectFinanceAndAccountancyPhrases',
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
            name='SlTextSubjectGeographicAdministrativeUnits',
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
            name='SlTextSubjectLandMeasurementUnits',
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
            name='SlTextSubjectLegalAndAdministrativeStockPhrases',
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
            name='SlTextSubjectLegalTransactions',
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
            name='SlTextSubjectMarkings',
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
            name='SlTextSubjectPeopleAndProcessesAdmin',
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
            name='SlTextSubjectPeopleAndProcessesLegal',
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
            name='SlTextSubjectReligion',
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
            name='SlTextSubjectToponym',
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
            name='SlUnitOfMeasurement',
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
                ('shelfmark', models.CharField(max_length=1000)),
                ('id_khan', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Khan ID')),
                ('id_nicholas_simms_williams', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Nicholas Simms-Williams ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('publication_statement_original', models.TextField(blank=True, null=True)),
                ('publication_statement_republished', models.TextField(blank=True, null=True)),
                ('writing_support_details', models.TextField(blank=True, null=True)),
                ('dimensions_height', models.FloatField(blank=True, null=True)),
                ('dimensions_width', models.FloatField(blank=True, null=True)),
                ('fold_lines_count_details', models.TextField(blank=True, help_text='Include fold lines count details, e.g. for recto, verso, etc.', null=True)),
                ('fold_lines_count_total', models.IntegerField(blank=True, help_text='Specify the total number of fold lines for this Text (you may need to add together the fold lines counts of recto, verso, etc. where applicable)', null=True)),
                ('physical_additional_details', models.TextField(blank=True, null=True)),
                ('public_review_notes', models.TextField(blank=True, help_text='Used to make comments or notes during the review process.', null=True)),
                ('public_approval_1_of_2_datetime', models.DateTimeField(blank=True, null=True)),
                ('public_approval_2_of_2_datetime', models.DateTimeField(blank=True, null=True)),
                ('admin_commentary', models.TextField(blank=True, null=True)),
                ('admin_notes', models.TextField(blank=True, null=True)),
                ('meta_created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('meta_lastupdated_datetime', models.DateTimeField(blank=True, null=True, verbose_name='last updated')),
                ('admin_classification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='texts', to='corpus.sltextclassification')),
                ('admin_contributors', models.ManyToManyField(blank=True, help_text='Admins who have contributed to this text but are not responsible for it', related_name='text_admin_contributors', to=settings.AUTH_USER_MODEL)),
                ('admin_owners', models.ManyToManyField(blank=True, help_text='Admins who are responsible for this text', related_name='text_admin_owners', to=settings.AUTH_USER_MODEL)),
                ('administrative_internal_correspondences', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectadministrativeinternalcorrespondence')),
                ('administrative_lists_and_accounting', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectadministrativelistsandaccounting')),
                ('administrative_tax_receipts', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectadministrativetaxreceipts')),
                ('agricultural_produce', models.ManyToManyField(blank=True, db_index=True, help_text='Agricultural produce, animals, and farming equipment', related_name='texts', to='corpus.sltextsubjectagriculturalproduce')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='texts', to='corpus.sltextcategory')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='texts', to='corpus.sltextcollection')),
                ('correspondence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='texts', to='corpus.sltextcorrespondence')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='texts', to='corpus.slcountry')),
                ('currencies_and_denominations', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectcurrenciesanddenominations')),
                ('dimensions_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='texts', to='corpus.slunitofmeasurement')),
                ('documentations', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectdocumentation')),
                ('finance_and_accountancy_phrases', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectfinanceandaccountancyphrases')),
                ('funders', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.slfunder')),
                ('geographic_administrative_units', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectgeographicadministrativeunits')),
                ('land_measurement_units', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectlandmeasurementunits')),
                ('languages', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextlanguage')),
                ('legal_and_administrative_stock_phrases', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectlegalandadministrativestockphrases')),
                ('legal_transactions', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectlegaltransactions')),
                ('markings', models.ManyToManyField(blank=True, db_index=True, help_text='Scribal markings, ciphers, abbreviations, para-text, column format', related_name='texts', to='corpus.sltextsubjectmarkings')),
                ('meta_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('meta_lastupdated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_lastupdated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
                ('people_and_processes_admins', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectpeopleandprocessesadmin', verbose_name='People and processes involved in public administration, tax, trade, and commerce')),
                ('people_and_processes_legal', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectpeopleandprocesseslegal', verbose_name='People and processes involved in legal and judiciary system')),
                ('public_approval_1_of_2', models.ForeignKey(blank=True, help_text='Texts must be approved by 2 admins to be visible on the public website. This is the 1st approval.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_public_approval_1_of_2', to=settings.AUTH_USER_MODEL)),
                ('public_approval_2_of_2', models.ForeignKey(blank=True, help_text='Texts must be approved by 2 admins to be visible on the public website. This is the 2nd approval.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='text_public_approval_2_of_2', to=settings.AUTH_USER_MODEL)),
                ('public_review_requests', models.ManyToManyField(blank=True, help_text='Select admins to request that they review this Text and approve it to be shown on the public website. Reviewers will be notified via email.', related_name='text_public_review_request', to=settings.AUTH_USER_MODEL)),
                ('publication_statement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='texts', to='corpus.slpublicationstatement')),
                ('religions', models.ManyToManyField(blank=True, db_index=True, related_name='texts', to='corpus.sltextsubjectreligion')),
                ('texts', models.ManyToManyField(blank=True, through='corpus.M2MTextToText', to='corpus.text')),
                ('toponyms', models.ManyToManyField(blank=True, db_index=True, help_text='Place names', related_name='texts', to='corpus.sltextsubjecttoponym')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='texts', to='corpus.sltexttype')),
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
                ('image', models.ImageField(blank=True, null=True, upload_to='corpus/text_folios')),
                ('open_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='corpus.sltextfolioopen')),
                ('side', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='corpus.sltextfolioside')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_folios', to='corpus.text')),
            ],
            options={
                'ordering': ['text', 'open_state', 'side', 'id'],
            },
        ),
        migrations.CreateModel(
            name='TextFolioPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('position_in_image', models.TextField(blank=True, null=True)),
                ('text_folio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_folio_parts', to='corpus.textfolio')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_folio_parts', to='corpus.sltextfolioparttype')),
            ],
        ),
        migrations.CreateModel(
            name='TextFolioLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcription_line_number', models.IntegerField()),
                ('transcription_line_number_end', models.IntegerField(blank=True, help_text='If this line spans multiple lines, specify the last line number here. E.g. if line range is 19-21, put 21 here', null=True)),
                ('transcription_text', models.TextField(blank=True, max_length=1000, null=True)),
                ('translation_line_number', models.IntegerField(blank=True, null=True)),
                ('translation_line_number_end', models.IntegerField(blank=True, help_text='If this line spans multiple lines, specify the last line number here. E.g. if line range is 19-21, put 21 here', null=True)),
                ('translation_text', models.TextField(blank=True, max_length=1000, null=True)),
                ('position_in_image', models.TextField(blank=True, null=True)),
                ('text_folio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_folio_lines', to='corpus.textfolio')),
            ],
        ),
        migrations.CreateModel(
            name='TextDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(blank=True, help_text='E.g. 0605-09-10, 1198-02-11, etc.', max_length=1000, null=True)),
                ('date_not_before', models.CharField(blank=True, help_text='E.g. 0605-09-10, 1198-02-11, etc.', max_length=1000, null=True)),
                ('date_not_after', models.CharField(blank=True, help_text='E.g. 0605-09-10, 1198-02-11, etc.', max_length=1000, null=True)),
                ('date_text', models.CharField(blank=True, help_text='E.g. 10 Ramaḍān 605, 11 Feb 1198, etc.', max_length=1000, null=True)),
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