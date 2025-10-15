from django.urls import path
from .api import ContactFormView

urlpatterns = [
    path('contact/', ContactFormView.as_view(), name='contact_form'),
]