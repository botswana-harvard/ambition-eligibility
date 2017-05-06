from model_mommy import mommy

from django.test import TestCase, tag

from edc_constants.constants import NO, FEMALE, YES


@tag('screening')
class TestSubjectScreening(TestCase):

    def test_subject_ineligible_lt_18_years(self):
        """Test eligibility of a participant under age and no one willing
           to give informed consent
        """
        options = {'age': 16, 'willing_to_give_informed_consent': NO}
        subject_screening = mommy.make_recipe(
            'ambition_subject.subject_screening', **options)
        self.assertIn(subject_screening.ineligibility, 'Participant is under 18')
        self.assertFalse(subject_screening.is_eligible)

    def test_subject_eligible_correct_age(self):
        """Test eligibility of a participant with correct age."""
        options = {'age': 19}
        subject_screening = mommy.make_recipe(
            'ambition_subject.subject_screening', **options)
        self.assertTrue(subject_screening.is_eligible)

    def test_subject_ineligible_female_pregnant(self):
        """Test eligibility of a participant currently pregnant"""
        options = {'sex': FEMALE, 'pregnancy_or_lactation': YES}
        subject_screening = mommy.make_recipe(
            'ambition_subject.subject_screening', **options)
        self.assertFalse(subject_screening.is_eligible)

    def test_subject_ineligible_previous_adverse_drug_reaction(self):
        """Test eligibility of a participant with a previous adverse drug
           reaction
        """
        options = {'previous_adverse_drug_reaction': YES}
        subject_screening = mommy.make_recipe(
            'ambition_subject.subject_screening', **options)
        self.assertFalse(subject_screening.is_eligible)

    def test_subject_ineligible_taking_concomitant_medication(self):
        """Test eligibility of a participant taking concomitant medication"""
        options = {'medication_contraindicated_with_study_drug': YES}
        subject_screening = mommy.make_recipe(
            'ambition_subject.subject_screening', **options)
        self.assertFalse(subject_screening.is_eligible)

    def test_subject_ineligible_took_two_days_amphotricin_b(self):
        """Test eligibility of a participant that received two days
           amphotricin_b before screening
        """
        options = {'two_days_amphotericin_b': YES}
        subject_screening = mommy.make_recipe(
            'ambition_subject.subject_screening', **options)
        self.assertFalse(subject_screening.is_eligible)

    def test_subject_ineligible_took_two_days_fluconazole(self):
        """Test eligibility of a participant that received two days
           fluconazole before screening
        """
        options = {'two_days_fluconazole': YES}
        subject_screening = mommy.make_recipe(
            'ambition_subject.subject_screening', **options)
        self.assertFalse(subject_screening.is_eligible)

    def test_successful_screening_id_not_regenerated_on_resave(self):
        """Test subject screening id is not regenerated when resaving
           subject screening
        """
        options = {'age': 19}
        subject_screening = mommy.make_recipe(
            'ambition_subject.subject_screening', **options)
        self.assertTrue(subject_screening.is_eligible)
        screening_id = subject_screening.screening_identifier
        subject_screening.save()
        self.assertEqual(subject_screening.screening_identifier, screening_id)
