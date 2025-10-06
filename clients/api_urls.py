# clients/api_urls.py
from django.urls import path
from . import api

urlpatterns = [
    path('client/login/', api.ClientLoginView.as_view(), name='client-login'),
    path('client/<str:ref>/services/', api.client_services, name='client-services'),
    path('client/<str:ref>/services/<int:service_id>/timeline/', api.service_timeline, name='client-service-timeline'),
]