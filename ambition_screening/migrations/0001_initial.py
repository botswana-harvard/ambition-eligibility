# Generated by Django 2.0 on 2017-12-28 18:02

import _socket
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_revision.revision_field
import edc_base.model_fields.hostname_modification_field
import edc_base.model_fields.userfield
import edc_base.model_fields.uuid_auto_field
import edc_base.utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalSubjectScreening',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_base.model_fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_base.model_fields.uuid_auto_field.UUIDAutoField(blank=True, db_index=True, editable=False, help_text='System auto field. UUID primary key.')),
                ('subject_identifier', models.CharField(max_length=50, verbose_name='Subject Identifier')),
                ('subject_identifier_as_pk', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('subject_identifier_aka', models.CharField(editable=False, help_text='track a previously allocated identifier.', max_length=50, null=True, verbose_name='Subject Identifier a.k.a')),
                ('slug', models.CharField(db_index=True, default='', editable=False, help_text='a field used for quick search', max_length=250, null=True)),
                ('reference', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, verbose_name='Reference')),
                ('screening_identifier', models.CharField(blank=True, db_index=True, editable=False, max_length=50, verbose_name='Screening ID')),
                ('report_datetime', models.DateTimeField(default=edc_base.utils.get_utcnow, help_text='Date and time of report.', verbose_name='Report Date and Time')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=10)),
                ('age_in_years', models.IntegerField()),
                ('meningitis_dx', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, verbose_name='First episode cryptococcal meningitis diagnosed by either: CSF India Ink or CSF cryptococcal antigen (CRAG)')),
                ('will_hiv_test', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, verbose_name='Known HIV positive/willing to consent to an HIV test.')),
                ('mental_status', models.CharField(choices=[('NORMAL', 'Normal'), ('ABNORMAL', 'Abnormal')], max_length=10, verbose_name='Mental status')),
                ('consent_ability', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, verbose_name='Participant or legal guardian/representative able and willing to give informed consent.')),
                ('pregnancy', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not Applicable: e.g. male, post-menopausal')], max_length=15, verbose_name='Is the patient pregnant?')),
                ('preg_test_date', models.DateTimeField(blank=True, null=True, verbose_name='Pregnancy test (Urine or serum βhCG) date')),
                ('breast_feeding', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], max_length=15, verbose_name='Is the patient breasfeeding?')),
                ('previous_drug_reaction', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, verbose_name='Previous Adverse Drug Reaction (ADR) to study drug (e.g. rash, drug induced blood abnormality)')),
                ('contraindicated_meds', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='Contraindicated Meds: Cisapride, Pimozide,Terfenadine, Quinidine, Astemizole, Erythromycin', max_length=5, verbose_name='Taking concomitant medication that is contra-indicated with any study drug')),
                ('received_amphotericin', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, verbose_name='Has received >48 hours of Amphotericin B (>=0.7mg/kg/day) prior to screening.')),
                ('received_fluconazole', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, verbose_name='Has received >48 hours of fluconazole treatment (>= 800mg/day) prior to screening.')),
                ('alt', models.IntegerField(blank=True, help_text="Leave blank if unknown. Units: 'IU/mL'. Ineligible if > 200 IU/L", null=True, verbose_name='ALT result')),
                ('neutrophil', models.DecimalField(blank=True, decimal_places=2, help_text="Leave blank if unknown. Units: '10^9/L'. Ineligible if < 0.5  10^9/L", max_digits=4, null=True, verbose_name='Neutrophil result')),
                ('platelets', models.IntegerField(blank=True, help_text="Leave blank if unknown. Units: '10^9/L'. Ineligible if < 50 10^9/L", null=True, verbose_name='Platelets result')),
                ('eligible', models.BooleanField(default=False, editable=False)),
                ('reasons_ineligible', models.TextField(editable=False, max_length=150, null=True, verbose_name='Reason not eligible')),
                ('consented', models.BooleanField(default=False, editable=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_id', edc_base.model_fields.uuid_auto_field.UUIDAutoField(primary_key=True, serialize=False)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sites.Site')),
            ],
            options={
                'verbose_name': 'historical ',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='SubjectScreening',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_base.model_fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_base.model_fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('subject_identifier', models.CharField(max_length=50, verbose_name='Subject Identifier')),
                ('subject_identifier_as_pk', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('subject_identifier_aka', models.CharField(editable=False, help_text='track a previously allocated identifier.', max_length=50, null=True, verbose_name='Subject Identifier a.k.a')),
                ('slug', models.CharField(db_index=True, default='', editable=False, help_text='a field used for quick search', max_length=250, null=True)),
                ('reference', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Reference')),
                ('screening_identifier', models.CharField(blank=True, editable=False, max_length=50, unique=True, verbose_name='Screening ID')),
                ('report_datetime', models.DateTimeField(default=edc_base.utils.get_utcnow, help_text='Date and time of report.', verbose_name='Report Date and Time')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=10)),
                ('age_in_years', models.IntegerField()),
                ('meningitis_dx', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, verbose_name='First episode cryptococcal meningitis diagnosed by either: CSF India Ink or CSF cryptococcal antigen (CRAG)')),
                ('will_hiv_test', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, verbose_name='Known HIV positive/willing to consent to an HIV test.')),
                ('mental_status', models.CharField(choices=[('NORMAL', 'Normal'), ('ABNORMAL', 'Abnormal')], max_length=10, verbose_name='Mental status')),
                ('consent_ability', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, verbose_name='Participant or legal guardian/representative able and willing to give informed consent.')),
                ('pregnancy', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not Applicable: e.g. male, post-menopausal')], max_length=15, verbose_name='Is the patient pregnant?')),
                ('preg_test_date', models.DateTimeField(blank=True, null=True, verbose_name='Pregnancy test (Urine or serum βhCG) date')),
                ('breast_feeding', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'Not applicable')], max_length=15, verbose_name='Is the patient breasfeeding?')),
                ('previous_drug_reaction', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, verbose_name='Previous Adverse Drug Reaction (ADR) to study drug (e.g. rash, drug induced blood abnormality)')),
                ('contraindicated_meds', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], help_text='Contraindicated Meds: Cisapride, Pimozide,Terfenadine, Quinidine, Astemizole, Erythromycin', max_length=5, verbose_name='Taking concomitant medication that is contra-indicated with any study drug')),
                ('received_amphotericin', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, verbose_name='Has received >48 hours of Amphotericin B (>=0.7mg/kg/day) prior to screening.')),
                ('received_fluconazole', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5, verbose_name='Has received >48 hours of fluconazole treatment (>= 800mg/day) prior to screening.')),
                ('alt', models.IntegerField(blank=True, help_text="Leave blank if unknown. Units: 'IU/mL'. Ineligible if > 200 IU/L", null=True, verbose_name='ALT result')),
                ('neutrophil', models.DecimalField(blank=True, decimal_places=2, help_text="Leave blank if unknown. Units: '10^9/L'. Ineligible if < 0.5  10^9/L", max_digits=4, null=True, verbose_name='Neutrophil result')),
                ('platelets', models.IntegerField(blank=True, help_text="Leave blank if unknown. Units: '10^9/L'. Ineligible if < 50 10^9/L", null=True, verbose_name='Platelets result')),
                ('eligible', models.BooleanField(default=False, editable=False)),
                ('reasons_ineligible', models.TextField(editable=False, max_length=150, null=True, verbose_name='Reason not eligible')),
                ('consented', models.BooleanField(default=False, editable=False)),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
