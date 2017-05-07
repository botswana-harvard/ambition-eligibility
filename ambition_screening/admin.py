from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin

from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin)

from .admin_site import ambition_screening_admin
from .models import SubjectScreening


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


@admin.register(SubjectScreening, site=ambition_screening_admin)
class SubjectScreeningAdmin(ModelAdminMixin, admin.ModelAdmin):

    radio_fields = {
        'sex': admin.VERTICAL,
        'meningitis_diagoses_by_csf_or_crag': admin.VERTICAL,
        'consent_to_hiv_test': admin.VERTICAL,
        'willing_to_give_informed_consent': admin.VERTICAL,
        'pregnancy_or_lactation': admin.VERTICAL,
        'previous_adverse_drug_reaction': admin.VERTICAL,
        'medication_contraindicated_with_study_drug': admin.VERTICAL,
        'two_days_amphotericin_b': admin.VERTICAL,
        'two_days_fluconazole': admin.VERTICAL, }

    fieldsets = (
        (None, {
            'fields': (
                'report_datetime',
                'sex',
                'age',
                'meningitis_diagoses_by_csf_or_crag',
                'consent_to_hiv_test',
                'willing_to_give_informed_consent',
                'pregnancy_or_lactation',
                'previous_adverse_drug_reaction',
                'medication_contraindicated_with_study_drug',
                'two_days_amphotericin_b',
                'two_days_fluconazole')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj))
