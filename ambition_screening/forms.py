from django import forms

from edc_base.modelform_validators import RequiredFieldValidator
from edc_constants.constants import YES, FEMALE, NO

from .models import SubjectScreening


class SubjectScreeningFormValidator(RequiredFieldValidator):

    def clean(self):
        condition = self.cleaned_data.get('gender') == FEMALE
        self.required_if_true(
            condition=condition, field_required='pregnancy_or_lactation')

        preg = self.cleaned_data.get('pregnancy_or_lactation') in [YES, NO]
        self.required_if_true(
            condition=preg,
            field='pregnancy_or_lactation',
            field_required='preg_test_date')
        return self.cleaned_data


class SubjectScreeningForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data = SubjectScreeningFormValidator(cleaned_data).clean()
        return cleaned_data

    class Meta:
        model = SubjectScreening
        fields = '__all__'
