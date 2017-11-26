# coding=utf-8

from django.contrib.admin import AdminSite


class AmbitionScreeningAdminSite(AdminSite):
    site_title = 'Ambition Screening'
    site_header = 'Ambition Screening'
    index_title = 'Ambition Screening'
    site_url = '/administration/'


ambition_screening_admin = AmbitionScreeningAdminSite(
    name='ambition_screening_admin')
