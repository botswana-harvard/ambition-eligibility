from edc_constants.constants import MALE, FEMALE


def age_eligible(age=None, guardian=None):
    eligible = False
    try:
        if 17 < age < 65:
            eligible = True
        elif guardian and age < 18:
            eligible = True
    except TypeError:
        pass
    return eligible


def gender_eligible(gender=None, not_pregnant=None):
    eligible = False
    if gender == MALE:
        eligible = True
    elif gender == FEMALE and not_pregnant:
        eligible = True
    return eligible


class Eligibility:

    def __init__(self, age=None, guardian=None, gender=None, not_pregnant=None,
                 meningitis_dx=None, no_drug_reaction=None, no_concomitant_meds=None,
                 no_amphotericin=None, no_fluconazole=None):
        criteria = dict(no_drug_reaction=no_drug_reaction,
                        no_concomitant_meds=no_concomitant_meds,
                        no_amphotericin=no_amphotericin,
                        no_fluconazole=no_fluconazole,
                        meningitis_dx=meningitis_dx)
        criteria.update(age=age_eligible(age=age, guardian=guardian))
        criteria.update(
            gender=gender_eligible(gender=gender, not_pregnant=not_pregnant))
        self.eligible = all(criteria.values())
        self.reasons = [k for k, v in criteria.items() if not v]
