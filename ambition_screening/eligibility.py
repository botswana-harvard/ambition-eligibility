from django.apps import apps as django_apps

from edc_constants.constants import MALE, FEMALE, NORMAL, ABNORMAL

from edc_constants.choices import NORMAL_ABNORMAL
from pprint import pprint


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
        eligible = False
        if self.mental_status == NORMAL:
            eligible = True
        elif self.mental_status == ABNORMAL and self.guardian:
            eligible = True
        return eligible

    @property
    def reason(self):
        reason = None
        if not self.eligible:
            reason = f'Mental status {self.mental_status}, no guardian.'
        return reason


class AgeEvaluator:

    def __init__(self, age=None, adult_lower=None,
                 adult_upper=None):
        app_config = django_apps.get_app_config('ambition_screening')
        self.age = age
        self.adult_lower = adult_lower or app_config.screening_age_adult_lower
        self.adult_upper = adult_upper or app_config.screening_age_adult_upper

    @property
    def eligible(self):
        """Returns True if within age range.
        """
        eligible = False
        try:
            if self.adult_lower <= self.age <= self.adult_upper:
                eligible = True
        except TypeError:
            pass
        return eligible

    @property
    def reason(self):
        reason = None
        if not self.eligible:
            if self.age < self.adult_lower:
                reason = f'age<{self.adult_lower}'
            elif self.age > self.adult_upper:
                reason = f'age>{self.adult_upper}'
        return reason


class GenderEvaluator:

    def __init__(self, gender=None, pregnant=None, breast_feeding=None):
        self.gender = gender
        self.pregnant = pregnant
        self.breast_feeding = breast_feeding

    @property
    def eligible(self):
        """Returns True if gender is valid and female not pregnant.
        """
        eligible = False
        if self.gender == MALE:
            eligible = True
        elif self.gender == FEMALE and not self.pregnant and not self.breast_feeding:
            eligible = True
        return eligible

    @property
    def reason(self):
        reason = None
        if not self.eligible:
            if self.pregnant:
                reason = 'pregnant'
            if self.breast_feeding:
                reason = 'breastfeeding'
            if self.gender not in [MALE, FEMALE]:
                reason = 'invalid gender'
        return reason


class Eligibility:

    def __init__(self, age=None, guardian=None, gender=None, pregnant=None,
                 meningitis_dx=None, no_drug_reaction=None,
                 no_concomitant_meds=None, no_amphotericin=None,
                 no_fluconazole=None, mental_status=None, breast_feeding=None):
        self.age_evaluator = AgeEvaluator(age=age)
        self.gender_evaluator = GenderEvaluator(
            gender=gender, pregnant=pregnant, breast_feeding=breast_feeding)
        mental_status_evaluator = MentalStatusEvaluator(
            mental_status=mental_status,
            guardian=guardian)
        self.criteria = dict(
            no_drug_reaction=no_drug_reaction,
            no_concomitant_meds=no_concomitant_meds,
            no_amphotericin=no_amphotericin,
            no_fluconazole=no_fluconazole,
            meningitis_dx=meningitis_dx,
            age=self.age_evaluator.eligible,
            gender=self.gender_evaluator.eligible,
            mental_status=mental_status_evaluator.eligible)

    @property
    def eligible(self):
        """Returns True if all criteria evaluate True.
        """
        return all(self.criteria.values())

    @property
    def reasons(self):
        """Returns a list of reason not eligible.
        """
        reasons = [k for k, v in self.criteria.items() if not v]
        if self.age_evaluator.reason:
            reasons.pop(reasons.index('age'))
            reasons.append(self.age_evaluator.reason)
        if self.gender_evaluator.reason:
            reasons.pop(reasons.index('gender'))
            reasons.append(self.gender_evaluator.reason)
        return reasons
