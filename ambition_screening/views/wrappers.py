from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from edc_base.utils import get_uuid
from edc_consent.site_consents import site_consents
from edc_model_wrapper import ModelWrapper

# this is bad. Means all of ambition subject needs to be imported
# just for this.
from ambition_subject.views import SubjectConsentModelWrapper


class ConsentMixin:

    @property
    def consent_object(self):
        """Returns the consent model.
        """
        default_consent_group = django_apps.get_app_config(
            'edc_consent').default_consent_group
        consent_object = site_consents.get_consent(
            report_datetime=self.object.report_datetime,
            consent_group=default_consent_group)
        return consent_object

    @property
    def consent(self):
        """Returns a wrapped saved or unsaved consent.
        """
        consent_model_wrapper_class = SubjectConsentModelWrapper
        try:
            consent = self.object.subjectconsent_set.get(
                version=self.consent_object.version)
        except ObjectDoesNotExist:
            consent = self.consent_object.model(
                subject_identifier=self.object.subject_identifier,
                consent_identifier=get_uuid(),
                subject_screening=self.object,
                version=self.consent_object.version)
        return consent_model_wrapper_class(consent)


class SubjectScreeningModelWrapper(ConsentMixin, ModelWrapper):

    model = 'ambition_screening.subjectscreening'
    next_url_name = django_apps.get_app_config(
        'ambition_screening').listboard_url_name
    next_url_attrs = ['screening_identifier']
    querystring_attrs = ['gender']
