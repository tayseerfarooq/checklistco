from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'client', 'date', 'amount', 'status', 'uploaded_at')
    list_filter = ('status', 'date')
    search_fields = ('invoice_number', 'client__reference_id', 'client__name')