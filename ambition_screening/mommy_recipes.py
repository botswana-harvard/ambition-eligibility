from model_mommy.recipe import Recipe

from edc_constants.constants import YES, NO, MALE, NORMAL, NOT_APPLICABLE

from .models import SubjectScreening

subjectscreening = Recipe(
    SubjectScreening,
    gender=MALE,
    age_in_years=40,
    meningitis_dx=YES,
    will_hiv_test=YES,
    guardian=YES,
    mental_status=NORMAL,
    pregnancy_or_lactation=NOT_APPLICABLE,
    previous_drug_reaction=NO,
    contraindicated_meds=NO,
    received_amphotericin=NO,
    received_fluconazole=NO,
    eligible=True,
    reasons_ineligible=None)
