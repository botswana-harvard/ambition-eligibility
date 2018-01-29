from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = 'ambition_screening'
    verbose_name = 'Ambition Subject Screening'
    screening_age_adult_upper = 99
    screening_age_adult_lower = 18
