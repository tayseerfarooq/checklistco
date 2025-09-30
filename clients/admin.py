from django.contrib import admin
from .models import Client, Service, TimelineTask

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('reference_id', 'name', 'email', 'active', 'created_at')
    search_fields = ('reference_id', 'name', 'email')
    list_filter = ('active', 'created_at')
    inlines = [ServiceInline]  # allows adding services directly under client

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('title', 'client__name', 'client__reference_id')

@admin.register(TimelineTask)
class TimelineTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'status', 'due_date', 'completed_at')
    list_filter = ('status', 'due_date')
    search_fields = ('title', 'service__title', 'service__client__reference_id')