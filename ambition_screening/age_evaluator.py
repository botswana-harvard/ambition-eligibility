from django.apps import apps as django_apps


class AgeEvaluator:

    def __init__(self, age=None, adult_lower=None, adult_upper=None, **kwargs):
        self.eligible = False
        self.reasons_ineligible = None
        app_config = django_apps.get_app_config('ambition_eligibility')
        adult_lower = int(adult_lower or app_config.screening_age_adult_lower)
        adult_upper = int(adult_upper or app_config.screening_age_adult_upper)
        if not age:
            self.reasons_ineligible = f'Age cannot be None.'
        else:
            age = int(age)
            if adult_lower <= age <= adult_upper:
                self.eligible = True
            if not self.eligible:
                if age < adult_lower:
                    self.reasons_ineligible = f'age<{adult_lower}.'
                elif age > adult_upper:
                    self.reasons_ineligible = f'age>{adult_upper}.'
