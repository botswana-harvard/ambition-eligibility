from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_title = 'Ambition Screening'
    site_header = 'Ambition Screening'
    index_title = 'Ambition Screening'
    site_url = '/administration/'


ambition_screening_admin = AdminSite(name='ambition_screening_admin')
