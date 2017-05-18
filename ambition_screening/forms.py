from django import forms

from edc_base.modelform_mixins import (
    CommonCleanModelFormMixin, ApplicableValidationMixin,
    RequiredFieldValidationMixin)
from edc_constants.constants import YES, FEMALE, MALE, NO

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
        preg = cleaned_data.get('pregnancy_or_lactation') in [YES, NO]
        self.required_if_true(
            preg,
            field='pregnancy_or_lactation',
            field_required='preg_test_date')
        self.validate_gender_pregancy()
        return cleaned_data

    def validate_gender_pregancy(self):
        cleaned_data = self.cleaned_data

        if (cleaned_data.get('gender') in [MALE]
                and cleaned_data.get('pregnancy_or_lactation') in [YES, NO]):
            raise forms.ValidationError({
                'pregnancy_or_lactation':
                'Gender is MALE, pregnancy must be Not Applicable.'})
        elif (cleaned_data.get('gender') in [FEMALE]
              and cleaned_data.get('pregnancy_or_lactation') not in [YES, NO]):
            raise forms.ValidationError({
                'pregnancy_or_lactation':
                'Gender is FEMALE, pregnancy must be either Yes or No.'})

    class Meta:
        model = SubjectScreening
        fields = '__all__'
