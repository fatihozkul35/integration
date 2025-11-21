from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage

# Register your models here.

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at', 'consent')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Kontaktinformationen'), {
            'fields': ('name', 'email', 'phone')
        }),
        (_('Nachricht'), {
            'fields': ('message',)
        }),
        (_('Status'), {
            'fields': ('consent', 'is_read', 'created_at')
        }),
    )
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = _("Als gelesen markieren")
    
    actions = [mark_as_read]
