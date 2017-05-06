# coding=utf-8

from django.contrib.admin import AdminSite


class AmbitionScreeningAdminSite(AdminSite):
    site_title = 'Ambition Screening'
    site_header = 'Ambition Screening'
    index_title = 'Ambition Screening'
    site_url = '/ambition_screening/listboard/'


ambition_screening_admin = AmbitionScreeningAdminSite(name='ambition_screening_admin')
