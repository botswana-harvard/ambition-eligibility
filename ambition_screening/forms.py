from django import forms

from edc_base.modelform_mixins import (
    CommonCleanModelFormMixin, OtherSpecifyValidationMixin,
    ApplicableValidationMixin, Many2ManyModelValidationMixin,
    RequiredFieldValidationMixin, JSONModelFormMixin)

from ambition_subject.models import SubjectVisit

from .models import SubjectScreening


class SubjectModelFormMixin(CommonCleanModelFormMixin,
                            OtherSpecifyValidationMixin,
                            ApplicableValidationMixin,
                            Many2ManyModelValidationMixin,
                            RequiredFieldValidationMixin,
                            JSONModelFormMixin,
                            forms.ModelForm):

    visit_model = SubjectVisit


class SubjectScreeningForm(SubjectModelFormMixin):

    class Meta:
        model = SubjectScreening
        fields = '__all__'
