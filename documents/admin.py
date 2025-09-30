from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'service', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('title', 'client__name', 'client__reference_id')