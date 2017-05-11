from model_mommy import mommy

from django.apps import apps as django_apps
from django.test import TestCase, tag

from edc_constants.constants import NO, FEMALE, YES, MALE

from ..eligibility import AgeEvaluator, GenderEvaluator, Eligibility


class TestSubjectScreening(TestCase):

    def setUp(self):
        django_apps.app_configs['ambition_screening'].screening_age_adult_upper = 64
        django_apps.app_configs['ambition_screening'].screening_age_adult_lower = 18
        django_apps.app_configs['ambition_screening'].screening_age_minor_lower = 16

    def test_eligibility_invalid_age_in_years(self):
        age_evaluator = AgeEvaluator(age=17)
        self.assertFalse(age_evaluator.eligible)
        age_evaluator = AgeEvaluator(age=65)
        self.assertFalse(age_evaluator.eligible)
        age_evaluator = AgeEvaluator(age=18)
        self.assertTrue(age_evaluator.eligible)
        age_evaluator = AgeEvaluator(age=64)
        self.assertTrue(age_evaluator.eligible)

    def test_eligibility_invalid_age_in_years_reasons(self):
        age_evaluator = AgeEvaluator(age=17)
        self.assertIn('age<18, no guardian', age_evaluator.reason)
        age_evaluator = AgeEvaluator(age=65)
        self.assertIn('age>64', age_evaluator.reason)

    def test_eligibility_minor_with_guardian(self):
        age_evaluator = AgeEvaluator(age=17, guardian=True)
        self.assertTrue(age_evaluator.eligible)

    def test_eligibility_minor_without_guardian(self):
        age_evaluator = AgeEvaluator(age=17)
        self.assertFalse(age_evaluator.eligible)

    def test_eligibility_gender(self):
        gender_evaluator = GenderEvaluator()
        self.assertFalse(gender_evaluator.eligible)
        gender_evaluator = GenderEvaluator(gender=FEMALE, pregnant=False)
        self.assertTrue(gender_evaluator.eligible)
        gender_evaluator = GenderEvaluator(gender=MALE)
        self.assertTrue(gender_evaluator.eligible)

    def test_eligibility_gender_reasons(self):
        gender_evaluator = GenderEvaluator()
        self.assertIn('invalid gender', gender_evaluator.reason)
        gender_evaluator = GenderEvaluator(gender=FEMALE, pregnant=True)
        self.assertIn('pregnant', gender_evaluator.reason)
        gender_evaluator = GenderEvaluator(gender='DOG')
        self.assertIn('invalid gender', gender_evaluator.reason)
        gender_evaluator = GenderEvaluator(gender=MALE)
        self.assertIsNone(gender_evaluator.reason)

    def test_eligibility(self):
        obj = Eligibility(
            age=18, gender=FEMALE, pregnant=False,
            meningitis_dx=True,
            no_drug_reaction=True,
            no_concomitant_meds=True,
            no_amphotericin=True,
            no_fluconazole=True)
        self.assertTrue(obj.eligible)
        self.assertIsNone(obj.reasons or None)

    def test_not_eligible(self):
        obj = Eligibility(
            age=18, gender=FEMALE, pregnant=False,
            meningitis_dx=True,
            no_drug_reaction=True,
            no_concomitant_meds=True,
            no_amphotericin=False,
            no_fluconazole=True)
        self.assertFalse(obj.eligible)
        self.assertIsNotNone(obj.reasons)

    def test_eligibility_reasons(self):
        obj = Eligibility(age=18, gender=FEMALE, pregnant=False)
        reasons = ['no_amphotericin', 'no_drug_reaction',
                   'no_concomitant_meds', 'no_fluconazole', 'meningitis_dx']
        reasons.sort()
        reasons1 = obj.reasons
        reasons1.sort()
        self.assertEqual(reasons, reasons1)

    def test_subject_eligible(self):
        """Asserts mommy recipe default criteria is eligible.
        """
        subject_screening = mommy.prepare_recipe(
            'ambition_screening.subjectscreening')
        self.assertTrue(subject_screening.eligible)

    def test_subject_invalid_age_in_years(self):
        """Asserts mommy recipe default criteria is eligible.
        """
        subject_screening = mommy.prepare_recipe(
            'ambition_screening.subjectscreening', age_in_years=2)
        subject_screening.verify_eligibility()
        self.assertFalse(subject_screening.eligible)

    def test_subject_age_lt_minor_lower(self):
        options = {'age_in_years': 15, 'guardian': NO}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening', **options)
        self.assertFalse(subject_screening.eligible)
        self.assertIn(
            subject_screening.reasons_ineligible, 'age<16')
        options = {'age_in_years': 15, 'guardian': YES}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening', **options)
        self.assertFalse(subject_screening.eligible)
        self.assertIn(
            subject_screening.reasons_ineligible, 'age<16')

    def test_subject_age_minor_no_guardian(self):
        options = {'age_in_years': 16, 'guardian': NO}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening', **options)
        self.assertFalse(subject_screening.eligible)
        self.assertIn(
            subject_screening.reasons_ineligible, 'age<18, no guardian')

    @tag('erik')
    def test_subject_age_minor_with_guardian_model(self):
        options = {'age_in_years': 16, 'guardian': YES}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening', **options)
        self.assertTrue(subject_screening.eligible)
        self.assertEqual(subject_screening.reasons_ineligible, '')

    def test_subject_age_lt_lower_adult(self):
        options = {'age_in_years': 16, 'guardian': NO}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening', **options)
        self.assertIn(
            subject_screening.reasons_ineligible, 'age<18, no guardian')
        self.assertFalse(subject_screening.eligible)

    def test_subject_age_gt_upper_adult(self):
        """Assert eligibility of a participant under age_in_years and no one willing
        to give informed consent.
        """
        options = {'age_in_years': 65, 'guardian': NO}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening', **options)
        self.assertIn(
            subject_screening.reasons_ineligible, 'age>64')
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_female_pregnant(self):
        """Assert not eligible if pregnant.
        """
        options = {'gender': FEMALE, 'pregnancy_or_lactation': YES}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening', **options)
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_previous_adverse_drug_reaction(self):
        """Assert eligibility of a participant with a previous adverse 
        drug reaction.
        """
        options = {'previous_drug_reaction': YES}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening', **options)
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_taking_concomitant_medication(self):
        """Test eligibility of a participant taking concomitant
        medication.
        """
        options = {'contraindicated_meds': YES}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening', **options)
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_took_two_days_amphotricin_b(self):
        """Test eligibility of a participant that received two days
        amphotricin_b before screening.
        """
        options = {'received_amphotericin': YES}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening', **options)
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_took_received_fluconazole(self):
        """Assert eligibility of a participant that received two days
        fluconazole before screening.
        """
        options = {'received_fluconazole': YES}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening', **options)
        self.assertFalse(subject_screening.eligible)

    def test_successful_screening_id_not_regenerated_on_resave(self):
        """Test subject screening id is not regenerated when resaving
           subject screening
        """
        options = {'age_in_years': 19}
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening', **options)
        self.assertTrue(subject_screening.eligible)
        screening_id = subject_screening.screening_identifier
        subject_screening.save()
        self.assertEqual(subject_screening.screening_identifier, screening_id)
