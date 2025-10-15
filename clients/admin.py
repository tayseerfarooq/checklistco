from django.contrib import admin
from .models import Client, Service, TimelineTask
from django.contrib.auth.hashers import make_password, is_password_usable


class TimelineTaskInline(admin.TabularInline):
    model = TimelineTask
    extra = 1
    fields = ('title', 'description', 'completed', 'current', 'created_at', 'completed_at')
    readonly_fields = ('created_at', 'completed_at')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('reference_id', 'name', 'email', 'active', 'created_at')
    search_fields = ('reference_id', 'name', 'email')
    list_filter = ('active', 'created_at')
    fields = ('reference_id', 'name', 'email', 'password', 'active')

    def save_model(self, request, obj, form, change):
        """
        Hash the password only if it isn't already hashed.
        """
        if not obj.password.startswith('pbkdf2_sha256$') and is_password_usable(obj.password):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'status', 'start_date', 'end_date', 'progress_percent')
    list_filter = ('status', 'start_date')
    search_fields = ('title', 'client__name')
    inlines = [TimelineTaskInline]


@admin.register(TimelineTask)
class TimelineTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'completed', 'current', 'created_at', 'completed_at')
    list_filter = ('completed', 'current')
    search_fields = ('title', 'service__title')


from django.contrib import admin

admin.site.site_header = "The Checklist Co. "
admin.site.site_title = "The Checklist Co. "
admin.site.index_title = "Welcome to The Checklist Co Management Portal"