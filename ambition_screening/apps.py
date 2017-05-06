# coding=utf-8

from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'ambition_screening'
    listboard_template_name = 'ambition_screening/listboard.html'
    listboard_url_name = 'ambition_screening:listboard_url'
    base_template_name = 'edc_base/base.html'
    url_namespace = 'ambition_screening'  # FIXME: is this still neeed??
    admin_site_name = 'ambition_screening_admin'
