from django import forms

from edc_base.modelform_mixins import CommonCleanModelFormMixin
from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, FEMALE, NO

from .models import SubjectScreening


class SubjectModelFormMixin(CommonCleanModelFormMixin, forms.ModelForm):

    pass


class SubjectScreeningForm(SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        form_validator = FormValidator(cleaned_data=cleaned_data)
        condition = cleaned_data.get('gender') == FEMALE
        self.required_if_true(
            condition=condition, field_required='pregnancy_or_lactation')

        preg = cleaned_data.get('pregnancy_or_lactation') in [YES, NO]
        form_validator.required_if_true(
            condition=preg,
            field='pregnancy_or_lactation',
            field_required='preg_test_date')

        return cleaned_data

    class Meta:
        model = SubjectScreening
        fields = '__all__'
