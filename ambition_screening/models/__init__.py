from django.conf import settings

from .subject_screening import SubjectScreening

if settings.APP_NAME == 'ambition_screening':
    from ..tests import models
