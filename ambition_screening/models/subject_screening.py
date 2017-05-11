from django.db import models
from uuid import uuid4

from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_constants.choices import GENDER, YES_NO, YES_NO_NA, NO, YES
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin

from ..eligibility import Eligibility
from ..identifier import ScreeningIdentifier


class SubjectScreening(NonUniqueSubjectIdentifierFieldMixin, BaseUuidModel):

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

    gender = models.CharField(
        choices=GENDER,
        max_length=10)

    age_in_years = models.IntegerField()

    meningitis_dx = models.CharField(
        choices=YES_NO,
        max_length=5,
        verbose_name='First episode cryptococcal meningitis diagnosed by '
                     'either: CSF India Ink or CSF cryptococcal antigen '
                     '(CRAG)')

    will_hiv_test = models.CharField(
        choices=YES_NO,
        max_length=5,
        verbose_name='Willing to consent to HIV test')

    guardian = models.CharField(
        choices=YES_NO,
        max_length=5,
        blank=True,
        verbose_name='Participant or legal guardian/representative able and '
                     'willing to give informed consent.')

    pregnancy_or_lactation = models.CharField(
        choices=YES_NO_NA,
        max_length=15,
        verbose_name='Pregnancy or lactation (Urine βhCG)')

    previous_drug_reaction = models.CharField(
        choices=YES_NO,
        max_length=5,
        verbose_name='Previous Adverse Drug Reaction (ADR) to study drug '
                     '(e.g. rash, drug induced blood abnormality)')

    contraindicated_meds = models.CharField(
        choices=YES_NO,
        max_length=5,
        verbose_name='Taking concomitant medication that is contra-indicated '
                     'with any study drug')

    received_amphotericin = models.CharField(
        choices=YES_NO,
        max_length=5,
        verbose_name='Has received >48 hours of Amphotericin B (AmB) therapy '
                     'prior to screening.')

    received_fluconazole = models.CharField(
        choices=YES_NO,
        max_length=5,
        verbose_name='Has received >48 hours of fluconazole treatment (> '
                     '400mg daily dose) prior to screening.')

    eligible = models.BooleanField(
        default=False,
        editable=False)

    reasons_ineligible = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.verify_eligibility()
        if not self.id:
            self.screening_identifier = ScreeningIdentifier().identifier
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.screening_identifier} {self.gender} {self.age_in_years}'

    def verify_eligibility(self):
        """Verifies eligibility criteria and sets model attrs.
        """
        def if_yes(value):
            return True if value == YES else False

        def if_no(value):
            return True if value == NO else False
        eligibility = Eligibility(
            age=self.age_in_years,
            gender=self.gender,
            guardian=if_yes(self.guardian),
            meningitis_dx=if_yes(self.meningitis_dx),
            pregnant=if_yes(self.pregnancy_or_lactation),
            no_drug_reaction=if_no(self.previous_drug_reaction),
            no_concomitant_meds=if_no(self.contraindicated_meds),
            no_amphotericin=if_no(self.received_amphotericin),
            no_fluconazole=if_no(self.received_fluconazole))
        self.reasons_ineligible = ','.join(eligibility.reasons)
        self.eligible = eligibility.eligible

    class Meta:
        app_label = 'ambition_screening'
        verbose_name = 'Subject Screening'
