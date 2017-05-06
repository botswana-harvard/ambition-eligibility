from dateutil.relativedelta import relativedelta
from faker import Faker
from faker.providers import BaseProvider
from model_mommy.recipe import Recipe

from edc_base.utils import get_utcnow
from edc_base_test.faker import EdcBaseProvider
from edc_constants.constants import YES, NO

from .models import SubjectScreening


class DateProvider(BaseProvider):

    def next_month(self):
        return (get_utcnow() + relativedelta(months=1)).date()

    def last_year(self):
        return (get_utcnow() - relativedelta(years=1)).date()

    def three_months_ago(self):
        return (get_utcnow() - relativedelta(months=3)).date()

    def thirty_four_weeks_ago(self):
        return (get_utcnow() - relativedelta(weeks=34)).date()

    def four_weeks_ago(self):
        return (get_utcnow() - relativedelta(weeks=4)).date()

    def yesterday(self):
        return (get_utcnow() - relativedelta(days=1)).date()


fake = Faker()
fake.add_provider(EdcBaseProvider)
fake.add_provider(DateProvider)

subject_screening = Recipe(
    SubjectScreening,
    sex='Male',
    age=40,
    meningitis_diagoses_by_csf_or_crag=YES,
    consent_to_hiv_test=YES,
    willing_to_give_informed_consent=YES,
    pregnancy_or_lactation=NO,
    previous_adverse_drug_reaction=NO,
    medication_contraindicated_with_study_drug=NO,
    two_days_amphotericin_b=NO,
    two_days_fluconazole=NO,
    is_eligible=True,
    ineligibility=None)
