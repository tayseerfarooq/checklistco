
from django.db import models
from clients.models import Client, Service

class Document(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='documents')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True, related_name='documents')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.client.reference_id})"