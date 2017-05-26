from django import forms

from edc_base.modelform_mixins import (
    CommonCleanModelFormMixin, ApplicableValidationMixin,
    RequiredFieldValidationMixin)
from edc_constants.constants import YES, FEMALE, MALE, NO, NOT_APPLICABLE

# from ambition_subject.models import SubjectVisit

from .models import SubjectScreening


class SubjectModelFormMixin(CommonCleanModelFormMixin,
                            ApplicableValidationMixin,
                            RequiredFieldValidationMixin,
                            forms.ModelForm):

    pass


class SubjectScreeningForm(SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        condition = cleaned_data.get('gender') == FEMALE
        self.required_if_true(
            condition=condition, field_required='pregnancy_or_lactation')

        preg = cleaned_data.get('pregnancy_or_lactation') in [YES, NO]
        self.required_if_true(
            condition=preg,
            field='pregnancy_or_lactation',
            field_required='preg_test_date')

        return cleaned_data

    class Meta:
        model = SubjectScreening
        fields = '__all__'
