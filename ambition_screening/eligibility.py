from django.apps import apps as django_apps

from edc_constants.constants import MALE, FEMALE


class AgeEvaluator:

    def __init__(self, age=None, guardian=None, adult_lower=None,
                 adult_upper=None, minor_lower=None):
        app_config = django_apps.get_app_config('ambition_screening')
        self.age = age
        self.guardian = guardian
        self.minor_lower = minor_lower or app_config.screening_age_minor_lower
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
            elif self.guardian and self.minor_lower <= self.age <= self.adult_lower:
                eligible = True
        except TypeError:
            pass
        return eligible

    @property
    def reason(self):
        reason = None
        if not self.eligible:
            if self.age < self.minor_lower:
                reason = f'age<{self.minor_lower}'
            elif self.age < self.adult_lower and not self.guardian:
                reason = f'age<{self.adult_lower}, no guardian'
            elif self.age < self.adult_lower:
                reason = f'age<{self.adult_lower}'
            elif self.age > self.adult_upper:
                reason = f'age>{self.adult_upper}'
        return reason


class GenderEvaluator:
    def __init__(self, gender=None, pregnant=None):
        self.gender = gender
        self.pregnant = pregnant

    @property
    def eligible(self):
        """Returns True if gender is valid and female not pregnant.
        """
        eligible = False
        if self.gender == MALE:
            eligible = True
        elif self.gender == FEMALE and not self.pregnant:
            eligible = True
        return eligible

    @property
    def reason(self):
        reason = None
        if not self.eligible:
            if self.pregnant:
                reason = 'pregnant'
            if self.gender not in [MALE, FEMALE]:
                reason = 'invalid gender'
        return reason


class Eligibility:

    def __init__(self, age=None, guardian=None, gender=None, pregnant=None,
                 meningitis_dx=None, no_drug_reaction=None, no_concomitant_meds=None,
                 no_amphotericin=None, no_fluconazole=None):
        self.age_evaluator = AgeEvaluator(age=age, guardian=guardian)
        self.gender_evaluator = GenderEvaluator(
            gender=gender, pregnant=pregnant)
        self.criteria = dict(
            no_drug_reaction=no_drug_reaction,
            no_concomitant_meds=no_concomitant_meds,
            no_amphotericin=no_amphotericin,
            no_fluconazole=no_fluconazole,
            meningitis_dx=meningitis_dx)
        self.criteria.update(age=self.age_evaluator.eligible)
        self.criteria.update(
            gender=self.gender_evaluator.eligible)

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
        return reasons
