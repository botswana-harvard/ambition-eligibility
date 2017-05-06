from django.apps import apps as django_apps

from edc_dashboard.wrappers.model_wrapper import ModelWrapper


class SubjectScreeningModelWrapper(ModelWrapper):

    model_name = 'ambition_screening.subjectscreening'
    next_url_name = django_apps.get_app_config(
        'ambition_screening').listboard_url_name
    next_url_attrs = {
        'ambition_screening.subjectscreening': ['screening_identifier']}
    extra_querystring_attrs = {
        'ambition_screening.subjectscreening': ['sex']}
    url_instance_attrs = [
        'screening_identifier', 'sex']
