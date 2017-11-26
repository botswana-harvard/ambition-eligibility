# coding=utf-8

from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'ambition_screening'
    admin_site_name = 'ambition_screening_admin'
    screening_age_adult_upper = 99
    screening_age_adult_lower = 18
