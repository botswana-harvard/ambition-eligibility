from django.test import TestCase, tag
from edc_constants.constants import YES, FEMALE, NO, NOT_APPLICABLE
from model_mommy import mommy

from ..forms import SubjectScreeningForm


class TestSubjectScreeningForm(TestCase):

    def test_default_mommy_recipe(self):
        obj = mommy.prepare_recipe('ambition_screening.subjectscreening')
        form = SubjectScreeningForm(data=obj.__dict__)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_female_no_preg_test_date(self):
        obj = mommy.prepare_recipe(
            'ambition_screening.subjectscreening',
            gender=FEMALE,
            pregnancy=NO)
        form = SubjectScreeningForm(data=obj.__dict__)
        self.assertFalse(form.is_valid())

    def test_male_pregnancy_yes(self):
        obj = mommy.prepare_recipe(
            'ambition_screening.subjectscreening',
            pregnancy=YES)
        form = SubjectScreeningForm(data=obj.__dict__)
        self.assertFalse(form.is_valid())

    def test_female_pregnancy_not_applicable(self):
        obj = mommy.prepare_recipe(
            'ambition_screening.subjectscreening',
            gender=FEMALE,
            pregnancy=NOT_APPLICABLE)
        form = SubjectScreeningForm(data=obj.__dict__)
        self.assertFalse(form.is_valid())
