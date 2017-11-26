from django.urls.conf import path

from .admin_site import ambition_screening_admin

app_name = 'ambition_screening'


urlpatterns = [
    path('admin/', ambition_screening_admin.urls)]
