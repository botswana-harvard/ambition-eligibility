from model_mommy import mommy

from django.test import TestCase, tag

from edc_constants.constants import NO, FEMALE, YES, MALE

from ..eligibility import age_eligible, gender_eligible, Eligibility


class TestSubjectScreening(TestCase):

    def test_eligibility_invalid_age_in_years(self):
        self.assertFalse(age_eligible(age=17))
        self.assertFalse(age_eligible(age=65))
        self.assertTrue(age_eligible(age=18))
        self.assertTrue(age_eligible(age=64))

    def test_eligibility_minor_with_guardian(self):
        self.assertTrue(age_eligible(age=17, guardian=True))

    def test_eligibility_gender(self):
        self.assertFalse(gender_eligible(gender=None))
        self.assertTrue(gender_eligible(gender=FEMALE, not_pregnant=True))
        self.assertTrue(gender_eligible(gender=MALE))

    def test_eligibility(self):
        obj = Eligibility(age=18, gender=FEMALE, not_pregnant=True,
                          meningitis_dx=True,
                          no_drug_reaction=True,
                          no_concomitant_meds=True,
                          no_amphotericin=True,
                          no_fluconazole=True)
        self.assertTrue(obj.eligible)
        self.assertIsNone(obj.reasons or None)

    def test_not_eligible(self):
        obj = Eligibility(age=18, gender=FEMALE, not_pregnant=True,
                          meningitis_dx=True,
                          no_drug_reaction=True,
                          no_concomitant_meds=True,
                          no_amphotericin=False,
                          no_fluconazole=True)
        self.assertFalse(obj.eligible)
        self.assertIsNotNone(obj.reasons)
        obj.reasons = ['no_amphotericin']

    def test_eligibility_reasons(self):
        obj = Eligibility(age=18, gender=FEMALE, not_pregnant=True)
        reasons = ['no_amphotericin', 'no_drug_reaction',
                   'no_concomitant_meds', 'no_fluconazole', 'meningitis_dx']
        reasons.sort()
        obj.reasons.sort()
        self.assertEqual(reasons, obj.reasons)

    def test_subject_eligible(self):
        """Asserts mommy recipe default criteria is eligible.
        """
        subject_screening = mommy.prepare_recipe(
            'ambition_screening.subject_screening')
        self.assertTrue(subject_screening.eligible)

    def test_subject_invalid_age_in_years(self):
        """Asserts mommy recipe default criteria is eligible.
        """
        subject_screening = mommy.prepare_recipe(
            'ambition_screening.subject_screening', age_in_years=2)
        subject_screening.verify_eligibility()
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_lt_18_years(self):
        """Assert eligibility of a participant under age_in_years and no one willing
        to give informed consent.
        """
        options = {'age_in_years': 16, 'guardian': NO}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subject_screening', **options)
        self.assertIn(
            subject_screening.reasons_ineligible, 'age')
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_female_pregnant(self):
        """Assert not eligible if pregnant.
        """
        options = {'gender': FEMALE, 'pregnancy_or_lactation': YES}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subject_screening', **options)
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_previous_adverse_drug_reaction(self):
        """Assert eligibility of a participant with a previous adverse 
        drug reaction.
        """
        options = {'previous_drug_reaction': YES}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subject_screening', **options)
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_taking_concomitant_medication(self):
        """Test eligibility of a participant taking concomitant
        medication.
        """
        options = {'contraindicated_meds': YES}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subject_screening', **options)
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_took_two_days_amphotricin_b(self):
        """Test eligibility of a participant that received two days
        amphotricin_b before screening.
        """
        options = {'received_amphotericin': YES}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subject_screening', **options)
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_took_received_fluconazole(self):
        """Assert eligibility of a participant that received two days
        fluconazole before screening.
        """
        options = {'received_fluconazole': YES}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subject_screening', **options)
        self.assertFalse(subject_screening.eligible)

    def test_successful_screening_id_not_regenerated_on_resave(self):
        """Test subject screening id is not regenerated when resaving
           subject screening
        """
        options = {'age_in_years': 19}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subject_screening', **options)
        self.assertTrue(subject_screening.eligible)
        screening_id = subject_screening.screening_identifier
        subject_screening.save()
        self.assertEqual(subject_screening.screening_identifier, screening_id)
