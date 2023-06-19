# Generated by Django 4.2.1 on 2023-06-19 16:01

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
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('subject', models.TextField(blank=True, null=True)),
                ('publication_statement_original', models.TextField(blank=True, null=True)),
                ('publication_statement_republished', models.TextField(blank=True, null=True)),
                ('shelfmark', models.CharField(blank=True, max_length=1000, null=True)),
                ('writing_support_details', models.TextField(blank=True, null=True)),
                ('dimensions_height', models.FloatField(blank=True, null=True)),
                ('dimensions_width', models.FloatField(blank=True, null=True)),
                ('fold_lines_count_details', models.TextField(blank=True, help_text='Include fold lines count details, e.g. for recto, verso, etc.', null=True)),
                ('fold_lines_count_total', models.IntegerField(blank=True, help_text='Specify the total number of fold lines for this Document (you may need to add together the fold lines counts of recto, verso, etc. where applicable)', null=True)),
                ('physical_additional_details', models.TextField(blank=True, null=True)),
                ('public_review_notes', models.TextField(blank=True, help_text='Used to make comments or notes during the review process.', null=True)),
                ('public_approval_1_of_2_datetime', models.DateTimeField(blank=True, null=True)),
                ('public_approval_2_of_2_datetime', models.DateTimeField(blank=True, null=True)),
                ('admin_commentary', models.TextField(blank=True, null=True)),
                ('admin_notes', models.TextField(blank=True, null=True)),
                ('meta_created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('meta_lastupdated_datetime', models.DateTimeField(blank=True, null=True, verbose_name='last updated')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='researchdata/document_pages')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_pages', to='researchdata.document')),
            ],
            options={
                'ordering': ['page_number', 'id'],
            },
        ),
        migrations.CreateModel(
            name='M2MPersonToPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            name='SlDocumentClassification',
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
            name='SlDocumentCollection',
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
            name='SlDocumentCorrespondence',
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
            name='SlDocumentPageOpen',
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
            name='SlDocumentPagePartType',
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
            name='SlDocumentPageSide',
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
            name='SlDocumentScript',
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
            name='SlDocumentType',
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
            name='SlDocumentTypeAdministrativeInternalCorrespondence',
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
            name='SlDocumentTypeAdministrativeListsAndAccounting',
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
            name='SlDocumentTypeAdministrativeTaxReceipts',
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
            name='SlDocumentTypeAgriculturalProduce',
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
            name='SlDocumentTypeCurrenciesAndDenominations',
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
            name='SlDocumentTypeDocumentation',
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
            name='SlDocumentTypeFinanceAndAccountancyPhrases',
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
            name='SlDocumentTypeGeographicAdministrativeUnits',
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
            name='SlDocumentTypeLandMeasurementUnits',
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
            name='SlDocumentTypeLegalAndAdministrativeStockPhrases',
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
            name='SlDocumentTypeLegalTransactions',
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
            name='SlDocumentTypeMarkings',
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
            name='SlDocumentTypePeopleAndProcessesAdmin',
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
            name='SlDocumentTypePeopleAndProcessesLegal',
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
            name='SlDocumentTypeReligion',
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
            name='SlDocumentTypeToponym',
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
            name='SlDocumentWritingSupport',
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
            name='SlPersonInDocumentType',
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
            name='SlDocumentLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=1000)),
                ('script', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='researchdata.sldocumentscript')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Upper('name'), 'id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonInDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name_in_document', models.CharField(blank=True, help_text='If Person is named differently in Document than in this database then record their name in the Document here', max_length=1000, null=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons_in_documents', to='researchdata.document')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons_in_documents', to='researchdata.person')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='persons_in_documents', to='researchdata.slpersonindocumenttype')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='researchdata.slpersongender'),
        ),
        migrations.AddField(
            model_name='person',
            name='person',
            field=models.ManyToManyField(blank=True, through='researchdata.M2MPersonToPerson', to='researchdata.person'),
        ),
        migrations.AddField(
            model_name='m2mpersontoperson',
            name='person_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_1', to='researchdata.person'),
        ),
        migrations.AddField(
            model_name='m2mpersontoperson',
            name='person_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_2', to='researchdata.person'),
        ),
        migrations.AddField(
            model_name='m2mpersontoperson',
            name='relationship_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='researchdata.slm2mpersontopersonrelationshiptype'),
        ),
        migrations.CreateModel(
            name='DocumentPagePart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('position_in_image', models.TextField(blank=True, null=True)),
                ('document_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_page_parts', to='researchdata.documentpage')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_page_parts', to='researchdata.sldocumentpageparttype')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentPageLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcription_line_number', models.IntegerField()),
                ('transcription_line_number_end', models.IntegerField(blank=True, help_text='If this line spans multiple lines, specify the last line number here. E.g. if line range is 19-21, put 21 here', null=True)),
                ('transcription_text', models.TextField(blank=True, max_length=1000, null=True)),
                ('translation_line_number', models.IntegerField(blank=True, null=True)),
                ('translation_line_number_end', models.IntegerField(blank=True, help_text='If this line spans multiple lines, specify the last line number here. E.g. if line range is 19-21, put 21 here', null=True)),
                ('translation_text', models.TextField(blank=True, max_length=1000, null=True)),
                ('position_in_image', models.TextField(blank=True, null=True)),
                ('document_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_page_lines', to='researchdata.documentpage')),
            ],
        ),
        migrations.AddField(
            model_name='documentpage',
            name='open_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='researchdata.sldocumentpageopen'),
        ),
        migrations.AddField(
            model_name='documentpage',
            name='side',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='researchdata.sldocumentpageside'),
        ),
        migrations.CreateModel(
            name='DocumentDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(blank=True, help_text='E.g. 0605-09-10, 1198-02-11, etc.', max_length=1000, null=True)),
                ('date_not_before', models.CharField(blank=True, help_text='E.g. 0605-09-10, 1198-02-11, etc.', max_length=1000, null=True)),
                ('date_not_after', models.CharField(blank=True, help_text='E.g. 0605-09-10, 1198-02-11, etc.', max_length=1000, null=True)),
                ('date_text', models.CharField(blank=True, help_text='E.g. 10 Ramaḍān 605, 11 Feb 1198, etc.', max_length=1000, null=True)),
                ('calendar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='document_dates', to='researchdata.slcalendar')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_dates', to='researchdata.document')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='admin_classification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='researchdata.sldocumentclassification'),
        ),
        migrations.AddField(
            model_name='document',
            name='admin_contributors',
            field=models.ManyToManyField(blank=True, help_text='Admins who have contributed to this document but are not responsible for it', related_name='document_admin_contributors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='admin_owners',
            field=models.ManyToManyField(blank=True, help_text='Admins who are responsible for this document', related_name='document_admin_owners', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='administrative_internal_correspondences',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.sldocumenttypeadministrativeinternalcorrespondence'),
        ),
        migrations.AddField(
            model_name='document',
            name='administrative_lists_and_accounting',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.sldocumenttypeadministrativelistsandaccounting'),
        ),
        migrations.AddField(
            model_name='document',
            name='administrative_tax_receipts',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.sldocumenttypeadministrativetaxreceipts'),
        ),
        migrations.AddField(
            model_name='document',
            name='agricultural_produce',
            field=models.ManyToManyField(blank=True, db_index=True, help_text='Agricultural produce, animals, and farming equipment', related_name='documents', to='researchdata.sldocumenttypeagriculturalproduce'),
        ),
        migrations.AddField(
            model_name='document',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='researchdata.sldocumentcollection'),
        ),
        migrations.AddField(
            model_name='document',
            name='correspondence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='researchdata.sldocumentcorrespondence'),
        ),
        migrations.AddField(
            model_name='document',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='researchdata.slcountry'),
        ),
        migrations.AddField(
            model_name='document',
            name='currencies_and_denominations',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.sldocumenttypecurrenciesanddenominations'),
        ),
        migrations.AddField(
            model_name='document',
            name='dimensions_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='researchdata.slunitofmeasurement'),
        ),
        migrations.AddField(
            model_name='document',
            name='documentations',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.sldocumenttypedocumentation'),
        ),
        migrations.AddField(
            model_name='document',
            name='finance_and_accountancy_phrases',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.sldocumenttypefinanceandaccountancyphrases'),
        ),
        migrations.AddField(
            model_name='document',
            name='funders',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.slfunder'),
        ),
        migrations.AddField(
            model_name='document',
            name='geographic_administrative_units',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.sldocumenttypegeographicadministrativeunits'),
        ),
        migrations.AddField(
            model_name='document',
            name='land_measurement_units',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.sldocumenttypelandmeasurementunits'),
        ),
        migrations.AddField(
            model_name='document',
            name='languages',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.sldocumentlanguage'),
        ),
        migrations.AddField(
            model_name='document',
            name='legal_and_administrative_stock_phrases',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.sldocumenttypelegalandadministrativestockphrases'),
        ),
        migrations.AddField(
            model_name='document',
            name='legal_transactions',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.sldocumenttypelegaltransactions'),
        ),
        migrations.AddField(
            model_name='document',
            name='markings',
            field=models.ManyToManyField(blank=True, db_index=True, help_text='Scribal markings, ciphers, abbreviations, para-text, column format', related_name='documents', to='researchdata.sldocumenttypemarkings'),
        ),
        migrations.AddField(
            model_name='document',
            name='meta_created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='document_created_by', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AddField(
            model_name='document',
            name='meta_lastupdated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='document_lastupdated_by', to=settings.AUTH_USER_MODEL, verbose_name='last updated by'),
        ),
        migrations.AddField(
            model_name='document',
            name='people_and_processes_admins',
            field=models.ManyToManyField(blank=True, db_index=True, help_text='People and processes involved in public administration, tax, trade, and commerce', related_name='documents', to='researchdata.sldocumenttypepeopleandprocessesadmin'),
        ),
        migrations.AddField(
            model_name='document',
            name='people_and_processes_legal',
            field=models.ManyToManyField(blank=True, db_index=True, help_text='People and processes involved in legal and judiciary system', related_name='documents', to='researchdata.sldocumenttypepeopleandprocesseslegal'),
        ),
        migrations.AddField(
            model_name='document',
            name='public_approval_1_of_2',
            field=models.ForeignKey(blank=True, help_text='Documents must be approved by 2 admins to be visible on the public website. This is the 1st approval.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='document_public_approval_1_of_2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='public_approval_2_of_2',
            field=models.ForeignKey(blank=True, help_text='Documents must be approved by 2 admins to be visible on the public website. This is the 2nd approval.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='document_public_approval_2_of_2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='public_review_requests',
            field=models.ManyToManyField(blank=True, help_text='Select admins to request that they review this Document and approve it to be shown on the public website. Reviewers will be notified via email.', related_name='document_public_review_request', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document',
            name='publication_statement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='researchdata.slpublicationstatement'),
        ),
        migrations.AddField(
            model_name='document',
            name='religions',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='documents', to='researchdata.sldocumenttypereligion'),
        ),
        migrations.AddField(
            model_name='document',
            name='toponyms',
            field=models.ManyToManyField(blank=True, db_index=True, help_text='Place names', related_name='documents', to='researchdata.sldocumenttypetoponym'),
        ),
        migrations.AddField(
            model_name='document',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='researchdata.sldocumenttype'),
        ),
        migrations.AddField(
            model_name='document',
            name='writing_support',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='researchdata.sldocumentwritingsupport'),
        ),
    ]
