import random

from django.db import models
from uuid import uuid4

from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_constants.choices import GENDER, YES_NO, YES_NO_NA, NO, YES, FEMALE

from ..models import ConsentModelMixin, ScreeningIdentifierModelMixin


class SubjectScreening(ConsentModelMixin, ScreeningIdentifierModelMixin, BaseUuidModel):

    reference = models.UUIDField(
        verbose_name="Reference",
        unique=True,
        default=uuid4,
        editable=False)

    screening_identifier = models.CharField(
        verbose_name='Screening Id',
        max_length=50,
        blank=True,
        unique=True,
        editable=False)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=get_utcnow,
        help_text='Date and time of report.')

    sex = models.CharField(
        choices=GENDER,
        max_length=10)

    age = models.IntegerField()

    meningitis_diagoses_by_csf_or_crag = models.CharField(
        choices=YES_NO,
        max_length=5,
        verbose_name='First episode cryptococcal meningitis diagnosed by '
                     'either: CSF India Ink or CSF cryptococcal antigen '
                     '(CRAG)')

    consent_to_hiv_test = models.CharField(
        choices=YES_NO,
        max_length=5,
        verbose_name='Willing to consent to HIV test')

    willing_to_give_informed_consent = models.CharField(
        choices=YES_NO,
        max_length=5,
        blank=True,
        unique=True,
        verbose_name='Participant or legal guardian/representative able and '
                     'willing to give informed consent.')

    pregnancy_or_lactation = models.CharField(
        choices=YES_NO_NA,
        max_length=15,
        verbose_name='Pregnancy or lactation (Urine βhCG)')

    previous_adverse_drug_reaction = models.CharField(
        choices=YES_NO,
        max_length=5,
        verbose_name='Previous Adverse Drug Reaction (ADR) to study drug '
                     '(e.g. rash, drug induced blood abnormality)')

    medication_contraindicated_with_study_drug = models.CharField(
        choices=YES_NO,
        max_length=5,
        verbose_name='Taking concomitant medication that is contra-indicated '
                     'with any study drug')

    two_days_amphotericin_b = models.CharField(
        choices=YES_NO,
        max_length=5,
        verbose_name='Has received >48 hours of Amphotericin B (AmB) therapy '
                     'prior to screening.')

    two_days_fluconazole = models.CharField(
        choices=YES_NO,
        max_length=5,
        verbose_name='Has received >48 hours of fluconazole treatment (> '
                     '400mg daily dose) prior to screening.')

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.is_eligible, self.ineligibility = self.get_is_eligible()
        if self.is_eligible and not self.value_is_screening_identifier():
            self.screening_identifier = self.prepare_screening_identifier()
        super().save(*args, **kwargs)

    def __str__(self):
        return (self.screening_identifier + self.sex + str(self.age))

    def get_is_eligible(self):
        error_message = []
        # consent_config = site_consents.get_consent(
        #    consent_model='ambition_subject.subjectconsent')
        if (self.age < 18 and
           self.willing_to_give_informed_consent == NO):
            error_message.append(
                'Participant is under 18')

        if self.sex == FEMALE and self.pregnancy_or_lactation == YES:
            error_message.append('Participant is pregnant')

        if self.previous_adverse_drug_reaction == YES:
            error_message.append('Previous adverse drug reaction reported')

        if self.medication_contraindicated_with_study_drug == YES:
            error_message.append(
                'Participant taking concomitant medication that is contra-'
                'indicated with any study drug')

        if self.two_days_amphotericin_b == YES:
            error_message.append('Has received >48 hours of Amphotericin B')

        if self.two_days_fluconazole == YES:
            error_message.append(
                'Has received >48 hours of fluconazole '
                'treatment (> 400mg daily dose) prior to screening.')
        is_eligible = False if error_message else True
        return (is_eligible, ','.join(error_message))

    def value_is_screening_identifier(self):
        if not self.screening_identifier:
            return False
        if len(self.screening_identifier) == 7:
            return True
        return False

    def prepare_screening_identifier(self):
        """Generate and returns a locally unique study screening
        identifier"""
        template = '{random_string}'
        opts = {
            'random_string': ''.join([random.choice('ABCDEFGHKMNPRTUVWXYZ2346789') for _ in range(7)])}
        screening_identifier = template.format(**opts)
        # look for a duplicate
        if self.__class__.objects.filter(screening_identifier=screening_identifier):
            n = 1
            while self.__class__.objects.filter(screening_identifier=screening_identifier):
                screening_identifier = template.format(**opts)
                n += 1
                if n == len('ABCDEFGHKMNPRTUVWXYZ2346789') ** 7:
                    raise TypeError('Unable prepare a unique requisition identifier, '
                                    'all are taken. Increase the length of the random string')
        return screening_identifier

    class Meta:
        app_label = 'ambition_screening'
        verbose_name = 'Subject Screening'
