from model_mommy.recipe import Recipe

from edc_constants.constants import YES, NO, MALE

from .models import SubjectScreening

subjectscreening = Recipe(
    SubjectScreening,
    gender=MALE,
    age_in_years=40,
    meningitis_dx=YES,
    will_hiv_test=YES,
    guardian=YES,
    pregnancy_or_lactation=NO,
    previous_drug_reaction=NO,
    contraindicated_meds=NO,
    received_amphotericin=NO,
    received_fluconazole=NO,
    eligible=True,
    reasons_ineligible=None)
