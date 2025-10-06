# documents/api_urls.py
from django.urls import path
from . import api

urlpatterns = [
    path('client/<str:ref>/documents/', api.client_documents, name='client-documents'),
]