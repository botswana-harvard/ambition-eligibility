from django.apps import apps as django_apps

from edc_constants.choices import NORMAL_ABNORMAL
from edc_constants.constants import ABNORMAL, MALE, FEMALE, NORMAL, YES, NO


class MentalStatusEvaluatorError(Exception):
    pass


class MentalStatusEvaluator:

    def __init__(self, mental_status=None, guardian=None):
        self.mental_status = mental_status
        if self.mental_status not in [tpl[0] for tpl in NORMAL_ABNORMAL]:
            raise MentalStatusEvaluatorError(
                f'Invalid mental status. Got {self.mental_status}')
        self.guardian = guardian

    @property
    def eligible(self):
        return self.mental_status == NORMAL or (
            self.mental_status == ABNORMAL and self.guardian == YES)

    @property
    def reason(self):
        reason = None
        if not self.eligible and self.guardian == NO:
            reason = f'Unable to consent.'
        return reason


class AgeEvaluator:

    def __init__(self, age=None, adult_lower=None,
                 adult_upper=None):
        app_config = django_apps.get_app_config('ambition_screening')
        adult_lower = adult_lower or app_config.screening_age_adult_lower
        adult_upper = adult_upper or app_config.screening_age_adult_upper

        self.eligible = False
        try:
            if adult_lower <= age <= adult_upper:
                self.eligible = True
        except TypeError:
            pass
        self.reason = None
        if not self.eligible:
            if age < adult_lower:
                self.reason = f'age<{adult_lower}'
            elif age > adult_upper:
                self.reason = f'age>{adult_upper}'


class GenderEvaluator:
    """Eligible if gender is valid and female not pregnant.
    """

    def __init__(self, gender=None, pregnant=None, breast_feeding=None):
        self.eligible = False
        self.reason = None
        if gender == MALE:
            self.eligible = True
        elif gender == FEMALE and not pregnant and not breast_feeding:
            self.eligible = True
        if not self.eligible:
            if pregnant:
                self.reason = 'pregnant'
            if breast_feeding:
                self.reason = 'breastfeeding'
            if gender not in [MALE, FEMALE]:
                self.reason = 'invalid gender'


class Eligibility:

    """Eligible if all criteria evaluate True.
    """

    def __init__(self, age=None, guardian=None, gender=None, pregnant=None,
                 meningitis_dx=None, no_drug_reaction=None,
                 no_concomitant_meds=None, no_amphotericin=None,
                 no_fluconazole=None, mental_status=None, breast_feeding=None):
        age_evaluator = AgeEvaluator(age=age)
        gender_evaluator = GenderEvaluator(
            gender=gender, pregnant=pregnant, breast_feeding=breast_feeding)
        mental_status_evaluator = MentalStatusEvaluator(
            mental_status=mental_status,
            guardian=guardian)
        criteria = dict(
            no_drug_reaction=no_drug_reaction,
            no_concomitant_meds=no_concomitant_meds,
            no_amphotericin=no_amphotericin,
            no_fluconazole=no_fluconazole,
            meningitis_dx=meningitis_dx,
            age=age_evaluator.eligible,
            gender=gender_evaluator.eligible,
            mental_status=mental_status_evaluator.eligible)
        self.eligible = all(criteria.values())
        self.reasons = [k for k, v in criteria.items() if not v]
        if age_evaluator.reason:
            self.reasons.pop(self.reasons.index('age'))
            self.reasons.append(age_evaluator.reason)
        if gender_evaluator.reason:
            self.reasons.pop(self.reasons.index('gender'))
            self.reasons.append(gender_evaluator.reason)
