from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin

from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin)

from .admin_site import ambition_screening_admin
from .forms import SubjectScreeningForm
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

    form = SubjectScreeningForm

    radio_fields = {
        'gender': admin.VERTICAL,
        'meningitis_dx': admin.VERTICAL,
        'will_hiv_test': admin.VERTICAL,
        'mental_status': admin.VERTICAL,
        'guardian': admin.VERTICAL,
        'pregnancy_or_lactation': admin.VERTICAL,
        'previous_drug_reaction': admin.VERTICAL,
        'contraindicated_meds': admin.VERTICAL,
        'received_amphotericin': admin.VERTICAL,
        'received_fluconazole': admin.VERTICAL, }

    fieldsets = (
        (None, {
            'fields': (
                'report_datetime',
                'gender',
                'age_in_years',
                'meningitis_dx',
                'will_hiv_test',
                'mental_status',
                'guardian',
                'pregnancy_or_lactation',
                'preg_test_date',
                'previous_drug_reaction',
                'contraindicated_meds',
                'received_amphotericin',
                'received_fluconazole')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj))
