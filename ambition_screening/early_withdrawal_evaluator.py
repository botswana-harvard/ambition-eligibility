from ambition_visit_schedule import DAY1
from collections import OrderedDict
from django.apps import apps as django_apps
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from edc_reportable import IU_LITER, TEN_X_9_PER_LITER

from .reportables import alt_ref, neutrophil_ref, platlets_ref


class EarlyWithdrawalEvaluator:

    subject_screening_model = 'ambition_screening.subjectscreening'
    blood_result_model = 'ambition_subject.bloodresult'

    def __init__(self, alt=None, neutrophil=None, platlets=None, allow_none=None,
                 screening_identifier=None, subject_identifier=None, request=None):
        self._day_one_blood_results = None
        self._subject_screening = None
        self.reasons_ineligible = {}
        self.blood_results = OrderedDict(
            alt=alt, neutrophil=neutrophil, platlets=platlets)

        self.screening_identifier = screening_identifier
        self.subject_identifier = subject_identifier
        if self.subject_screening:
            self.update_blood_results(self.subject_screening)
        if self.day_one_blood_results:
            self.update_blood_results(self.day_one_blood_results)

        alt, neutrophil, platlets = [v for v in self.blood_results.values()]
        if (not alt and not neutrophil and not platlets and allow_none):
            self.eligible = True
            if request:
                messages.warning(
                    request, 'Screening blood results are required.')
        elif not alt and not neutrophil and not platlets and not allow_none:
            self.eligible = False
        else:
            if alt and not alt_ref.in_bounds(value=float(alt), units=IU_LITER):
                self.reasons_ineligible.update(
                    alt=f'High value: {alt}. {alt.description()}.')
            if neutrophil and not neutrophil_ref.in_bounds(float(neutrophil), units=TEN_X_9_PER_LITER):
                self.reasons_ineligible.update(
                    platlets=f'Low value: {neutrophil}. {neutrophil.description()}.')
            if platlets and not platlets_ref.in_bounds(float(platlets), units=TEN_X_9_PER_LITER):
                self.reasons_ineligible.update(
                    platlets=f'Low value: {platlets}. {platlets_ref.description()}.')
            self.eligible = (
                True if len(self.reasons_ineligible) == 0 else False)

    @property
    def subject_screening(self):
        if not self._subject_screening:
            model_cls = django_apps.get_model(self.subject_screening_model)
            try:
                self._subject_screening = model_cls.objects.get(
                    screening_identifier=self.screening_identifier)
            except ObjectDoesNotExist:
                pass
        return self._subject_screening

    @property
    def day_one_blood_results(self):
        if not self._day_one_blood_results:
            model_cls = django_apps.get_model(self.blood_result_model)
            try:
                self._day_one_blood_results = model_cls.objects.get(
                    subject_visit__subject_identifier=self.subject_identifier,
                    subject_visit__visit_code=DAY1)
            except ObjectDoesNotExist:
                pass
        return self._day_one_blood_results

    def update_blood_results(self, obj):
        if obj.alt:
            self.blood_results.update(alt=obj.alt)
        if obj.neutrophil:
            self.blood_results.update(neutrophil=obj.neutrophil)
        if obj.platlets:
            self.blood_results.update(platlets=obj.platlets)
